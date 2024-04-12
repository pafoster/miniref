#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

DESCRIPTION = """
refadd.py creates the directory `basename DIR` at $MINIREF_HOME, if it does not already exist ($MINIREF_HOME defaults
to $HOME/miniref). If SOURCE is specified, it is either copied to DIR or fetched remotely (depending on whether SOURCE
is a local path or a URL). If DOI is specified, SOURCE is populated with citation data in RIS format, fetched remotely
via HTTP and stored in the file ref.ris (overwriting any existing ref.ris file in the process). If DOI is not specified
and ref.ris does not exist, a minimal ref.ris is created based on a template. The -e flag causes ref.ris to be
subsequently opened using $EDITOR (first populating SOURCE with a template ref. Finally, refadd.py prints the full path
to DIR to stdout.
"""

MINIREF_HOME = os.environ.get('MINIREF_HOME', os.environ['HOME'] + '/miniref')

DOI_SERVICE_URL = 'http://dx.doi.org/'

TEMPLATE_RIS_ENTRY = """TY  - STD
TI  - 
AU  - 
PY  - 
UR  - 
ER  -
"""

RIS_FILENAME = 'ref.ris'

EDITOR = os.environ.get('EDITOR', 'vim')

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-s', '--source', type=str, help='source file (URL or local path)')
parser.add_argument('-i', '--doi', type=str, help='digital object identifier (e.g. 10.1002/andp.19053221004)')
parser.add_argument('-e', '--edit', action='store_true', help='edit citation data interactively using $EDITOR')
parser.add_argument('target', metavar='DIR', type=str, help='target directory (e.g. einstein1905elektrodynamik)')
args = parser.parse_args()

def create_target():
    target = Path(MINIREF_HOME, os.path.basename(args.target))
    try:
        os.makedirs(target, exist_ok=True)
        print(target)
    except OSError as e:
        print('{}: {}'.format(parser.prog, str(e)), file=sys.stderr)
        sys.exit(1)

    return target
target = create_target()

def copy_to_target():
    if args.source is not None:
        try:
            if re.match(r'(ftps?|https?)://.*', args.source):
                url = urllib.parse.urlparse(args.source)
                file_path = Path(target, os.path.basename(url.path))
                urllib.request.urlretrieve(args.source, file_path)
            else:
                file_path = Path(target, os.path.basename(args.source))
                shutil.copyfile(args.source, file_path)
        except OSError as e:
            print('{}: {}'.format(parser.prog, str(e)), file=sys.stderr)
            sys.exit(1)
copy_to_target()

def populate_metadata():
    file_path = Path(target, RIS_FILENAME)
    try:
        if args.doi is None and not file_path.is_file():
            with open(file_path, 'w') as f:
                f.write(TEMPLATE_RIS_ENTRY)
        if args.doi is not None and args.doi.strip():
            opener = urllib.request.build_opener()
            opener.addheaders = [('Accept', 'application/x-research-info-systems')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(DOI_SERVICE_URL + args.doi.strip(), file_path)

        if args.edit:
            subprocess.call([EDITOR, file_path])
    except OSError as e:
        print('{}: {}'.format(parser.prog, str(e)), file=sys.stderr)
        sys.exit(1)
populate_metadata()

