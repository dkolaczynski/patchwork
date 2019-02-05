#!/usr/bin/env python3

import datetime
import time
from argparse import ArgumentParser


def parse_arguments(parser):
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-d', '--date', action='store_true', help='ISO 8601 date')
	group.add_argument('-D', '--date-and-time', action='store_true', help='ISO 8601 date and time')
	group.add_argument('-T', '--timestamp', action='store_true', help='Unix time (in seconds)')
	group.add_argument('-M', '--timestamp-in-millis', action='store_true', help='Unix time in milliseconds')

	return parser.parse_args()


def prepare_date(timestamp):
	return datetime.date.fromtimestamp(timestamp).isoformat()


def prepare_date_and_time(timestamp):
	return datetime.datetime.fromtimestamp(timestamp).isoformat(timespec='seconds')


def prepare_timestamp(timestamp, in_millis=False):
	if in_millis:
		return round(timestamp * 1000)
	return round(timestamp)


def main():
	args = parse_arguments(ArgumentParser(description='''
		Print current date and/or time related value for given argument. If none of arguments is specified,
		it will print all values in the same order as they are listed in help.'''))

	timestamp = time.time()

	if args.date:
		print(prepare_date(timestamp))
	elif args.date_and_time:
		print(prepare_date_and_time(timestamp))
	elif args.timestamp:
		print(prepare_timestamp(timestamp))
	elif args.timestamp_in_millis:
		print(prepare_timestamp(timestamp, in_millis=True))
	else:
		print(prepare_date(timestamp))
		print(prepare_date_and_time(timestamp))
		print(prepare_timestamp(timestamp))
		print(prepare_timestamp(timestamp, in_millis=True))


if __name__ == '__main__':
	main()
