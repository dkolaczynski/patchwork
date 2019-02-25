#!/usr/bin/env python3

import json
from argparse import ArgumentParser

from gi.repository import Gio  # PyGObject should be available by default

INPUT_FILENAME = './key-binder.json'
OUTPUT_FILENAME = './key-binder-dump.json'

MEDIA_KEYS_SCHEMA = 'org.gnome.settings-daemon.plugins.media-keys'
CUSTOM_KEYBINDINGS_PATH = '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{}/'
CUSTOM_KEYBINDINGS_SCHEMA = MEDIA_KEYS_SCHEMA + '.custom-keybinding'

KEYBINDING_KEYS = ('name', 'command', 'binding')
CUSTOM_KEYBINDINGS_KEY = 'custom-keybindings'


def parse_arguments(parser):
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-a', '--append', action='store_true', help='TODO')
	group.add_argument('-o', '--overwrite', action='store_true', help='TODO')
	cleararg = group.add_argument('-c', '--clear', action='store_true', help='TODO')
	group.add_argument('-d', '--dump', action='store_true', help='TODO')
	group.add_argument('-v', '--validate', action='store_true', help='TODO')
	filearg = parser.add_argument('-f', '--file', metavar='PATH', help='TODO')

	args = parser.parse_args()

	if args.clear and args.file:
		parser.error('the combination of arguments {}/{} and {}/{} is not allowed'
			.format(*cleararg.option_strings, *filearg.option_strings))
	return args


def load_configuration(path):
	with open(path) as configuration:
		return json.load(configuration)


def overwrite_bindings(path):
	_add_bindings(path, [])


def append_bindings(path):
	existing_bindings = Gio.Settings(MEDIA_KEYS_SCHEMA).get_strv(CUSTOM_KEYBINDINGS_KEY)
	_add_bindings(path, existing_bindings)


def dump_bindings(path):
	existing_bindings = Gio.Settings(MEDIA_KEYS_SCHEMA).get_strv(CUSTOM_KEYBINDINGS_KEY)
	bindings = []

	for binding in existing_bindings:
		setting = Gio.Settings(CUSTOM_KEYBINDINGS_SCHEMA, binding)
		binding = {}

		for key in KEYBINDING_KEYS:
			binding[key] = setting.get_string(key)

		bindings.append(binding)

	with open(path, 'w') as fp:
		json.dump(bindings, fp, indent='\t')
		fp.write('\n')


def _add_bindings(path, existing_bindings):
	new_bindings = load_configuration(path)

	# Iterate through each defined binding
	for index, binding in enumerate(new_bindings, len(existing_bindings)):
		path = CUSTOM_KEYBINDINGS_PATH.format(index)
		settings = Gio.Settings.new_with_path(CUSTOM_KEYBINDINGS_SCHEMA, path)

		# Populate required data: name, command and binding of each bindings
		for key in KEYBINDING_KEYS:
			settings.set_string(key, binding[key])
			Gio.Settings.sync()

		existing_bindings.append(path)

	Gio.Settings(MEDIA_KEYS_SCHEMA).set_strv(CUSTOM_KEYBINDINGS_KEY, existing_bindings)


def clear_settings():
	existing_bindings = Gio.Settings(MEDIA_KEYS_SCHEMA)

	for binding in existing_bindings.get_strv(CUSTOM_KEYBINDINGS_KEY):
		setting = Gio.Settings(CUSTOM_KEYBINDINGS_SCHEMA, binding)

		for key in KEYBINDING_KEYS:
			setting.reset(key)
			Gio.Settings.sync()

	existing_bindings.reset(CUSTOM_KEYBINDINGS_KEY)


def main():
	args = parse_arguments(ArgumentParser(description="TODO"))

	if args.append:
		append_bindings(args.file if args.file else INPUT_FILENAME)
	elif args.overwrite:
		overwrite_bindings(args.file if args.file else INPUT_FILENAME)
	elif args.clear:
		clear_settings()
	elif args.dump:
		dump_bindings(args.file if args.file else OUTPUT_FILENAME)


if __name__ == '__main__':
	main()
