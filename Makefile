OUTDIR := generated

METADATA := $(wildcard metadata.yaml)

override DATADIR := $(dir $(lastword $(MAKEFILE_LIST)))data

$(OUTDIR)/%.html $(OUTDIR)/%.latex $(OUTDIR)/%.pdf: \
%.md $(DATADIR)/index.yaml $(DATADIR)/annex-f
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

override SRC := $(filter-out README.md, $(wildcard *.md))

override HTML := $(SRC:.md=.html)
override LATEX := $(SRC:.md=.latex)
override PDF := $(SRC:.md=.pdf)

.PHONY: all
all: $(PDF)

.PHONY: clean
clean:
	rm -rf $(OUTDIR)

.PHONY: update
update:
	wget https://wg21.link/index.yaml -O $(DATADIR)/index.yaml
	wget https://timsong-cpp.github.io/cppwp/annex-f -O $(DATADIR)/annex-f

$(DATADIR)/index.yaml:
	wget https://wg21.link/index.yaml -O $@

$(DATADIR)/annex-f:
	wget https://timsong-cpp.github.io/cppwp/annex-f -O $@

.PHONY: $(HTML)
$(HTML): %.html: $(OUTDIR)/%.html

.PHONY: $(LATEX)
$(LATEX): %.latex: $(OUTDIR)/%.latex

.PHONY: $(PDF)
$(PDF): %.pdf: $(OUTDIR)/%.pdf
