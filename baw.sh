#!/bin/bash
# baw - bloated AUR wrapper
# written by null because he's a lazy piece of shit

# TODO: remove
# TODO: list
# TODO: command parsing
# TODO: search completion

# check if AUR_SHIT directory already exists
AUR_SHIT_DIR=$HOME/AUR_SHIT/
[ ! -e $AUR_SHIT_DIR ] && mkdir $AUR_SHIT_DIR && echo "created AUR_SHIT directory in $AUR_SHIT_DIR"

# download and install every parameter
if [ $1 = "install" ]; then
    shift # replace this with array slicing of args array, READ THE TUTORIAL ON THIS
    for arg; do
        cd $AUR_SHIT_DIR
        [ -e $AUR_SHIT_DIR/$arg ] && rm -Rf $AUR_SHIT_DIR/$arg # reinstall if already there
        # pipe error message to outputs
        # what does 2>&1 do??
        git clone https://aur.archlinux.org/$arg.git >/dev/null 2>&1 && echo "OK: git clone into $AUR_SHIT_DIR succesful, created $arg dir" || echo "ERROR: git clone of $arg directory FAILED"
        # make this automatically install with pacman without prompting user
        makepkg -sic $AUR_SHIT_DIR/$arg/PKGBUILD >/dev/null 2>&1 && echo "OK: installed package $arg" || echo "ERROR: makepkg FAILED, $arg not installed"
    done
fi
