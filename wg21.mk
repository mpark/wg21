DEFAULTS ?=
REQUIREMENTS ?=

override ROOTDIR := $(dir $(lastword $(MAKEFILE_LIST)))

override DATADIR := $(ROOTDIR)data
override DEPSDIR := $(ROOTDIR)deps

override PANDOC_VER := 3.9.0.2
override PANDOC_DIR := $(DEPSDIR)/pandoc/$(PANDOC_VER)
override PYTHON_DIR := $(DEPSDIR)/python
override PYTHON_BIN := $(PYTHON_DIR)/bin/python3

export SHELL := bash
export PATH := $(PANDOC_DIR):$(PYTHON_DIR)/bin:$(PATH)

override define PANDOC
$(eval override FILES := $(filter %.md, $^))
$(eval override SUGGESTION := $(shell $(PYTHON_BIN) $(DATADIR)/suggest-target.py '$@'))
$(if $(FILES),,$(error No Markdown input found for target '$@'$(if $(SUGGESTION),. $(SUGGESTION))))
$(eval override CMD := pandoc $(DATADIR)/srefs.defs $(FILES) -o $@ --data-dir=$(DATADIR) -M data-dir=$(DATADIR) -d doc -d formatting)
$(eval $(and $(DEFAULTS), override CMD += -d $(DEFAULTS)))
$(if $(filter %.html, $@),
  $(eval override TOCDEPTH := $(shell $(PYTHON_BIN) $(DATADIR)/toc-depth.py < $(firstword $(FILES))))
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
	suggest-target.py \
	toc-depth.py)
$(eval $(and $(DEFAULTS), override SRCDEPS += $(DEFAULTS)))

override GENDEPS := $(PANDOC_DIR) $(PYTHON_DIR) $(addprefix $(DATADIR)/, csl.json srefs.json srefs.defs)
override DEPS := $(SRCDEPS) $(GENDEPS)

$(SRCDEPS): ;

$(PANDOC_DIR): $(DEPSDIR)/install-pandoc.sh
	PANDOC_VER=$(PANDOC_VER) PANDOC_DIR=$(PANDOC_DIR) $(DEPSDIR)/install-pandoc.sh

$(PYTHON_DIR): $(DEPSDIR)/install-venv.sh $(DEPSDIR)/requirements.txt $(REQUIREMENTS)
	PYTHON_DIR=$(PYTHON_DIR) $(DEPSDIR)/install-venv.sh -r $(DEPSDIR)/requirements.txt $(addprefix -r ,$(REQUIREMENTS))

$(DATADIR)/csl.json: $(DATADIR)/refs.py $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

$(DATADIR)/srefs.json: $(DATADIR)/srefs.py $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

$(DATADIR)/srefs.defs: $(DATADIR)/srefs-md.py $(DATADIR)/srefs.json $(PYTHON_DIR)
	set -e; trap 'rm -f "$@.tmp"' EXIT; $(PYTHON_BIN) $< < $(DATADIR)/srefs.json > "$@.tmp"; mv "$@.tmp" "$@"; trap - EXIT

.PHONY: distclean
distclean:
	rm -rf $(DEPSDIR)/pandoc $(DEPSDIR)/python $(GENDEPS)

.PHONY: update
update:
	@$(MAKE) -W $(DATADIR)/refs.py -W $(DATADIR)/srefs.py $(DATADIR)/csl.json $(DATADIR)/srefs.json $(DATADIR)/srefs.defs
