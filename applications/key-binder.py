#!/usr/bin/env python3

import ast
import json
import subprocess
from enum import Enum

# TODO
# - [FEATURE] Option for clearing custom keybindings: -c clear
# - [FEATURE] Option to replace custom settings (by default it should append them):  -o overwrite, -a append
# - [FEATURE] Option to dump existing custom keybindings: -d dump
# - [FEATURE] Option for validation of configuration file: -t test
# - https://lazka.github.io/pgi-docs/#Gio-2.0/classes/Settings.html

MEDIA_KEYS_SCHEMA = 'org.gnome.settings-daemon.plugins.media-keys'
CUSTOM_KEYBINDINGS_PATH = '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{}/'
CUSTOM_KEYBINDINGS_SCHEMA = MEDIA_KEYS_SCHEMA + '.custom-keybinding:' + CUSTOM_KEYBINDINGS_PATH


class GsettingsKey(Enum):
	NAME = 'name'
	COMMAND = 'command'
	BINDING = 'binding'
	CUSTOM_KEYBINDINGS = 'custom-keybindings'


def get_from_gsettings(schema, key):
	completed_process = _run_gsettings('get', schema, key.value)
	return completed_process.stdout.decode()


def set_in_gsettings(schema, key, value):
	_run_gsettings('set', schema, key.value, value)


def _run_gsettings(*args):
	command = ['gsettings']
	command.extend(args)
	return subprocess.run(command, stdout=subprocess.PIPE)  # In Python 3.7: capture_output=True


def get_existing_custom_keybindings():
	command_result = get_from_gsettings(MEDIA_KEYS_SCHEMA, GsettingsKey.CUSTOM_KEYBINDINGS)
	return [] if command_result.startswith('@as []') else ast.literal_eval(command_result)


def load_configuration():
	with open('./key-binder.json') as configuration:
		return json.load(configuration)


def main():
	configuration = load_configuration()
	custom_keybindings = get_existing_custom_keybindings()

	for index, binding in enumerate(configuration, len(custom_keybindings)):
		schema = CUSTOM_KEYBINDINGS_SCHEMA.format(index)

		custom_keybindings.append(CUSTOM_KEYBINDINGS_PATH.format(index))

		for key in (GsettingsKey.NAME, GsettingsKey.COMMAND, GsettingsKey.BINDING):
			set_in_gsettings(schema, key, binding[key.value])

	set_in_gsettings(MEDIA_KEYS_SCHEMA, GsettingsKey.CUSTOM_KEYBINDINGS, str(custom_keybindings))


if __name__ == '__main__':
	main()
