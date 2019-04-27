DATADIR=$(join $(dir $(lastword $(MAKEFILE_LIST))), data)
METADATA=$(wildcard metadata.yaml)
OUTDIR=generated

%.html %.latex %.pdf: %.md
	pandoc $(METADATA) $< $(DATADIR)/references.md \
       --self-contained \
       --table-of-contents \
       --csl $(DATADIR)/cpp.csl \
       --filter pandoc-citeproc \
       --filter $(DATADIR)/filter/wg21.py \
       --metadata datadir:$(DATADIR) \
       --metadata-file $(DATADIR)/metadata.yaml \
       --number-sections \
       --syntax-definition $(DATADIR)/syntax/isocpp.xml \
       --template $(DATADIR)/template/wg21 \
       --output $(OUTDIR)/$@
