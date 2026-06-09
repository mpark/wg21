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

export SHELL := bash
export PATH := $(PANDOC_DIR):$(PYTHON_DIR)/bin:$(PATH)

override DATADIR := $(ROOTDIR)/data

override define PANDOC
$(eval override FILE := $(filter %.md, $^))
$(eval override CMD := pandoc $(FILE) -o $@ --data-dir=$(DATADIR) -d $(DATADIR)/defaults.yaml)
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

override GENDEPS := $(PANDOC_DIR) $(PYTHON_DIR) $(addprefix $(DATADIR)/, defaults.yaml csl.json srefs.json srefs.md)

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
	@$(MAKE) -W $(DATADIR)/refs.py -W $(DATADIR)/srefs.py $(DATADIR)/csl.json $(DATADIR)/srefs.json $(DATADIR)/srefs.md

$(OUTDIR):
	mkdir -p $@

$(PANDOC_DIR): $(DEPSDIR)/install-pandoc.sh
	PANDOC_VER=$(PANDOC_VER) PANDOC_DIR=$(PANDOC_DIR) $(DEPSDIR)/install-pandoc.sh

$(PYTHON_DIR): $(DEPSDIR)/install-venv.sh $(DEPSDIR)/requirements.txt $(REQUIREMENTS)
	PYTHON_DIR=$(PYTHON_DIR) $(DEPSDIR)/install-venv.sh -r $(DEPSDIR)/requirements.txt $(addprefix -r ,$(REQUIREMENTS))

$(DATADIR)/defaults.yaml: $(DATADIR)/defaults.sh
	DATADIR=$(abspath $(DATADIR)) $< > $@

$(DATADIR)/csl.json: $(DATADIR)/refs.py $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

$(DATADIR)/srefs.json: $(DATADIR)/srefs.py $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

$(DATADIR)/srefs.md: $(DATADIR)/srefs-md.py $(DATADIR)/srefs.json $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< < $(DATADIR)/srefs.json > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

$(OUTDIR)/%.html: $(SRCDIR)/%.md $(SRCDEPS) $(GENDEPS) | $(OUTDIR)
	$(PANDOC) --bibliography $(DATADIR)/csl.json

$(OUTDIR)/%.latex: $(SRCDIR)/%.md $(SRCDEPS) $(GENDEPS) | $(OUTDIR)
	$(PANDOC) --bibliography $(DATADIR)/csl.json

$(OUTDIR)/%.pdf: $(SRCDIR)/%.md $(SRCDEPS) $(GENDEPS) | $(OUTDIR)
	$(PANDOC) --bibliography $(DATADIR)/csl.json
