# Reveal.js presentations built from sources named `*.slides.md`.

slide_sources := $(wildcard *.slides.md)
paper_slide_source := $(wildcard $(addsuffix .slides.md,$(paper_src)))

override REVEALJS_VER := 5.2.1
override REVEALJS_SHA256 := 359b575dd51bbda32f89b2fd4c7dc46ad7389a805572158916c29252f7a27333
override REVEALJS_DIR := $(DEPSDIR)/revealjs/$(REVEALJS_VER)

slide_targets := $(slide_sources:.md=.html)
ifneq ($(paper_slide_source),)
slide_targets := $(filter-out $(paper_src).slides.html,$(slide_targets))
slide_targets += $(paper_id).slides.html
endif
targets += $(slide_targets)
slide_deps := $(addprefix $(DATADIR)/, \
	defaults/slides.yaml \
	favicon.ico \
	templates/slides.css)

override WATCHDEPS += $(slide_sources) $(slide_deps)

override define PANDOC_SLIDES
pandoc $(DATADIR)/srefs.defs $< -o $@ --data-dir=$(DATADIR) -M data-dir=$(DATADIR) -d slides -d formatting \
	-M revealjs-url=$(REVEALJS_DIR)
endef

.PHONY: slides
slides: $(addprefix $(OUTDIR)/,$(slide_targets))

$(OUTDIR)/%.slides.html: %.slides.md $(COMMONDEPS) $(slide_deps) $(GENDEPS) $(REVEALJS_DIR) | $(OUTDIR)
	$(PANDOC_SLIDES)

ifneq ($(paper_slide_source),)
$(OUTDIR)/$(paper_id).slides.html: $(paper_slide_source) $(COMMONDEPS) $(slide_deps) $(GENDEPS) $(REVEALJS_DIR) | $(OUTDIR)
	$(PANDOC_SLIDES)
endif

$(REVEALJS_DIR): $(DEPSDIR)/install-revealjs.sh
	REVEALJS_VER=$(REVEALJS_VER) \
	REVEALJS_SHA256=$(REVEALJS_SHA256) \
	REVEALJS_DIR=$(REVEALJS_DIR) \
		$<
