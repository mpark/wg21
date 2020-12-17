#!/usr/bin/env bash

: "${DATADIR:?Set 'DATADIR' to the absolute path to the data directory.}"

cat <<EOF
number-sections: true
table-of-contents: true
self-contained: true

data-dir: ${DATADIR}

filters:
  - pandoc-citeproc
  - wg21.py

template: wg21

css:
  - ${DATADIR}/templates/14882.css

pdf-engine: xelatex

metadata:
  datadir: ${DATADIR}
  csl: ${DATADIR}/csl/wg21.csl

metadata-file: ${DATADIR}/metadata.yaml
EOF
