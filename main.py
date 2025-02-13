import os
import argparse
import csv
from collections import namedtuple
from datetime import  datetime

# function to format date in readable form
def format_date(date_str):
    date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
    return date_obj.strftime("%B %d")

# data structure to store each weather reading
weather_records = namedtuple("weather_records", ["date", "max_temp", "min_temp", "humidity"])

# function to parse weather data from files in given directory
def parsing_weather_files(directory):
    records = []
    all_files = os.listdir(directory) # list all files in directory
    for filename in all_files:
        filepath = os.path.join(directory, filename) # join file path
        with open(filepath, 'r') as file_obj:
            file_content = csv.reader(file_obj) # read csv file
            next(file_content) # skiping the header of each file
            for row in file_content:
                try:
                    # extracting the required values from CSV and add them to records
                    date, max_temp, min_temp, humidity = row[0], row[1], row[3], row[7]
                    if max_temp and min_temp and humidity:
                        records.append(weather_records(date, int(max_temp), int(min_temp), int(humidity)))
                except Exception as e:
                    print(e) # print the error in case of exception
    return records

# function to generate yearly report
def generate_yearly_report(records, year):
    yearly_record = []
    for row in records:
        if row.date.startswith(str(year)): # filter record for given year
            yearly_record.append(row)
    if not yearly_record:
        print(f"No records found for ${year}") # if record not found
        return

    highest = max(yearly_record, key=lambda x:x.max_temp) # find highest temperature record
    lowest = min(yearly_record, key=lambda x:x.min_temp) # find lowest temperature record
    max_humidity = min(yearly_record, key=lambda x:x.humidity) # maximum humidity record

    # displaying the result
    print(f'Highest: {highest.max_temp}C on {format_date(highest.date)}')
    print(f'Lowest: {lowest.min_temp}C on {format_date(lowest.date)}')
    print(f'Humidity: {max_humidity.humidity}C on {format_date(max_humidity.date)}')

# function to generate monthly average temperature and humidity
def generate_monthly_average(records, year, month):
    monthly_records = [r for r in records if r.date.startswith(f'{year}-{month}')] # filter record for given month
    if not monthly_records:
        print(f'No records found for {year}/{month}') # if record not found

    # calculate avg high, low temperature & humidity
    avg_high = sum(row.max_temp for row in monthly_records) / len(monthly_records)
    avg_low = sum(row.min_temp for row in monthly_records) / len(monthly_records)
    avg_humidity = sum(row.humidity for row in monthly_records) / len(monthly_records)

    # display the result
    print(f'Highest Average: {round(avg_high)}C')
    print(f'Lowest Average: {round(avg_low)}C')
    print(f'Average Mean Humidity: {round(avg_humidity)}C')


# function to generate temperature chart for each day in given month
def generate_temp_charts(records, year, month):
    monthly_records = [row for row in records if row.date.startswith(f'{year}-{month}')] # filter record for given month
    if not monthly_records:
        print(f'No records found for {year}/{month}') # if no records found for that month

    # loop through monthly_records to get each day data
    for record in monthly_records:
        # The below code is for task. 03
        # print(f'{record.date.split("-")[-1]} \033[31m{"+" * record.max_temp}\033[0m {record.max_temp}C')
        # print(f'{record.date.split("-")[-1]} \033[34m{"+" * record.min_temp}\033[0m {record.min_temp}C')

        # The below code is for task. 05 (Grand task)
        print(f'{record.date.split("-")[-1]} \033[34m{"+" * record.min_temp}\033[0m \033[31m{"+" * record.max_temp}\033[0m {record.min_temp}C - {record.max_temp}C')

# main function to execute command-line arguments
def main():
    parser = argparse.ArgumentParser() # initialize argument parser
    parser.add_argument('directory', help='it will be path to weather files given') # directory argument
    parser.add_argument("-e","--year", help='yearly report') # argument for yearly report
    parser.add_argument("-a", "--avg", help='average monthly report') # argument for monthly report
    parser.add_argument("-c", "--chart", help='Temperature Chart') # argument for generating temperature charts
    args = parser.parse_args() # parse argument to parser object

    # pass weather data files to function and get records
    records = parsing_weather_files(args.directory)

    # Logic based on provided arguments
    if args.year:
        generate_yearly_report(records, args.year) # if -e is provided then generate yearly report
    if args.avg:
        year, month = map(int, args.avg.split('/')) # split year and month from argument
        generate_monthly_average(records, year, month) # generate monthly average report if -a is provided
    if args.chart:
        year, month = map(int, args.chart.split('/')) # split year and month from argument
        generate_temp_charts(records, year, month) # generate the chart if -c is provided

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main() # call the main function
