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
	@output="$$(pandoc $(DATADIR)/srefs.defs warnings/missing_revision.md \
		-o /dev/null -t html --data-dir=$(DATADIR) -M data-dir=$(DATADIR) \
		-d doc -d formatting 2>&1)"; \
	printf '%s\n' "$$output"; \
	printf '%s\n' "$$output" | grep -Fq 'citation P2806 requires a revision. (e.g. `[@P2806R0]`)'; \
	! printf '%s\n' "$$output" | grep -Fq 'make update'
	# Running paper.mk tests...
	@$(MAKE) -C paper check

.PHONY: actual expected
actual expected:
	rm -rf $@
	@$(MAKE) -f ../flat.mk OUTDIR=$@ html latex

include ../flat.mk
