DATADIR = $(dir $(lastword $(MAKEFILE_LIST)))data
METADATA = $(wildcard metadata.yaml)
OUTDIR = generated

$(OUTDIR)/%.html $(OUTDIR)/%.latex $(OUTDIR)/%.pdf: %.md
	mkdir -p $(OUTDIR) && \
	pandoc $< $(METADATA) $(DATADIR)/references.md \
       --number-sections \
       --self-contained \
       --table-of-contents \
       --bibliography $(DATADIR)/index.yaml \
       --csl $(DATADIR)/cpp.csl \
       --css $(DATADIR)/template/14882.css \
       --filter pandoc-citeproc \
       --filter $(DATADIR)/filter/wg21.py \
       --metadata datadir:$(DATADIR) \
       --metadata-file $(DATADIR)/metadata.yaml \
       --template $(DATADIR)/template/wg21 \
       --output $@

SRC = $(filter-out README.md, $(wildcard *.md))

HTML = $(SRC:.md=.html)
LATEX = $(SRC:.md=.latex)
PDF = $(SRC:.md=.pdf)

.PHONY: all
all: $(PDF)

.PHONY: clean
clean:
	rm -rf $(OUTDIR)/*

.PHONY: update
update:
	wget https://wg21.link/index.yaml -O $(DATADIR)/index.yaml
	wget https://timsong-cpp.github.io/cppwp/annex-f -O $(DATADIR)/annex-f

$(DATADIR)/index.yaml:
	wget https://wg21.link/index.yaml -O $@

$(DATADIR)/annex-f:
	wget https://timsong-cpp.github.io/cppwp/annex-f -O $@

.PHONY: $(HTML)
$(HTML): %.html: $(DATADIR)/index.yaml $(DATADIR)/annex-f $(OUTDIR)/%.html

.PHONY: $(LATEX)
$(LATEX): %.latex: $(DATADIR)/index.yaml $(DATADIR)/annex-f $(OUTDIR)/%.latex

.PHONY: $(PDF)
$(PDF): %.pdf: $(DATADIR)/index.yaml $(DATADIR)/annex-f $(OUTDIR)/%.pdf
