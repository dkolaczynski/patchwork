#!/usr/bin/env python3
# [Gedit Tool]
# Applicability=always
# Input=document
# Languages=
# Name=Format JSON
# Output=replace-document
# Save-files=nothing
# Shortcut=<Shift><Alt>j

import json
import sys


def format_json(text):
	json_text = json.loads(text.replace('\n', ''))
	return json.dumps(json_text, indent=2, sort_keys=False)


print(format_json(sys.stdin.read()))
