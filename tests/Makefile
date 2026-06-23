SRCDIR := .
OUTDIR ?= out

.DEFAULT_GOAL := check

include ../Makefile

.PHONY: tests
tests:
	rm -rf out
	@$(MAKE) html latex pdf

.PHONY: check
check:
	rm -rf out
	@$(MAKE) html latex
	diff -ruN gold out

.PHONY: update-gold
update-gold:
	rm -rf gold
	@$(MAKE) OUTDIR=gold html latex
