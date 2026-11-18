#!/usr/bin/env bash
set -euo pipefail

EFI_APP="${1:-dist/HackintoiOSLoader.efi}"
if [[ ! -f "$EFI_APP" ]]; then
  echo "Missing UEFI application: $EFI_APP" >&2
  exit 2
fi

QEMU_BIN="${QEMU_BIN:-qemu-system-aarch64}"
command -v "$QEMU_BIN" >/dev/null || { echo "qemu-system-aarch64 not found" >&2; exit 2; }

FIRMWARE="${UEFI_FIRMWARE:-}"
if [[ -z "$FIRMWARE" ]]; then
  for candidate in \
    /usr/share/qemu-efi-aarch64/QEMU_EFI.fd \
    /usr/share/AAVMF/AAVMF_CODE.fd \
    /usr/share/edk2/aarch64/QEMU_EFI.fd; do
    if [[ -f "$candidate" ]]; then FIRMWARE="$candidate"; break; fi
  done
fi
if [[ -z "$FIRMWARE" || ! -f "$FIRMWARE" ]]; then
  echo "AArch64 UEFI firmware not found; set UEFI_FIRMWARE." >&2
  exit 2
fi

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/esp/EFI/BOOT"
cp "$EFI_APP" "$WORK/esp/EFI/BOOT/BOOTAA64.EFI"

set +e
timeout 25s "$QEMU_BIN" \
  -machine virt -cpu cortex-a57 -m 1024 \
  -bios "$FIRMWARE" \
  -drive "format=raw,file=fat:rw:$WORK/esp" \
  -nographic -monitor none -no-reboot \
  >"$WORK/console.log" 2>&1
QEMU_STATUS=$?
set -e

cat "$WORK/console.log"
if grep -Fq "This is an experimental AArch64 UEFI app." "$WORK/console.log"; then
  echo "PASS: UEFI firmware launched HackintoiOSLoader.efi in QEMU."
  exit 0
fi

echo "FAIL: expected loader banner was not observed (QEMU exit: $QEMU_STATUS)." >&2
exit 1
