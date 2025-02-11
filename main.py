import os
import argparse
import csv
from collections import namedtuple
from datetime import  datetime

def format_date(date_str):
    date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
    return date_obj.strftime("%B %d")

weather_records = namedtuple("weather_records", ["date", "max_temp", "min_temp", "humidity"])
def parsing_weather_files(directory):
    records = []
    all_files = os.listdir(directory)
    for filename in all_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file_obj:
            file_content = csv.reader(file_obj)
            next(file_content)
            for row in file_content:
                try:
                    date, max_temp, min_temp, humidity = row[0], row[1], row[3], row[7]
                    if max_temp and min_temp and humidity:
                        records.append(weather_records(date, int(max_temp), int(min_temp), int(humidity)))
                except Exception as e:
                    print(e)
    return records

def generate_yearly_report(records, year):
    yearly_record = []
    for row in records:
        if row.date.startswith(str(year)):
            yearly_record.append(row)
    if not yearly_record:
        print(f"No records found for ${year}")
        return

    highest = max(yearly_record, key=lambda x:x.max_temp)
    lowest = min(yearly_record, key=lambda x:x.min_temp)
    max_humidity = min(yearly_record, key=lambda x:x.humidity)

    print(f'Highest: {highest.max_temp}C on {format_date(highest.date)}')
    print(f'Lowest: {lowest.min_temp}C on {format_date(lowest.date)}')
    print(f'Humidity: {max_humidity.humidity}C on {format_date(max_humidity.date)}')


def generate_monthly_average(records, year, month):
    monthly_records = [r for r in records if r.date.startswith(f'{year}-{month}')]
    if not monthly_records:
        print(f'No records found for {year}/{month}')

    avg_high = sum(row.max_temp for row in monthly_records) / len(monthly_records)
    avg_low = sum(row.min_temp for row in monthly_records) / len(monthly_records)
    avg_humidity = sum(row.humidity for row in monthly_records) / len(monthly_records)

    print(f'Highest Average: {round(avg_high)}C')
    print(f'Lowest Average: {round(avg_low)}C')
    print(f'Average Mean Humidity: {round(avg_humidity)}C')


def generate_temp_charts(records, year, month):
    monthly_records = [row for row in records if row.date.startswith(f'{year}-{month}')]
    if not monthly_records:
        print(f'No records found for {year}/{month}')

    for record in monthly_records:
        # The below code is for task.03
        # print(f'{record.date.split("-")[-1]} \033[31m{"+" * record.max_temp}\033[0m {record.max_temp}C')
        # print(f'{record.date.split("-")[-1]} \033[34m{"+" * record.min_temp}\033[0m {record.min_temp}C')

        # The below code is for task. 05 (Grand task)
        print(f'{record.date.split("-")[-1]} \033[34m{"+" * record.min_temp}\033[0m \033[31m{"+" * record.max_temp}\033[0m {record.min_temp}C - {record.max_temp}C')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='it will be path to weather files given')
    parser.add_argument("-e","--year", help='yearly report')
    parser.add_argument("-a", "--avg", help='average monthly salary')
    parser.add_argument("-c", "--chart", help='Temperature Chart')
    args = parser.parse_args()
    records = parsing_weather_files(args.directory)
    if args.year:
        generate_yearly_report(records, args.year)
    if args.avg:
        year, month = map(int, args.avg.split('/'))
        generate_monthly_average(records, year, month)
    if args.chart:
        year, month = map(int, args.chart.split('/'))
        generate_temp_charts(records, year, month)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
