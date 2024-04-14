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
refman.py checks if basename(abspath(REF_DIR)) is an existing subdirectory of $MINIREF_HOME. If not, it creates the
directory at $MINIREF_HOME ($MINIREF_HOME defaults to $HOME/miniref). If SOURCE is specified, it is either copied
to this existing/newly created target directory or fetched remotely (depending on whether SOURCE is a local path or a
URL). If DOI is specified, the target directory is populated with citation data in RIS format, fetched remotely via HTTP
and stored in the file ref.ris (overwriting any existing ref.ris file in the process). If DOI is not specified and
ref.ris does not exist, a minimal ref.ris is created based on a template. The -e flag causes ref.ris to be subsequently
opened using $EDITOR. If NEW_TAG is specified, the file tags.txt is created (or updated) to include NEW_TAG. If
EXISTING_TAG is specified, the specified tag is removed from tags.txt.

refman.py prints the full path of the target directory to stdout.
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
TAG_FILENAME = 'tags.txt'
EDITOR = os.environ.get('EDITOR', 'vim')

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-s', '--source', type=str, action='append', help='source file (URL or local path)')
parser.add_argument('-i', '--doi', type=str, help='digital object identifier (e.g. 10.1002/andp.19053221004)')
parser.add_argument('-e', '--edit', action='store_true', help='edit citation data interactively using $EDITOR')
parser.add_argument('-t', '--tag', metavar='NEW_TAG', action='append', type=str, help='new tag to add')
parser.add_argument('-u', '--untag', metavar='EXISTING_TAG', action='append', type=str, help='existing tag to remove')
parser.add_argument('target', metavar='REF_DIR', type=str, help='reference identifier (e.g. einstein1905elektrodynamik)')
args = parser.parse_args()

def create_target():
    target = Path(MINIREF_HOME, os.path.basename(os.path.abspath(args.target)))
    try:
        os.makedirs(target, exist_ok=True)
        print(target)
    except OSError as e:
        print('{}: {}'.format(parser.prog, str(e)), file=sys.stderr)
        sys.exit(1)

    return target
target = create_target()

def copy_to_target(source):
    try:
        if re.match(r'(ftps?|https?)://.*', source):
            url = urllib.parse.urlparse(source)
            file_path = Path(target, os.path.basename(url.path))
            urllib.request.urlretrieve(source, file_path)
        else:
            file_path = Path(target, os.path.basename(source))
            shutil.copyfile(source, file_path)
    except OSError as e:
        print('{}: {}'.format(parser.prog, str(e)), file=sys.stderr)
        sys.exit(1)
if args.source is not None:
    for s in args.source:
        copy_to_target(s)

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

def modify_tags(new_tags, tags_to_remove):
    try:
        file_path = Path(target, TAG_FILENAME)
        tags = set()
        if file_path.is_file():
            with open(file_path) as f:
                tags = set(line for line in f)
        tags |= set(new_tags)
        tags = set(t.strip() for t in tags if len(t.strip()) > 0)
        tags -= set(t.strip() for t in tags_to_remove)

        with open(file_path, 'w') as f:
            f.write('\n'.join(sorted(tags)))
            # Check number of tags (after filtering zero-length tags)
            if len(tags) > 0:
                f.write('\n')
    except OSError as e:
        print('{}: {}'.format(parser.prog, str(e)), file=sys.stderr)
if args.tag is not None:
    modify_tags(args.tag, set())
if args.untag is not None:
    modify_tags(set(), args.untag)
