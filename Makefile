# Root entry point. Build targets are added only when their implementations exist.
.PHONY: help docs-check device-check

help:
	@$(MAKE) -f build/Makefile help

docs-check:
	@$(MAKE) -f build/Makefile docs-check

device-check:
	@python3 tools/check-device-profile.py
