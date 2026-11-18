#!/usr/bin/env bash
# Extract the iPhone XR build manifest and its selected OS archive member.
# This does not decrypt or install firmware.
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <iPhone11,8 IPSW> <output-directory>" >&2
    exit 2
fi

IPSW="$(realpath "$1")"
OUT="$2"
if [[ ! -f "$IPSW" ]]; then
    echo "error: IPSW file not found: $IPSW" >&2
    exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
MEMBER_TOOL="$SCRIPT_DIR/ipsw-member.py"
SELECTOR="$SCRIPT_DIR/select-system.py"

mkdir -p "$OUT/metadata" "$OUT/payload"
python3 "$MEMBER_TOOL" extract "$IPSW" BuildManifest.plist \
    --output "$OUT/metadata/BuildManifest.plist"

OS_MEMBER="$(python3 "$SELECTOR" "$OUT/metadata/BuildManifest.plist" --print-path | tail -n 1)"
OS_NAME="$(basename "$OS_MEMBER")"
python3 "$MEMBER_TOOL" extract "$IPSW" "$OS_MEMBER" \
    --output "$OUT/payload/$OS_NAME"

echo "IPSW inspection complete."
echo "Manifest: $OUT/metadata/BuildManifest.plist"
echo "OS archive member: $OUT/payload/$OS_NAME"
echo "Note: the OS image may be encrypted; no decryption or security bypass was attempted."
