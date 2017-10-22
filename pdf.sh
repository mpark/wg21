#!/usr/bin/env bash

pandoc template/header.yaml \
       ${1}.md \
       --number-section \
       --highlight-style=kate \
       --filter pandoc-citeproc \
       --syntax-definition template/cpp.xml \
       --syntax-definition template/diff.xml \
       --template template/wg21.latex \
       -o pdf/${1}.pdf
