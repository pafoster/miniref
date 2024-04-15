#!/bin/sh

separator() {
    n=$(tput cols)
    printf "%${n}s" "" | tr " " "-"
}

if test -f "$1"/ref.ris; then
    cat "$1"/ref.ris
fi
separator
if test -f "$1"/tags; then
    tr "\n" " " < "$1"/tags && echo ""
fi
separator
find "$1" -maxdepth 1 -type f -iname "*.txt" -exec cat '{}' +
