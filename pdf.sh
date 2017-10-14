#!/usr/bin/env bash

pandoc ${1}.md \
       --filter pandoc-citeproc \
       --standalone \
       --number-section \
       --csl template/acm.csl \
       --template template/paper.latex \
       template/common.yaml \
       -o pdf/${1}.pdf
