DATADIR = $(join $(dir $(lastword $(MAKEFILE_LIST))), data)
METADATA = $(wildcard metadata.yaml)
OUTDIR = generated

$(OUTDIR)/%.html $(OUTDIR)/%.latex $(OUTDIR)/%.pdf: %.md
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
       --output $@

SRC = $(wildcard *.md)

HTML = $(SRC:.md=.html)
LATEX = $(SRC:.md=.latex)
PDF = $(SRC:.md=.pdf)

.PHONY: $(HTML)
$(HTML): %.html: $(OUTDIR)/%.html

.PHONY: $(LATEX)
$(LATEX): %.latex: $(OUTDIR)/%.latex

.PHONY: $(PDF)
$(PDF): %.pdf: $(OUTDIR)/%.pdf
