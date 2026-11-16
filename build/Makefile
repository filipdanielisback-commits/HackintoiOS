# HackintoiOS research helper targets.
# These targets do not compile kernels, fetch firmware, create images, or touch devices.

.PHONY: help status docs-check

help:
	@echo "HackintoiOS research helpers"
	@echo "  make help       Show available targets"
	@echo "  make status     Show current project phase"
	@echo "  make docs-check Check that core documentation files exist"

status:
	@echo "Project phase: research and documentation"
	@echo "Target: Motorola Moto G60 (XT2135-2)"
	@echo "No functional port or device image is implemented."

docs-check:
	@test -f README.md
	@test -f docs/README.md
	@test -f docs/device-profile.md
	@test -f docs/roadmap.md
	@test -f docs/research-log.md
	@test -f kernel/README.md
	@test -f bootloader/README.md
	@test -f firmware/README.md
	@test -f hardware/README.md
	@echo "Core documentation files are present."
