#!/usr/bin/env bash


packages="
	curl
	gimp
	git
	htop
	`# contains inotifywait`
	inotify-tools
	shutter
	tree
	"

sudo apt update && sudo apt install $packages
