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
#   - DEFAULT_FORMAT := <html|pdf|latex>
#
#     Default format built by `make` with no explicit target.
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

DEFAULT_FORMAT ?= html
ifneq ($(filter $(DEFAULT_FORMAT),html pdf latex),$(DEFAULT_FORMAT))
$(error DEFAULT_FORMAT must be one of html, pdf, latex)
endif

DEFAULTS ?= $(wildcard defaults.yaml)
REQUIREMENTS ?= $(wildcard requirements.txt)

src := $(filter-out CHANGELOG.md LICENSE.md README.md, $(wildcard *.md))
html_targets := $(src:.md=.html)
pdf_targets := $(src:.md=.pdf)
latex_targets := $(src:.md=.latex)

.PHONY: all html pdf latex
all: $(DEFAULT_FORMAT)
html: $(html_targets)
pdf: $(pdf_targets)
latex: $(latex_targets)

include $(dir $(lastword $(MAKEFILE_LIST)))base.mk

targets := $(html_targets) $(pdf_targets) $(latex_targets)

.PHONY: clean
clean:
	rm -f $(addprefix $(OUTDIR)/,$(targets))

ifneq ($(OUTDIR),.)
$(OUTDIR):
	mkdir -p $@

# Specify the source to generated output mapping, e.g. `p2688r0.html` to `generated/p2688r0.html`
.PHONY: $(targets)
$(targets): %: $(OUTDIR)/%
endif

# Automatic rules to handle, e.g. `p2688r0.html : p2688r0.md`.
$(OUTDIR)/%.html: %.md $(DEPS) | $(OUTDIR)
	$(PANDOC)

$(OUTDIR)/%.latex: %.md $(DEPS) | $(OUTDIR)
	$(PANDOC)

$(OUTDIR)/%.pdf: %.md $(DEPS) | $(OUTDIR)
	$(PANDOC)
