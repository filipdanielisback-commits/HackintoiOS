#!/usr/bin/env python3
"""Validate the pinned XNU QEMU feasibility experiment inputs."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
workflow = ROOT / ".github/workflows/xnu-qemu-experiment.yml"
version_note = ROOT / "docs/xnu/ios-18.7.12-version.md"
boot_readme = ROOT / "bootloader/README.md"

checks = {
    "workflow exists": workflow.is_file(),
    "candidate commit pinned": "43a90889846e00bfb5cf1d255cdc0a701a1e05a4" in workflow.read_text(),
    "report artifact configured": "xnu-qemu-feasibility-report" in workflow.read_text(),
    "candidate caveat documented": "exact source match" in version_note.read_text(),
    "QEMU experiment limitation documented": "feasibility experiment" in boot_readme.read_text().lower(),
}
for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
if not all(checks.values()):
    sys.exit(1)
