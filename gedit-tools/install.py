#!/usr/bin/env python3

import logging
import os
import shutil
import subprocess
import sys

POSSIBLE_TOOLS_PATHS = (os.path.join(os.environ['HOME'], *x) for x in (
	('.config', 'gedit', 'tools'),
	('.gnome2', 'gedit', 'tools')))

SCRIPTS = (
	{'file': 'format-json.py'},
	{'file': 'format-xml.sh', 'command': ('xmllint', '--version')},
	{'file': 'sort-lines.sh'},
	{'file': 'toggle-case.py'},
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def find_tools_path(paths):
	path = find_existing_path(paths)
	if path:
		return path

	logger.error('No tools path found, exiting!')
	logger.info('Please make sure that you have checked Preferences > Plugins > External Tools')
	sys.exit(1)


def find_existing_path(paths):
	logger.debug('Checking paths...')

	for path in paths:
		if os.path.isdir(path):
			logger.debug('Found: %s', path)
			return path

	logger.debug('No existing path found')
	return None


def copy_scripts(tools_path, scripts):
	for script in scripts:
		if 'command' in script:
			if not is_dependency_installed(script['command']):
				logger.warning('Could not copy "%s" because of unmet dependency', script['file'])
				continue

		destination = os.path.join(tools_path, script['file'])
		copy_file_if_not_exists(script['file'], destination)


def is_dependency_installed(command):
	logger.debug('Checking if dependency %s exists...', command[0])

	try:
		subprocess.run(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
		logger.debug('OK')
		return True
	except OSError:
		logger.warning('Dependency not found: %s', command[0])
		return False


def copy_file_if_not_exists(filename, destination):
	logger.debug('Checking if file "%s" already exists...', filename)

	if os.path.exists(destination):
		logger.debug('Yes, skipping')
		return

	logger.debug('No, copying...')
	source = os.path.join('tools', filename)
	shutil.copy2(source, destination)


def main():
	tools_path = find_tools_path(POSSIBLE_TOOLS_PATHS)
	copy_scripts(tools_path, SCRIPTS)


if __name__ == '__main__':
	main()
