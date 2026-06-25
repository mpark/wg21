include ../flat.mk

.PHONY: check
check:
	# Running rendering tests...
	rm -rf actual
	@$(MAKE) -f ../flat.mk OUTDIR=actual html latex
	@diff -ruN expected actual \
		&& printf '\033[32mRendering tests passed: actual output matches expected.\033[0m\n' \
		|| { printf '\033[31mRendering tests failed: actual output differs from expected.\033[0m\n'; exit 1; }
	# Running paper.mk tests...
	@$(MAKE) -C paper check

.PHONY: expected
expected:
	rm -rf expected
	@$(MAKE) -f ../flat.mk OUTDIR=expected html latex
