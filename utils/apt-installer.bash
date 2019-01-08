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
	mc
	meld
	shutter
	tree
	"

sudo apt update && sudo apt install $packages

