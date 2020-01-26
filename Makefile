SRCDIR ?= .
OUTDIR ?= generated

DEFAULTS ?= $(wildcard $(SRCDIR)/defaults.yaml)
METADATA ?= $(wildcard $(SRCDIR)/metadata.yaml)

override DATADIR := $(dir $(lastword $(MAKEFILE_LIST)))data

override SRC := $(filter-out %/README.md, $(wildcard $(SRCDIR)/*.md))

override HTML := $(SRC:.md=.html)
override LATEX := $(SRC:.md=.latex)
override PDF := $(SRC:.md=.pdf)

override define PANDOC
$(eval override FILE := $(filter %.md, $^))
$(eval override CMD := pandoc $(FILE) -o $@ -d $(DATADIR)/defaults.yaml)
$(eval $(and $(DEFAULTS), override CMD += -d $(DEFAULTS)))
$(eval $(and $(METADATA), override CMD += --metadata-file $(METADATA)))
$(if $(filter %.html, $@),
  $(eval override TOCDEPTH := $(shell $(DATADIR)/toc-depth.py < $(FILE)))
  $(eval $(and $(TOCDEPTH), override CMD += --toc-depth $(TOCDEPTH))))
$(CMD)
endef

override DEPS := $(OUTDIR)
override DEPS += $(addprefix $(DATADIR)/, defaults.yaml index.yaml annex-f)
$(eval $(and $(DEFAULTS), override DEPS += $(DEFAULTS)))
$(eval $(and $(METADATA), override DEPS += $(METADATA)))

.PHONY: all
all: $(PDF)

ifneq ($(SRCDIR), $(OUTDIR))
.PHONY: clean
clean:
	rm -rf $(OUTDIR)

.PHONY: $(HTML) $(LATEX) $(PDF)
$(HTML) $(LATEX) $(PDF): $(SRCDIR)/%: $(OUTDIR)/%
endif

.PHONY: update
update:
	@$(MAKE) --always-make $(DATADIR)/index.yaml $(DATADIR)/annex-f

$(OUTDIR):
	mkdir -p $@

$(DATADIR)/defaults.yaml: $(DATADIR)/defaults.py
	$< > $@

$(DATADIR)/index.yaml:
	wget https://wg21.link/index.yaml -O $@

$(DATADIR)/annex-f:
	wget https://timsong-cpp.github.io/cppwp/annex-f -O $@

$(OUTDIR)/%.html $(OUTDIR)/%.latex $(OUTDIR)/%.pdf: $(DEPS) $(SRCDIR)/%.md
	$(PANDOC) \
    --bibliography $(DATADIR)/index.yaml
