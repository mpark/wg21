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
	# Running table-of-contents option tests...
	@pandoc $(DATADIR)/srefs.defs options/toc_disabled.md \
		-o actual/toc_disabled.html --data-dir=$(DATADIR) -M data-dir=$(DATADIR) \
		-d doc -d formatting; \
	grep -Fq '<form class="view-controls">' actual/toc_disabled.html; \
	! grep -Fq '<nav id="TOC"' actual/toc_disabled.html; \
	! grep -Fq '<header class="toc-mobile-bar">' actual/toc_disabled.html; \
	! grep -Fq "document.querySelector('[role=\"doc-toc\"]')" actual/toc_disabled.html
	@pandoc $(DATADIR)/srefs.defs options/id_prefix.md \
		-o actual/id_prefix.html --data-dir=$(DATADIR) -M data-dir=$(DATADIR) \
		-d doc -d formatting --id-prefix=paper-; \
	grep -Fq '<nav id="paper-TOC"' actual/id_prefix.html; \
	grep -Fq '<dialog id="paper-toc-dialog"' actual/id_prefix.html; \
	grep -Fq 'aria-controls="paper-toc-dialog"' actual/id_prefix.html; \
	grep -Fq 'id="paper-heading"' actual/id_prefix.html; \
	grep -Fq 'href="#paper-heading"' actual/id_prefix.html
	# Running paper.mk tests...
	@$(MAKE) -C paper check

.PHONY: actual expected
actual expected:
	rm -rf $@
	@$(MAKE) -f ../flat.mk OUTDIR=$@ html latex

include ../flat.mk
