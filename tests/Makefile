include ../Makefile

.DEFAULT_GOAL := tests

.PHONY: tests
tests: $(HTML) $(LATEX) $(PDF)

.PHONY: check
check:
	rm -rf actual
	@$(MAKE) -f ../Makefile OUTDIR=actual html latex
	diff -ruN expected actual

.PHONY: expected
expected:
	rm -rf expected
	@$(MAKE) -f ../Makefile OUTDIR=expected html latex
