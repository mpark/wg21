DATADIR=$(join $(dir $(lastword $(MAKEFILE_LIST))), data)
OUTDIR=generated

%.pdf %.html: %.md
	pandoc $< $(DATADIR)/references.md \
       --self-contained \
       --table-of-contents \
       --csl $(DATADIR)/cpp.csl \
       --filter pandoc-citeproc \
       --filter $(DATADIR)/filter/diff.py \
       --filter $(DATADIR)/filter/tonytable.py \
       --highlight-style kate \
       --metadata-file $(DATADIR)/metadata.yaml \
       --number-sections \
       --syntax-definition $(DATADIR)/syntax/cpp.xml \
       --syntax-definition $(DATADIR)/syntax/diff.xml \
       --template $(DATADIR)/template/wg21 \
       --output $(OUTDIR)/$@
