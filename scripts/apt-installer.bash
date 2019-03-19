#!/usr/bin/env bash

packages="
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
	shutter
	tree
	"

sudo apt update && sudo apt install ${packages}
