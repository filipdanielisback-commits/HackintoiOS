# Root entry point. All targets are documentation-only.
.PHONY: help docs-check

help:
	@$(MAKE) -f build/Makefile help

docs-check:
	@$(MAKE) -f build/Makefile docs-check
