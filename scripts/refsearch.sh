#!/bin/sh

# Search reference tree located at $REFS using fzf
# Based on https://github.com/bellecp/fast-p

MINIREF_HOME=${MINIREF_HOME:-${HOME}/miniref}

cd "$MINIREF_HOME" && find . -type d -exec ref_summarise.sh {} \; |
 	fzf --read0 --reverse --exact --no-hscroll \
    --preview 'ref_preview.sh {1}' \
    --bind 'f1:execute(refview.sh {1})' \
    --bind 'enter:execute(cd {1} && $SHELL)' \
    --preview-window='wrap'
