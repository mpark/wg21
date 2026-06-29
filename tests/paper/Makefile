.PHONY: check
check:
	@$(MAKE) -C p0000 -B -n p0000r0.html | grep -q 'p0000r0.md' \
		|| { printf '\033[31mpaper.mk test failed: same-stem target did not use p0000r0.md.\033[0m\n'; exit 1; }
	@$(MAKE) -C p0000 -n P0000R0.html 2>&1 \
		| grep -q "Did you mean 'p0000r0.html'" \
		|| { printf '\033[31mpaper.mk test failed: typo target did not suggest p0000r0.html.\033[0m\n'; exit 1; }
	@$(MAKE) -C p2806 -B -n p2806r4.html | grep -q 'do-expr.md' \
		|| { printf '\033[31mpaper.mk test failed: remapped target did not use do-expr.md.\033[0m\n'; exit 1; }
	@$(MAKE) -C p2806 -B -n | grep -q -- '-o p2806r4.html' \
		|| { printf '\033[31mpaper.mk test failed: default target did not build p2806r4.html.\033[0m\n'; exit 1; }
	@printf '\033[32mpaper.mk tests passed.\033[0m\n'
