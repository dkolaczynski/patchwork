#!/usr/bin/env python3

import ast
import os
import subprocess
import sys
from argparse import ArgumentParser


# TODO:
# - change configuration to JSON
# - remove configuration file restriction to be in the same directory
# - use common Python module

def parse_arguments(parser):
	parser.add_argument('-c', '--config-file', default='tabber.conf', metavar='NAME',
						help='name of configuration file (script looks for the file in its own directory)')
	parser.add_argument('-p', '--print-args', action='store_true', default=False,
						help='print arguments instead of launching the command')

	return parser.parse_args()


def resolve_configuration_path(filename):
	tabber_directory = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(tabber_directory, filename)


def print_error(message):
	print(message, file=sys.stderr)


def file_not_found_interruptor(func):
	def interruptor(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except FileNotFoundError as err:
			print_error('File not exist: ' + err.filename)
			sys.exit(os.EX_NOINPUT)

	return interruptor


@file_not_found_interruptor
def load_configuration(configuration_path):
	with open(configuration_path) as configuration:
		return ast.literal_eval(configuration.read())


def build_terminal_command(configuration):
	result = ['gnome-terminal']

	for entry in configuration:
		if 'profile' in entry:
			result.extend(['--tab-with-profile', entry['profile']])
		else:
			result.append('--tab')

		if 'title' in entry:
			result.extend(['-t', entry['title']])

		result.extend(['-e', 'bash -c "{0}"'.format(entry['command'])])

	return result


def main():
	args = parse_arguments(ArgumentParser(description='Launch terminal with multiple tabs'))
	configuration_path = resolve_configuration_path(args.config_file)
	configuration = load_configuration(configuration_path)
	terminal = build_terminal_command(configuration)

	if args.print_args:
		print(terminal)
	else:
		subprocess.run(terminal)


if __name__ == '__main__':
	main()
