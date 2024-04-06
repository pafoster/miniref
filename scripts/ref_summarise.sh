#!/bin/sh

# Helper script used by refsearch.sh
# Takes a reference as an argument and outputs the same reference, along with a
# summary of available textual information (NUL-terminated)
# (ref.bib, any other text files) for searching with refsearch.sh.

RIS_FILENAME="ref.ris"
MAX_CHARS=10000 # TODO Implement char limit

if test ! -z "$1"; then
    ris="$1"/"$RIS_FILENAME"
    # Use xargs to remove extraneous white-space and newlines
    test -f "$ris" && ris_summary=$(cut -d'-' -f2- "$ris" | xargs)

    # Find all ASCII files which are not $RIS_FILENAME
    # (don't descend into subdirectories)
    other_files_sumary=$(find "$1" -maxdepth 1 -type f \! -name "$RIS_FILENAME" \
        -exec grep -Iq . {} \; -print0 | xargs -0 cat | xargs)

    # Join reference to summaries using a tab and terminate with NUL
    printf '%s\t%s %s\0' "$1" "$ris_summary" "$other_files_sumary"
fi
