#!/bin/sh

# Search reference tree located at $REFS using fzf
# Based on https://github.com/bellecp/fast-p

MINIREF_HOME=${MINIREF_HOME:-${HOME}/miniref}

cd "$MINIREF_HOME" && find . -type d -exec ref_summarise.sh {} \; |
 	fzf --read0 --reverse \
    --preview 'k={1} && test -f "$k"/ref.ris && cat "$k"/ref.ris; echo "---"; test -f "$k"/tags && cat "$k"/tags | tr "\n" " " && echo ""; echo "---"; find "$k" -maxdepth 1 -type f -iname "*.txt" -exec cat \{\} +' \
    --bind 'f1:execute(refview.sh {1})' \
    --bind 'enter:execute(cd {1} && $SHELL)' \
    --preview-window='wrap'
