#!/bin/sh

if test -f "$1"/ref.ris; then
    cat "$1"/ref.ris
    echo ""
fi
if test -f "$1"/tags; then
    tr "\n" " " < "$1"/tags && echo ""
    echo ""
fi
find "$1" -maxdepth 1 -type f -iname "*.txt" -exec cat '{}' +
