#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser


def parse_arguments(parser):
	parser.add_argument('source', help='link source', metavar='SOURCE')
	parser.add_argument('destination', help='link destination', metavar='DESTINATION')
	parser.add_argument('-f', '--force', action='store_true', help='remove existing destination symbolic link')

	return parser.parse_args()


def print_error(message):
	print(message, file=sys.stderr)


def main():
	args = parse_arguments(ArgumentParser(description='Create absolute symbolic link to a file'))
	source = os.path.abspath(args.source)
	destination = os.path.abspath(args.destination)

	try:
		os.symlink(source, destination)
	except FileExistsError:
		if args.force:
			if os.path.islink(destination):
				os.unlink(destination)
				os.symlink(source, destination)
			else:
				print_error('Failed to remove file "{0}": it is not a symbolic link'.format(destination))
		else:  # force flag was not specified
			print_error('Failed to create symbolic link "{0}": file exists'.format(destination))


if __name__ == '__main__':
	main()
