#!/usr/bin/env python3
"""Static contract checks for the XNU environment/build wrappers."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
env = (ROOT / "xnu-env.sh").read_text()
build = (ROOT / "xnu-build.sh").read_text()
checks = {
    "environment is repository-relative": 'dirname -- "${BASH_SOURCE[0]}"' in env,
    "candidate commit is pinned": "43a90889846e00bfb5cf1d255cdc0a701a1e05a4" in env,
    "candidate is not called an exact match": "candidate-not-exactly-matched-to-ios-18.7.12" in env,
    "SDK is not silently selected": 'XNU_SDKROOT="${XNU_SDKROOT:-${SDKROOT:-}}"' in env,
    "machine config must be supplied": 'set XNU_MACHINE_CONFIG' in build,
    "build requires explicit opt-in": 'XNU_BUILD_ENABLE:-0' in build,
    "source commit is verified": 'git -C "$XNU_SRC" rev-parse HEAD' in build,
    "ARM64 target is explicit": "ARCH_CONFIGS=ARM64" in build,
    "build limitation is documented": "does not imply HANOIP compatibility" in build,
}
for label, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {label}")
if not all(checks.values()):
    sys.exit(1)
