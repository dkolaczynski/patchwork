#!/usr/bin/env python3

import json

from gi.repository import Gio  # PyGObject should be available by default

# TODO
# - [FEATURE] Option for clearing custom keybindings: -c clear
# - [FEATURE] Option to replace custom settings (by default it should append them):  -o overwrite, -a append
# - [FEATURE] Option to dump existing custom keybindings: -d dump
# - [FEATURE] Option for validation of configuration file: -t test

MEDIA_KEYS_SCHEMA = 'org.gnome.settings-daemon.plugins.media-keys'
CUSTOM_KEYBINDINGS_PATH = '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{}/'
CUSTOM_KEYBINDINGS_SCHEMA = MEDIA_KEYS_SCHEMA + '.custom-keybinding'

NAME_KEY = 'name'
COMMAND_KEY = 'command'
BINDING_KEY = 'binding'
CUSTOM_KEYBINDINGS_KEY = 'custom-keybindings'


def load_configuration():
	with open('./key-binder.json') as configuration:
		return json.load(configuration)


def main():
	new_bindings = load_configuration()
	existing_bindings = Gio.Settings(MEDIA_KEYS_SCHEMA).get_strv(CUSTOM_KEYBINDINGS_KEY)

	# Iterate through each defined keybinding
	for index, binding in enumerate(new_bindings, len(existing_bindings)):
		path = CUSTOM_KEYBINDINGS_PATH.format(index)
		settings = Gio.Settings.new_with_path(CUSTOM_KEYBINDINGS_SCHEMA, path)

		# Populate required data: name command and binding of each keybinding
		for key in (NAME_KEY, COMMAND_KEY, BINDING_KEY):
			settings.set_string(key, binding[key])
			Gio.Settings.sync()

		existing_bindings.append(path)

	Gio.Settings(MEDIA_KEYS_SCHEMA).set_strv(CUSTOM_KEYBINDINGS_KEY, existing_bindings)


if __name__ == '__main__':
	main()
