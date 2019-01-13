#!/usr/bin/env bash

packages="
	curl
	gimp
	git
	gitk
	gparted
	hardinfo
	htop
	`# contains inotifywait`
	inotify-tools
	`# contains xmllint`
	libxml2-utils
	mc
	meld
	shutter
	tree
	"

sudo apt update && sudo apt install ${packages}
