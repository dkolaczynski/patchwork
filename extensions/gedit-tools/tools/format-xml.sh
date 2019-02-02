#!/bin/sh
# [Gedit Tool]
# Applicability=always
# Input=document
# Languages=
# Name=Format XML
# Output=replace-document
# Save-files=nothing
# Shortcut=<Shift><Alt>x

xmllint --format /dev/stdin
