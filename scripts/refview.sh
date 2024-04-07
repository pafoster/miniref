#!/bin/sh

# Display first PDF for each reference using an xpdf subprocess

PDF_VIEWER=xpdf 

for ref in "$@"; do
    pdf=$( find "$ref" -maxdepth 1 -type f -iname "*.pdf" | head -1 )
    if test ! -z "$pdf"; then
        "$PDF_VIEWER" -title "$ref" "$pdf" &
    fi
done
