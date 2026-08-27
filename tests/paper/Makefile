.PHONY: check
check: actual
	@diff -ruN expected actual \
		&& printf '\033[32mpaper.mk tests passed.\033[0m\n' \
		|| { printf '\033[31mpaper.mk tests failed: actual output differs from expected.\033[0m\n'; exit 1; }

.PHONY: actual expected
actual expected:
	rm -rf $@
	mkdir -p $@
	@$(MAKE) -C p0000 clean
	@$(MAKE) -C p0000
	cp p0000/p0000r0.html $@/p0000r0.html
	@$(MAKE) -C p0000 clean
	@$(MAKE) -C p2806
	cp p2806/p2806r4.html $@/p2806r4.html
	@$(MAKE) -C p2806 clean
	@$(MAKE) -C p2806 DEFAULT_FORMAT=latex
	cp p2806/p2806r4.latex $@/p2806r4.latex
	@$(MAKE) -C p2806 clean
	@$(MAKE) -C p2806 LEGACY=1
	@cmp p2806/p2806r4.html $@/p2806r4.html
	rm -f p2806/p2806r4.html
