#!/usr/bin/env python3

import json
from argparse import ArgumentParser

from gi.repository import Gio  # PyGObject should be available by default

# TODO
# - [FEATURE] Option to dump existing custom keybindings: -d dump
# - [FEATURE] Option for validation of configuration file: -t test

MEDIA_KEYS_SCHEMA = 'org.gnome.settings-daemon.plugins.media-keys'
CUSTOM_KEYBINDINGS_PATH = '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{}/'
CUSTOM_KEYBINDINGS_SCHEMA = MEDIA_KEYS_SCHEMA + '.custom-keybinding'

KEYBINDING_KEYS = ('name', 'command', 'binding')
CUSTOM_KEYBINDINGS_KEY = 'custom-keybindings'


def parse_arguments(parser):
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-a', '--append', action='store_true', help='TODO')
	group.add_argument('-o', '--overwrite', action='store_true', help='TODO')
	group.add_argument('-c', '--clear', action='store_true', help='TODO')

	return parser.parse_args()


def load_configuration():
	with open('./key-binder.json') as configuration:
		return json.load(configuration)


def overwrite_bindings():
	_add_bindings([])


def append_settings():
	existing_bindings = Gio.Settings(MEDIA_KEYS_SCHEMA).get_strv(CUSTOM_KEYBINDINGS_KEY)
	_add_bindings(existing_bindings)


def _add_bindings(existing_bindings):
	new_bindings = load_configuration()

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

	if args.append:  # TODO make this option a default one
		append_settings()
	elif args.overwrite:
		overwrite_bindings()
	elif args.clear:
		clear_settings()


if __name__ == '__main__':
	main()
