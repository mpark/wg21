SRCDIR ?= .
OUTDIR ?= generated

DEFAULTS ?= $(wildcard $(SRCDIR)/defaults.yaml)
METADATA ?= $(wildcard $(SRCDIR)/metadata.yaml)
REQUIREMENTS ?= $(wildcard $(SRCDIR)/requirements.txt)

override SRC := $(filter-out %/LICENSE.md %/README.md, $(wildcard $(SRCDIR)/*.md))

override HTML := $(SRC:.md=.html)
override LATEX := $(SRC:.md=.latex)
override PDF := $(SRC:.md=.pdf)

override ROOTDIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

override DEPSDIR := $(ROOTDIR)/deps

override PANDOC_VER := 3.9.0.2
override PANDOC_DIR := $(DEPSDIR)/pandoc/$(PANDOC_VER)
override PYTHON_DIR := $(DEPSDIR)/python
override PYTHON_BIN := $(PYTHON_DIR)/bin/python3
override PYTHON_STAMP := $(PYTHON_DIR)/.stamp

export SHELL := bash
export PATH := $(PANDOC_DIR):$(PYTHON_DIR)/bin:$(PATH)

override DATADIR := $(ROOTDIR)/data

override define PANDOC
$(eval override FILE := $(filter %.md, $^))
$(eval override CMD := pandoc $(FILE) -o $@ --mathjax -d $(DATADIR)/defaults.yaml)
$(eval $(and $(DEFAULTS), override CMD += -d $(DEFAULTS)))
$(eval $(and $(METADATA), override CMD += --metadata-file $(METADATA)))
$(if $(filter %.html, $@),
  $(eval override TOCDEPTH := $(shell $(PYTHON_BIN) $(DATADIR)/toc-depth.py < $(FILE)))
  $(eval $(and $(TOCDEPTH), override CMD += --toc-depth $(TOCDEPTH))))
$(CMD)
endef

override SRCDEPS := $(shell find $(DATADIR) -type f)
$(eval $(and $(DEFAULTS), override SRCDEPS += $(DEFAULTS)))
$(eval $(and $(METADATA), override SRCDEPS += $(METADATA)))

override GENDEPS := $(PANDOC_DIR) $(PYTHON_STAMP) $(addprefix $(DATADIR)/, defaults.yaml csl.json annex-f)

.PHONY: all
all: $(PDF)

.PHONY: html
html: $(HTML)

.PHONY: latex
latex: $(LATEX)

.PHONY: pdf
pdf: $(PDF)

ifneq ($(SRCDIR), $(OUTDIR))
.PHONY: clean
clean:
	rm -rf $(DEPSDIR)/pandoc $(DEPSDIR)/python $(GENDEPS) $(OUTDIR)

.PHONY: $(HTML) $(LATEX) $(PDF)
$(HTML) $(LATEX) $(PDF): $(SRCDIR)/%: $(OUTDIR)/%
endif

.PHONY: update
update:
	@$(MAKE) --always-make $(DATADIR)/csl.json $(DATADIR)/annex-f

$(OUTDIR):
	mkdir -p $@

$(PANDOC_DIR):
	PANDOC_VER=$(PANDOC_VER) PANDOC_DIR=$@ $(DEPSDIR)/install-pandoc.sh

$(PYTHON_STAMP): $(DEPSDIR)/requirements.txt $(REQUIREMENTS) $(ROOTDIR)/Makefile
	python3 -m venv $(PYTHON_DIR)
	$(PYTHON_BIN) -m pip install --upgrade pip -r $(DEPSDIR)/requirements.txt
	if [ -n "$(REQUIREMENTS)" ]; then $(PYTHON_BIN) -m pip install --upgrade pip -r $(REQUIREMENTS); fi
	touch $@

$(DATADIR)/defaults.yaml: $(DATADIR)/defaults.sh
	DATADIR=$(abspath $(DATADIR)) $< > $@

$(DATADIR)/csl.json: $(DATADIR)/refs.py $(PYTHON_STAMP)
	tmp="$@.tmp"; trap 'rm -f "$$tmp"' EXIT; $(PYTHON_BIN) $< > "$$tmp"; mv "$$tmp" $@

$(DATADIR)/annex-f:
	tmp="$@.tmp"; trap 'rm -f "$$tmp"' EXIT; curl -fsSL https://timsong-cpp.github.io/cppwp/annex-f -o "$$tmp"; mv "$$tmp" $@

$(OUTDIR)/%.html: $(SRCDIR)/%.md $(SRCDEPS) $(GENDEPS) | $(OUTDIR)
	$(PANDOC) --bibliography $(DATADIR)/csl.json

$(OUTDIR)/%.latex: $(SRCDIR)/%.md $(SRCDEPS) $(GENDEPS) | $(OUTDIR)
	$(PANDOC) --bibliography $(DATADIR)/csl.json

$(OUTDIR)/%.pdf: $(SRCDIR)/%.md $(SRCDEPS) $(GENDEPS) | $(OUTDIR)
	$(PANDOC) --bibliography $(DATADIR)/csl.json
