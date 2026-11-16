#!/usr/bin/env bash
# Build the public hanoip kernel baseline with a HackintoiOS local-version fragment.
# This produces a kernel image and DTBs only; it does not make a boot image.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KERNEL_REPO="https://github.com/motorola-sm6150-devs/android_kernel_motorola_sm6150.git"
KERNEL_BRANCH="lineage-20"
KERNEL_COMMIT="5b04fac0cb2a8311ae69c8644384426e838d91fe"
KERNEL_DIR="${KERNEL_DIR:-$ROOT/.work/hanoip-kernel}"
OUT_DIR="${OUT_DIR:-$ROOT/out/hanoip}"
JOBS="${JOBS:-2}"

if ! command -v clang >/dev/null 2>&1 || ! command -v ld.lld >/dev/null 2>&1; then
  echo "ERROR: Clang and LLD are required. CI installs the pinned LLVM toolchain." >&2
  exit 2
fi

mkdir -p "$(dirname "$KERNEL_DIR")" "$OUT_DIR"

if [ ! -d "$KERNEL_DIR/.git" ]; then
  git clone --depth 1 --branch "$KERNEL_BRANCH" "$KERNEL_REPO" "$KERNEL_DIR"
fi

actual_commit="$(git -C "$KERNEL_DIR" rev-parse HEAD)"
if [ "$actual_commit" != "$KERNEL_COMMIT" ]; then
  echo "ERROR: expected kernel commit $KERNEL_COMMIT, got $actual_commit" >&2
  echo "Update the pinned source revision deliberately after reviewing it." >&2
  exit 3
fi

export ARCH=arm64
# This 4.14 tree needs an explicit Clang target triple; without it Clang
# defaults to the CI host architecture even though ARCH=arm64 is set.
export CC=clang
export CROSS_COMPILE=aarch64-linux-gnu-
export LD=ld.lld
export LLVM=1
export LLVM_IAS=1

make -C "$KERNEL_DIR" O="$OUT_DIR" vendor/hanoip_defconfig
"$KERNEL_DIR/scripts/kconfig/merge_config.sh" -m -O "$OUT_DIR" \
  "$OUT_DIR/.config" "$ROOT/kernel/hackintoiOS.fragment"
make -C "$KERNEL_DIR" O="$OUT_DIR" olddefconfig

grep -q '^CONFIG_LOCALVERSION="-hackintoiOS"$' "$OUT_DIR/.config"

make -C "$KERNEL_DIR" O="$OUT_DIR" -j"$JOBS" Image.gz dtbs

test -s "$OUT_DIR/arch/arm64/boot/Image.gz"
echo "Kernel image built: $OUT_DIR/arch/arm64/boot/Image.gz"
echo "DTB output directory: $OUT_DIR/arch/arm64/boot/dts"
echo "Source commit: $actual_commit"
echo "NOTE: compile output only; not a boot image and not validated on a phone."
