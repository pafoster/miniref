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
refadd.py creates the directory DIR, if it does not already exist (any other directories in the path prefix of DIR
must already exist). If SOURCE is specified, it is either copied to DIR or fetched remotely (depending on whether SOURCE
is a local path or a URL). If DOI is specified, SOURCE is populated with citation data in RIS format, fetched remotely
via HTTP and stored in the file ref.ris (overwriting any existing ref.ris file in the process). If DOI is not specified
and ref.ris does not exist, a minimal ref.ris is created based on a template. The -e flag causes ref.ris to be
subsequently opened using $EDITOR (first populating SOURCE with a template ref. Finally, refadd.py prints DIR to stdout.

The recommended use of this utility is that DIR represents a single bibliographic reference via a meaningful directory
name. For example, we might use einstein1905elektrodynamik as the directory name for Albert Einstein's 1905 paper
"Zur Elektrodynamik bewegter Körper". In this way, basic use might involve populating a single directory
(e.g. ~/references) with a set of appropriately named sub-directories, each representing a unique bibliographic
reference. More advanced use of this utility (e.g. via additional scripting and/or involving the use of symbolic links)
is to use the file system to represent thematic relationships among bibliographic references, or to accommodate
workflows.
"""

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
    target = Path(args.target)
    if not target.is_dir():
        try:
            print('{}: Creating {}'.format(parser.prog, args.target), file=sys.stderr)
            os.mkdir(target)
        except OSError as e:
            print('{}: {}'.format(parser.prog, str(e)), file=sys.stderr)
            sys.exit(1)
    else:
        print('{}: Using existing {}'.format(parser.prog, args.target), file=sys.stderr)
create_target()

def copy_to_target():
    if args.source is not None:
        try:
            if re.match(r'(ftps?|https?)://.*', args.source):
                url = urllib.parse.urlparse(args.source)
                file_path = Path(args.target, os.path.basename(url.path))
                if file_path.is_file():
                    print('{}: Fetching to existing {}'.format(parser.prog, file_path), file=sys.stderr)
                urllib.request.urlretrieve(args.source, file_path)
            else:
                file_path = Path(args.target, os.path.basename(args.source))
                if file_path.is_file():
                    print('{}: Copying to existing {}'.format(parser.prog, file_path), file=sys.stderr)
                shutil.copyfile(args.source, file_path)
        except OSError as e:
            print('{}: {}'.format(parser.prog, str(e)), file=sys.stderr)
            sys.exit(1)
copy_to_target()

def populate_metadata():
    file_path = Path(args.target, RIS_FILENAME)
    try:
        if args.doi is None and not file_path.is_file():
            with open(file_path, 'w') as f:
                f.write(TEMPLATE_RIS_ENTRY)
        if args.doi is not None and args.doi.strip():
            if file_path.is_file():
                print('{}: Fetching to existing {}'.format(parser.prog, file_path), file=sys.stderr)

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

print(args.target)
