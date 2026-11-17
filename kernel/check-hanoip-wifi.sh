#!/usr/bin/env bash
# Source-level audit of the HANOIP Qualcomm CLD WLAN driver configuration.
# This does not identify the physical radio or prove runtime Wi-Fi operation.
set -euo pipefail

KERNEL_DIR="${1:?Usage: check-hanoip-wifi.sh /path/to/kernel/source}"
DEFCONFIG="$KERNEL_DIR/arch/arm64/configs/vendor/hanoip_defconfig"
DRIVER_DIR="$KERNEL_DIR/drivers/staging/qcacld-3.0"

for path in "$DEFCONFIG" "$DRIVER_DIR/Kconfig" "$DRIVER_DIR/Makefile"; do
  if [ ! -f "$path" ]; then
    echo "ERROR: expected Wi-Fi source/config file is missing: $path" >&2
    exit 1
  fi
done

grep -Eq '^[[:space:]]*config QCA_CLD_WLAN([[:space:]]|$)' "$DRIVER_DIR/Kconfig"
grep -Eq '^CONFIG_QCA_CLD_WLAN=m$' "$DEFCONFIG"
grep -Fq 'WLAN_SELECT := CONFIG_QCA_CLD_WLAN=m' "$DRIVER_DIR/Makefile"

echo "HANOIP Wi-Fi source audit passed:"
echo "  - Qualcomm CLD WLAN Kconfig entry exists"
echo "  - hanoip_defconfig selects CONFIG_QCA_CLD_WLAN=m"
echo "  - qcacld-3.0 Makefile selects the CLD module"
echo "NOTE: this is a source/configuration check, not a module build, chipset identification, or hardware test."
