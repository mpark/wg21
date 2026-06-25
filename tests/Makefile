include ../flat.mk

.PHONY: check
check:
	rm -rf actual
	@$(MAKE) -f ../flat.mk OUTDIR=actual html latex
	diff -ruN expected actual

.PHONY: expected
expected:
	rm -rf expected
	@$(MAKE) -f ../flat.mk OUTDIR=expected html latex
