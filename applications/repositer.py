#!/usr/bin/env python3

import os
import os.path


def find_git_directory(working_directory):
	git_directory = os.path.join(working_directory, '.git')
	if os.path.exists(git_directory):
		return working_directory
	else:
		ancestor_directory = os.path.normpath(os.path.join(working_directory, '..'))
		if ancestor_directory == working_directory:
			return None
		else:
			return find_git_directory(ancestor_directory)


def main():
	current_directory = os.getcwd()
	git_directory = find_git_directory(current_directory)
	result = git_directory if git_directory else current_directory
	print(result)


if __name__ == '__main__':
	main()
