ifeq ($(lastword $(MAKEFILE_LIST)),$(firstword $(MAKEFILE_LIST)))
include flat.mk

$(OUTDIR)/MANUAL.render.md: MANUAL.md $(DATADIR)/filters/render.py $(PANDOC_DIR) $(PYTHON_DIR) | $(OUTDIR)
	pandoc $< -o $@ --standalone --filter $(DATADIR)/filters/render.py

$(OUTDIR)/MANUAL.html $(OUTDIR)/MANUAL.latex $(OUTDIR)/MANUAL.pdf: $(OUTDIR)/MANUAL.render.md $(DEPS) | $(OUTDIR)
	$(PANDOC)

.PHONY: check
check:
	@$(MAKE) -C tests check
else
override THIS_FILE := $(lastword $(MAKEFILE_LIST))
override THIS_DIR := $(dir $(THIS_FILE))
override INCLUDED_FROM := $(lastword $(filter-out $(THIS_FILE),$(MAKEFILE_LIST)))

$(warning $(INCLUDED_FROM) includes deprecated $(THIS_FILE); include $(THIS_DIR)flat.mk or $(THIS_DIR)paper.mk instead. See https://mpark.github.io/wg21/MANUAL.html#project-layouts)

include $(THIS_DIR)flat.mk
endif
