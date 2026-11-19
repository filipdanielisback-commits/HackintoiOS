#!/usr/bin/env bash
# Guarded XNU build entry point. This is not yet a validated HANOIP build recipe.
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck source=xnu-env.sh
source "$SCRIPT_DIR/xnu-env.sh"

usage() {
    cat <<'EOF'
Usage:
  bash xnu-build.sh --print-env
  bash xnu-build.sh --check
  bash xnu-build.sh --dry-run [make arguments...]
  XNU_BUILD_ENABLE=1 bash xnu-build.sh [make arguments...]

Required for a real build:
  XNU_SRC             checked-out public XNU source tree
  XNU_MACHINE_CONFIG  an upstream-supported machine configuration
  XNU_KERNEL_CONFIG   kernel configuration (defaults to DEVELOPMENT)
  XNU_SDKROOT         compatible SDK directory (also accepted as SDKROOT)
  XNU_BUILD_ENABLE=1  explicit opt-in to run make

The default source pin is a Darwin 24.6.0-family candidate, not a confirmed
exact source match for iOS 18.7.12 build 22H390. No HANOIP machine config,
XNU patch, or bootable target is supplied by this script.
EOF
}

die() { printf 'xnu-build: ERROR: %s\n' "$*" >&2; exit 1; }
note() { printf 'xnu-build: %s\n' "$*"; }

check_source() {
    [ -d "$XNU_SRC" ] || die "XNU source tree not found: $XNU_SRC"
    [ -f "$XNU_SRC/Makefile" ] || die "missing top-level Makefile in $XNU_SRC"
    command -v git >/dev/null 2>&1 || die "git is required to verify the source pin"
    local actual
    actual="$(git -C "$XNU_SRC" rev-parse HEAD 2>/dev/null)" ||
        die "XNU_SRC is not a Git checkout"
    [ "$actual" = "$XNU_UPSTREAM_COMMIT" ] ||
        die "source commit mismatch: expected $XNU_UPSTREAM_COMMIT, found $actual"
    note "source commit verified: $actual"
    note "source status: $XNU_SOURCE_STATUS"
}

check_build_inputs() {
    check_source
    [ -n "$XNU_MACHINE_CONFIG" ] ||
        die "set XNU_MACHINE_CONFIG to a configuration actually supported by this XNU tree"
    [ -n "$XNU_KERNEL_CONFIG" ] ||
        die "set XNU_KERNEL_CONFIG to a supported kernel configuration"
    [ -n "$XNU_SDKROOT" ] || die "set XNU_SDKROOT (or SDKROOT) to a compatible SDK"
    [ -d "$XNU_SDKROOT" ] || die "SDK directory does not exist: $XNU_SDKROOT"
    command -v make >/dev/null 2>&1 || die "make is required"
    command -v clang >/dev/null 2>&1 || die "clang is required on the build host"
}

case "${1:-}" in
    -h|--help)
        usage
        exit 0
        ;;
    --print-env)
        printf 'HACKINTIOS_ROOT=%s\nXNU_SRC=%s\nXNUDEPS=%s\nXNU_UPSTREAM_TAG=%s\nXNU_UPSTREAM_COMMIT=%s\nXNU_SOURCE_STATUS=%s\nXNU_HOST_OS=%s\nXNU_HOST_ARCH=%s\nXNU_TARGET_ARCH=%s\nXNU_SDKROOT=%s\nXNU_MACHINE_CONFIG=%s\nXNU_KERNEL_CONFIG=%s\n' \
            "$HACKINTIOS_ROOT" "$XNU_SRC" "$XNUDEPS" "$XNU_UPSTREAM_TAG" \
            "$XNU_UPSTREAM_COMMIT" "$XNU_SOURCE_STATUS" "$XNU_HOST_OS" \
            "$XNU_HOST_ARCH" "$XNU_TARGET_ARCH" "$XNU_SDKROOT" \
            "$XNU_MACHINE_CONFIG" "$XNU_KERNEL_CONFIG"
        exit 0
        ;;
    --check)
        check_build_inputs
        note "preflight passed; no compilation was performed"
        exit 0
        ;;
    --dry-run)
        shift
        check_build_inputs
        printf 'make -C %q ARCH_CONFIGS=ARM64 MACHINE_CONFIGS=%q KERNEL_CONFIGS=%q SDKROOT=%q' \
            "$XNU_SRC" "$XNU_MACHINE_CONFIG" "$XNU_KERNEL_CONFIG" "$XNU_SDKROOT"
        printf ' %q' "$@"
        printf '\n'
        note "dry run only; no compilation was performed"
        exit 0
        ;;
esac

[ "${XNU_BUILD_ENABLE:-0}" = "1" ] ||
    die "real builds are disabled by default; set XNU_BUILD_ENABLE=1 after reviewing the preflight"
check_build_inputs

note "starting upstream XNU make; this does not imply HANOIP compatibility"
cd "$XNU_SRC"
exec make ARCH_CONFIGS=ARM64 \
    MACHINE_CONFIGS="$XNU_MACHINE_CONFIG" \
    KERNEL_CONFIGS="$XNU_KERNEL_CONFIG" \
    SDKROOT="$XNU_SDKROOT" "$@"
