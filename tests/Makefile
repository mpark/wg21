.PHONY: check
check: actual
	# Running rendering tests...
	@diff -ruN expected actual \
		&& printf '\033[32mRendering tests passed: actual output matches expected.\033[0m\n' \
		|| { printf '\033[31mRendering tests failed: actual output differs from expected.\033[0m\n'; exit 1; }
	# Running warning tests...
	@output="$$(pandoc $(DATADIR)/srefs.defs warnings/missing_citation.md \
		-o /dev/null -t html --data-dir=$(DATADIR) -M data-dir=$(DATADIR) \
		-d doc -d formatting 2>&1)"; \
	printf '%s\n' "$$output"; \
	printf '%s\n' "$$output" | grep -Fq 'Tip: run `make update` to refresh it'
	# Running paper.mk tests...
	@$(MAKE) -C paper check

.PHONY: actual expected
actual expected:
	rm -rf $@
	@$(MAKE) -f ../flat.mk OUTDIR=$@ html latex

include ../flat.mk
