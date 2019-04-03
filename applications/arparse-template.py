#!/usr/bin/env python3

from argparse import ArgumentParser


def parse_arguments(parser):
	return parser.parse_args()


def main():
	args = parse_arguments(ArgumentParser(description=''))


if __name__ == '__main__':
	main()
