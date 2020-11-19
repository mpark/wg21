#!/usr/bin/env python3

import pathlib

print(
"""\
number-sections: true
table-of-contents: true
self-contained: true

citeproc: true
filters: [{datadir}/filter/wg21.py]
template: {datadir}/template/wg21

css: {datadir}/template/14882.css

metadata:
  datadir: {datadir}

metadata-file: {datadir}/metadata.yaml\
""".format(datadir = pathlib.Path(__file__).parent.resolve()))
