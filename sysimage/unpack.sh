#!/usr/bin/env bash
# Extract the iPhone XR build manifest and a selected component from a local IPSW.
# This is archive inspection only: no decryption, restore, or device modification.
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <iPhone11,8 IPSW> <output-directory>" >&2
    exit 2
fi

IPSW="$(realpath "$1")"
if [[ ! -f "$IPSW" ]]; then
    echo "error: IPSW file not found: $IPSW" >&2
    exit 1
fi

mkdir -p "$2"
OUT="$(cd -- "$2" && pwd)"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
MEMBER_TOOL="$SCRIPT_DIR/ipsw-member.py"
SELECTOR="$SCRIPT_DIR/select-system.py"
MANIFEST="$OUT/metadata/BuildManifest.plist"

mkdir -p "$OUT/metadata" "$OUT/payload"
python3 "$MEMBER_TOOL" extract "$IPSW" BuildManifest.plist --output "$MANIFEST"

echo "Available image components:"
python3 "$SELECTOR" "$MANIFEST" --list-components

OS_MEMBER="$(python3 "$SELECTOR" "$MANIFEST" --component OS --print-path)"
OS_NAME="$(basename "$OS_MEMBER")"
python3 "$MEMBER_TOOL" extract "$IPSW" "$OS_MEMBER" --output "$OUT/payload/$OS_NAME"

echo "IPSW archive inspection complete."
echo "Build manifest: $MANIFEST"
echo "Selected OS member: $OUT/payload/$OS_NAME"
echo "The image may be encrypted or otherwise require Apple-specific processing."
