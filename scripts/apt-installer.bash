#!/usr/bin/env bash

packages="
	build-essential
	curl
	gimp
	git
	gitk
	gnome-tweak-tool
	gparted
	hardinfo
	htop
	httpie
	inotify-tools  `# contains inotifywait`
	libxml2-utils  `# contains xmllint`
	mc
	meld
	python-pip
	python3-pip
	shutter
	tree
	"

sudo apt update && sudo apt install ${packages}
