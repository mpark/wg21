.PHONY: check
check: actual
	# Running rendering tests...
	@diff -ruN expected actual \
		&& printf '\033[32mRendering tests passed: actual output matches expected.\033[0m\n' \
		|| { printf '\033[31mRendering tests failed: actual output differs from expected.\033[0m\n'; exit 1; }
	# Running paper.mk tests...
	@$(MAKE) -C paper check

.PHONY: actual expected
actual expected:
	rm -rf $@
	@$(MAKE) -f ../flat.mk OUTDIR=$@ html latex

include ../flat.mk
