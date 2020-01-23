#!/usr/bin/env python3

import pathlib

print(
"""\
number-sections: true
table-of-contents: true
self-contained: true

filters: [pandoc-citeproc, {datadir}/filter/wg21.py]
template: {datadir}/template/wg21

css: {datadir}/template/14882.css
input-file: {datadir}/references.md

metadata:
  datadir: {datadir}
  bibliography: {datadir}/index.yaml
  csl: {datadir}/wg21.csl

metadata-file: {datadir}/metadata.yaml\
""".format(datadir = pathlib.Path(__file__).parent.resolve()))
