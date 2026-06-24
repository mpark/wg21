SRCDIR ?= .
OUTDIR ?= generated

DEFAULTS ?= $(wildcard $(SRCDIR)/defaults.yaml)
METADATA ?= $(wildcard $(SRCDIR)/metadata.yaml)
REQUIREMENTS ?= $(wildcard $(SRCDIR)/requirements.txt)

override SRC := $(filter-out %/CHANGELOG.md %/LICENSE.md %/README.md, $(wildcard $(SRCDIR)/*.md))

override HTML := $(SRC:.md=.html)
override LATEX := $(SRC:.md=.latex)
override PDF := $(SRC:.md=.pdf)

override ROOTDIR := $(dir $(lastword $(MAKEFILE_LIST)))

override DEPSDIR := $(ROOTDIR)deps

override PANDOC_VER := 3.9.0.2
override PANDOC_DIR := $(DEPSDIR)/pandoc/$(PANDOC_VER)
override PYTHON_DIR := $(DEPSDIR)/python
override PYTHON_BIN := $(PYTHON_DIR)/bin/python3

export SHELL := bash
export PATH := $(PANDOC_DIR):$(PYTHON_DIR)/bin:$(PATH)

override DATADIR := $(ROOTDIR)data

override define PANDOC
$(eval override AUX := $(filter $(DATADIR)/%, $(filter %.md, $^)))
$(eval override FILE := $(filter-out $(DATADIR)/%, $(filter %.md, $^)))
$(eval override CMD := pandoc $(AUX) $(FILE) -o $@ --data-dir=$(DATADIR) -M data-dir=$(DATADIR) -d doc -d formatting)
$(eval $(and $(DEFAULTS), override CMD += -d $(DEFAULTS)))
$(eval $(and $(METADATA), override CMD += --metadata-file $(METADATA)))
$(if $(filter %.html, $@),
  $(eval override TOCDEPTH := $(shell $(PYTHON_BIN) $(DATADIR)/toc-depth.py < $(firstword $(FILE))))
  $(eval $(and $(TOCDEPTH), override CMD += --toc-depth $(TOCDEPTH))))
$(CMD)
endef

override SRCDEPS := $(addprefix $(DATADIR)/, \
	csl/wg21.csl \
	defaults/doc.yaml \
	defaults/formatting.yaml \
	filters/citetitle.py \
	filters/wg21.py \
	syntax/highlighting-css.yaml \
	syntax/highlighting-macros.yaml \
	syntax/wg21.theme \
	syntax/wg21.xml \
	templates/14882.css \
	templates/wg21.css \
	templates/wg21.html \
	templates/wg21.latex \
	favicon.ico \
	metadata.yaml \
	toc-depth.py)
$(eval $(and $(DEFAULTS), override SRCDEPS += $(DEFAULTS)))
$(eval $(and $(METADATA), override SRCDEPS += $(METADATA)))

override GENDEPS := $(PANDOC_DIR) $(PYTHON_DIR) $(addprefix $(DATADIR)/, csl.json srefs.json srefs.md)
override DEPS := $(SRCDEPS) $(GENDEPS)  # This is used by downstream projects. Do not remove.

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

$(DATADIR)/csl.json: $(DATADIR)/refs.py $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

$(DATADIR)/srefs.json: $(DATADIR)/srefs.py $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

$(DATADIR)/srefs.md: $(DATADIR)/srefs-md.py $(DATADIR)/srefs.json $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< < $(DATADIR)/srefs.json > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

$(OUTDIR)/MANUAL.render.md: $(SRCDIR)/MANUAL.md $(DATADIR)/filters/render.py $(PANDOC_DIR) $(PYTHON_DIR) | $(OUTDIR)
	pandoc $< -o $@ --standalone --filter $(DATADIR)/filters/render.py

$(OUTDIR)/MANUAL.html $(OUTDIR)/MANUAL.latex $(OUTDIR)/MANUAL.pdf: $(OUTDIR)/MANUAL.render.md $(DEPS) | $(OUTDIR)
	$(PANDOC)

$(OUTDIR)/%.html: $(SRCDIR)/%.md $(DEPS) | $(OUTDIR)
	$(PANDOC)

$(OUTDIR)/%.latex: $(SRCDIR)/%.md $(DEPS) | $(OUTDIR)
	$(PANDOC)

$(OUTDIR)/%.pdf: $(SRCDIR)/%.md $(DEPS) | $(OUTDIR)
	$(PANDOC)
