#!/usr/bin/env bash
# Shared, repository-relative environment for HackintoiOS XNU research/build scripts.
# This file is intended to be sourced: source ./xnu-env.sh

_HACKINTIOS_ENV_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
export HACKINTIOS_ROOT="$_HACKINTIOS_ENV_DIR"
export XNUDEPS="${XNUDEPS:-$HACKINTIOS_ROOT/xnu-deps}"
export XNU_SRC="${XNU_SRC:-$HACKINTIOS_ROOT/xnu-src/xnu-11417.140.69}"

export XNU_UPSTREAM_URL="${XNU_UPSTREAM_URL:-https://github.com/apple-oss-distributions/xnu.git}"
export XNU_UPSTREAM_TAG="${XNU_UPSTREAM_TAG:-xnu-11417.140.69}"
export XNU_UPSTREAM_COMMIT="${XNU_UPSTREAM_COMMIT:-43a90889846e00bfb5cf1d255cdc0a701a1e05a4}"
export XNU_SOURCE_STATUS="candidate-not-exactly-matched-to-ios-18.7.12"

export XNU_HOST_OS="$(uname -s)"
export XNU_HOST_ARCH="$(uname -m)"
export XNU_TARGET_ARCH="arm64"

# Add project-built host tools only when that directory exists. Do not silently
# select an Apple SDK or override the caller's compiler/toolchain.
if [ -d "$XNUDEPS/host/bin" ]; then
    export PATH="$XNUDEPS/host/bin:$PATH"
fi

# Optional values are deliberately not guessed. The caller/build workflow must
# provide a compatible SDK and a real XNU machine/kernel configuration.
export XNU_SDKROOT="${XNU_SDKROOT:-${SDKROOT:-}}"
export XNU_MACHINE_CONFIG="${XNU_MACHINE_CONFIG:-}"
export XNU_KERNEL_CONFIG="${XNU_KERNEL_CONFIG:-DEVELOPMENT}"
