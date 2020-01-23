OUTDIR := generated

DEFAULTS := $(wildcard defaults.yaml)
METADATA := $(wildcard metadata.yaml)

override DATADIR := $(dir $(lastword $(MAKEFILE_LIST)))data

$(OUTDIR)/%.html $(OUTDIR)/%.latex $(OUTDIR)/%.pdf: \
%.md $(DATADIR)/defaults.yaml $(DATADIR)/index.yaml $(DATADIR)/annex-f
	@mkdir -p $(OUTDIR)
	$(eval override CMD := pandoc $< -o $@ -d $(DATADIR)/defaults.yaml)
	$(eval $(and $(DEFAULTS), override CMD += -d $(DEFAULTS)))
	$(eval $(and $(METADATA), override CMD += --metadata-file $(METADATA)))
	$(eval $(if $(filter %.html, $@), \
	  $(eval override TOCDEPTH := $(shell $(DATADIR)/toc-depth.py < $<)) \
	  $(and $(TOCDEPTH), override CMD += --toc-depth $(TOCDEPTH))))
	$(CMD)

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

$(DATADIR)/defaults.yaml: $(DATADIR)/defaults.py
	$(DATADIR)/defaults.py > $@

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
