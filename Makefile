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
override SAVED_GOAL := $(.DEFAULT_GOAL)
override THIS_FILE := $(lastword $(MAKEFILE_LIST))
override THIS_DIR := $(dir $(THIS_FILE))

$(warning Including $(THIS_FILE) is deprecated; include $(THIS_DIR)flat.mk instead.)
$(warning See https://mpark.github.io/wg21/MANUAL.html#project-layouts for further details.)

include $(THIS_DIR)flat.mk

.DEFAULT_GOAL := $(SAVED_GOAL)
endif
