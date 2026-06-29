# Flat project layout:
#
#   wg21-papers/
#   |-- wg21 (submodule)
#   |-- Makefile
#   |-- p2806r4.md
#   |-- p2996r13.md
#   `-- generated/
#       |-- p2806r4.html
#       `-- p2996r13.html
#
# From the top-level Makefile:
#
#   include path/to/wg21/flat.mk
#
# With that in place, the following commands are available:
#
#   make p2806r4.html  # builds generated/p2806r4.html from p2806r4.md
#   make p2806r4.latex # builds generated/p2806r4.latex from p2806r4.md
#   make p2806r4.pdf   # builds generated/p2806r4.pdf from p2806r4.md
#
#   make               # builds all the papers in HTML format (default)
#   make html          # builds all the papers in HTML format
#   make latex         # builds all the papers in LaTeX format
#   make pdf           # builds all the papers in PDF format
#
#   make clean         # deletes generated files
#
# The following variables can be set before including this file:
#
#   - OUTDIR := <path/to/directory>
#
#     Build the papers to the specified directory instead of `generated`
#
#   - DEFAULTS := <path/to/defaults.yaml>
#
#     Passed to Pandoc as an additional defaults file.
#     If a top-level `defaults.yaml` file exists, it will be used automatically.
#
#   - REQUIREMENTS := <path/to/requirements.txt>
#
#     Passed to Python virtual env to install additional packages.
#     If a top-level `requirements.txt` file exists, it will be used automatically.

OUTDIR ?= generated

DEFAULTS ?= $(wildcard defaults.yaml)
REQUIREMENTS ?= $(wildcard requirements.txt)

override SRC := $(filter-out CHANGELOG.md LICENSE.md README.md, $(wildcard *.md))

override HTML := $(SRC:.md=.html)
override LATEX := $(SRC:.md=.latex)
override PDF := $(SRC:.md=.pdf)

.PHONY: all
all: $(HTML)

.PHONY: html
html: $(HTML)

.PHONY: latex
latex: $(LATEX)

.PHONY: pdf
pdf: $(PDF)

include $(dir $(lastword $(MAKEFILE_LIST)))base.mk

.PHONY: clean

ifeq ($(OUTDIR),.)
clean:
	rm -f $(HTML) $(LATEX) $(PDF)
else
clean:
	rm -rf $(OUTDIR)

$(OUTDIR):
	mkdir -p $@

.PHONY: $(HTML) $(LATEX) $(PDF)
$(HTML) $(LATEX) $(PDF): %: $(OUTDIR)/%
endif

$(OUTDIR)/%.html: %.md $(DEPS) | $(OUTDIR)
	$(PANDOC)

$(OUTDIR)/%.latex: %.md $(DEPS) | $(OUTDIR)
	$(PANDOC)

$(OUTDIR)/%.pdf: %.md $(DEPS) | $(OUTDIR)
	$(PANDOC)
