#!/bin/bash
# baw - bloated AUR wrapper
# written by null because he's a lazy piece of shit

AUR_SHIT_DIR=$HOME/AUR_SHIT/
[ ! -e $AUR_SHIT_DIR ] && mkdir $AUR_SHIT_DIR && echo "created AUR_SHIT directory in $AUR_SHIT_DIR"

if [ $1 = "install" ]; then
    shift
    for arg; do
        cd $AUR_SHIT_DIR
        [ -e $AUR_SHIT_DIR/$arg ] && rm -Rf $AUR_SHIT_DIR/$arg
        git clone https://aur.archlinux.org/$arg.git >/dev/null 2>&1 && echo "OK: git clone into $AUR_SHIT_DIR succesful, created $arg dir" || echo "ERROR: git clone of $arg directory FAILED"
        cd $AUR_SHIT_DIR/$arg/
        makepkg -sic PKGBUILD && echo "OK: installed package $arg" || echo "ERROR: makepkg FAILED, $arg not installed"
    done
fi
