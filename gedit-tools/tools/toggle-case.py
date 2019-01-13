#!/usr/bin/env python3
# [Gedit Tool]
# Applicability=always
# Input=selection-document
# Languages=
# Name=Toggle Case
# Output=replace-selection
# Save-files=nothing
# Shortcut=<Shift><Alt>u

import sys


def toggle_case(text):
	if is_uppercase(text):
		return text.lower()
	return text.upper()


def is_uppercase(text):
	for letter in text:
		if letter.isalpha():
			return letter.isupper()
	return False


print(toggle_case(sys.stdin.read()), end='')
