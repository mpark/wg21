include flat.mk

$(OUTDIR)/MANUAL.render.md: MANUAL.md $(DATADIR)/filters/render.py $(PANDOC_DIR) $(PYTHON_DIR) | $(OUTDIR)
	pandoc $< -o $@ --standalone --filter $(DATADIR)/filters/render.py

$(OUTDIR)/MANUAL.html $(OUTDIR)/MANUAL.latex $(OUTDIR)/MANUAL.pdf: $(OUTDIR)/MANUAL.render.md $(DEPS) | $(OUTDIR)
	$(PANDOC)
