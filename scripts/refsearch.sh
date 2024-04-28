#!/bin/sh

# Search reference tree located at $REFS using fzf
# Based on https://github.com/bellecp/fast-p

MINIREF_HOME=${MINIREF_HOME:-${HOME}/miniref}

# TODO refactor, so that ref_summarise performs the `find . type d`
summarise_all="find . -type d -exec ref_summarise.sh \{\} \;"
cd "$MINIREF_HOME" && eval "$summarise_all" |
  	fzf --read0 --reverse --exact --no-hscroll \
    --preview-window down:80% \
    --preview 'ref_preview.sh {1}' \
    --bind 'ctrl-o:execute(refview.sh {1})' \
    --bind 'enter:execute(cd {1} && $SHELL)+reload('"$summarise_all"')' \
    --bind 'ctrl-r:reload('"$summarise_all"')' \
    --preview-window='wrap'
