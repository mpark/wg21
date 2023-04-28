#!/usr/bin/env bash

# MPark.WG21
#
# Copyright Michael Park, 2022
#
# Distributed under the Boost Software License, Version 1.0.
# (See accompanying file LICENSE.md or copy at http://boost.org/LICENSE_1_0.txt)

: "${DATADIR:?Set 'DATADIR' to the absolute path to the data directory.}"

cat <<EOF
number-sections: true
table-of-contents: true
self-contained: true

data-dir: ${DATADIR}

filters:
  - citeproc
  - wg21.py
  - pandoc_plantuml_filter.py

template: wg21

css:
  - ${DATADIR}/templates/14882.css

pdf-engine: xelatex

metadata:
  datadir: ${DATADIR}
  csl: ${DATADIR}/csl/wg21.csl

metadata-file: ${DATADIR}/metadata.yaml
EOF
