#!/bin/sh

# Helper script used by refsearch.sh
# Takes a reference as an argument and outputs the same reference, along with a
# summary of available textual information (NUL-terminated)
# (ref.bib, any other text files) for searching with refsearch.sh.

RIS_FILENAME="ref.ris"
MAX_CHARS=10000 # TODO Implement char limit

clean_spaces() {
    # Collapse successive [:space:] characters (includes tab, newline) into
    # a single ' '
    tr -s '[:space:]' ' '
}

if test ! -z "$1"; then
    ris="$1"/"$RIS_FILENAME"
    test -f "$ris" && ris_summary=$(cut -d'-' -f2- "$ris" | clean_spaces)

    # Find all *.txt and .*.txt files
    # (don't descend into subdirectories)
    other_files_sumary=$(find "$1" -maxdepth 1 -type f -iname "*.txt" -exec cat \{\} + | clean_spaces)

    # Join reference to summaries using a tab and terminate with NUL
    printf '%s\t%s %s\0' "$1" "$ris_summary" "$other_files_sumary"
fi
