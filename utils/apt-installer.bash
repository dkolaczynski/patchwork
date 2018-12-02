#!/usr/bin/env bash


packages="
	curl
	gimp
	git
	gitk
	hardinfo
	htop
	`# contains inotifywait`
	inotify-tools
	mc
	shutter
	tree
	"

sudo apt update && sudo apt install $packages

