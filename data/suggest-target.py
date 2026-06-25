#!/usr/bin/env python3

import difflib
import glob
import os
import sys

target = sys.argv[1]
directory, filename = os.path.split(target)
basename, ext = os.path.splitext(filename)

stems = [os.path.splitext(path)[0] for path in glob.glob('*.md')]
matches = difflib.get_close_matches(basename, stems, n=1)

if matches:
    stem = matches[0]
    suggestion = os.path.join(directory, f'{stem}{ext}')
    note = ' (names are case-sensitive)' if basename != stem and basename.lower() == stem.lower() else ''
    print(f"Did you mean '{suggestion}'?{note}")
