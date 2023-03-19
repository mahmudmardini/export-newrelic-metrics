# NewRelic Metrics Extractor

This Python script extracts and organizes important application metrics from the NewRelic API, including response time, throughput, and error rate. The extracted data is saved to a CSV file that can be used for further analysis.

## Prerequisites
Before running the script, you will need:

A NewRelic API key
A list of applications to extract metrics for (optional)

## Installation
To install the required dependencies, run:

`pip install requests pandas`


## Usage
To run the script, use the following command:

`python main.py <api_key> [<target_days>] [<application_list>]`

The api_key argument is required and should be replaced with your NewRelic API key. The target_days and application_list arguments are optional:

target_days: the number of days of metrics to extract (default: 30)
application_list: a JSON array of objects representing the applications to extract metrics for (default: all applications)
Example usage:

`python main.py ABC123 7 '[{"id":123,"name":"My App 1"},{"id":456,"name":"My App 2"}]'`

This will extract metrics for the applications with IDs 123 and 456 for the last 7 days, and save the results to a CSV file in the reports directory.

## Output
The extracted data is saved to a CSV file in the reports directory. The filename is constructed using the start and end dates of the time range being queried.

The CSV file contains the following columns:

Application Name: the name of the application
Application ID: the ID of the application
Response Time: the average response time in milliseconds
Throughput: the average number of requests per minute
Error Rate: the percentage of requests that resulted in errors

## License
This code is released under the MIT license.
