#!/usr/bin/env bash

# Move up in directory tree
#
# $ cd /usr/local/bin/; pwd
#   /usr/local/bin
# $ ...; pwd
#   /usr
alias up='../'
alias ..='../'
alias ...='../../'
alias ....='../../../'

# Make directory (with parents) and enter it
#
# $ cd /tmp; pwd
#   /tmp
# $ mkcd ./foo/bar/baz; pwd
#   /tmp/foo/bar/baz
alias mkcd='__mkcd'

# Reenter current directory
#
# $ cd /tmp; pwd
#   /tmp
# $ reenter; pwd
#   /tmp
alias reenter='cd $(pwd)'

# Print multiline $PATH splitted by colon
#
# $ path
#   /usr/bin
#   /sbin
#   /bin
# 	...
alias path='echo -e ${PATH//:/\\n}'

# Search in history
alias hgrep='history | grep'

# Search in processes
alias psgrep='ps aux | grep'

# Reload aliases
alias reload='source ~/.bash_aliases'

# Update and upgrade packages
alias upgrade='sudo apt update && sudo apt upgrade'

# Exiting the shorter way
alias q='exit'

function __mkcd() {
	mkdir --parents "$1" && cd "$_"
}
