include ../Makefile

.DEFAULT_GOAL := tests

.PHONY: tests
tests: $(HTML) $(LATEX) $(PDF)

.PHONY: check
check:
	rm -rf check
	@$(MAKE) -f ../Makefile OUTDIR=check html latex
	diff -ruN gold check

.PHONY: gold
gold:
	rm -rf gold
	@$(MAKE) -f ../Makefile OUTDIR=gold html latex
