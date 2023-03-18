import os
import requests
import json
from datetime import datetime, timedelta
from application_list import seller_base_applications
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('api_key', help='a string argument')
parser.add_argument('target_days', nargs='?', default='30', help='a string argument')
parser.add_argument('application_list', nargs='?', default='[]', help='a JSON array of objects')
arguments = parser.parse_args()

api_key = arguments.api_key
target_days = int(arguments.target_days)
target_applications = json.loads(arguments.application_list) or seller_base_applications

headers = {
    'Accept': 'application/json',
    'X-Api-Key': api_key
}

API_ENDPOINT = 'https://api.newrelic.com/v2/applications/{}/metrics/data.json'

start_time = datetime.utcnow() - timedelta(days=target_days)
start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')
start_date = start_time.strftime('%d-%m-%Y')
current_date = datetime.utcnow().strftime('%d-%m-%Y')

data = []
for application in target_applications:
    url = API_ENDPOINT.format(application['id'])
    params = {
        'from': start_time_str,
        'names[]': ['HttpDispatcher', 'Errors/all'],
        'summarize': True,
    }
    response = requests.get(url, headers=headers, params=params)

    try:
        response_data = response.json()
    except json.decoder.JSONDecodeError:
        print('Error: Invalid JSON response')
        continue

    if 'error' in response_data:
        print('Error:', response_data['error']['title'])
        continue

    metric_data = response_data['metric_data']
    call_count = metric_data['metrics'][0]['timeslices'][0]['values']['call_count']
    error_count = metric_data['metrics'][1]['timeslices'][0]['values']['error_count']
    response_time = metric_data['metrics'][0]['timeslices'][0]['values']['average_response_time']
    throughput = metric_data['metrics'][0]['timeslices'][0]['values']['requests_per_minute']
    error_rate = 100 * error_count / call_count

    data.append({
            'Application Name': application['name'],
            'Application ID': application['id'],
            'Response Time': f"{response_time:.3f} ms",
            'Throughput': f"{throughput:.3f}",
            'Error Rate': f"{error_rate:.2f}%",
        })

path = 'reports/'
file_name = f"Newrelic Metrics {start_date} -> {current_date}"

os.mkdir(path)
df = pd.DataFrame(data)
df.to_csv(f"{path}{file_name}.csv", index=False)

