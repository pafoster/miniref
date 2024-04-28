#!/bin/sh

# Search reference tree located at $REFS using fzf
# Based on https://github.com/bellecp/fast-p

MINIREF_HOME=${MINIREF_HOME:-${HOME}/miniref}

# TODO refactor, so that ref_summarise performs the `find . type d`
cd "$MINIREF_HOME" && find . -type d -exec ref_summarise.sh {} \; |
 	fzf --read0 --reverse --exact --no-hscroll \
    --preview-window down:80% \
    --preview 'ref_preview.sh {1}' \
    --bind 'ctrl-o:execute(refview.sh {1})' \
    --bind 'enter:execute(cd {1} && $SHELL)+reload(find . -type d -exec ref_summarise.sh \{\} \;)' \
    --bind 'ctrl-r:reload(find . -type d -exec ref_summarise.sh \{\} \;)' \
    --preview-window='wrap'
