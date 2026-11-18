#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
OUTPUT_DIR=${1:-"$ROOT_DIR/build/userland"}
CC=${CC:-cc}
CFLAGS=${CFLAGS:--std=c11 -Wall -Wextra -Werror -O2}

mkdir -p "$OUTPUT_DIR"
"$CC" $CFLAGS "$ROOT_DIR/userland/src/hello/main.c" -o "$OUTPUT_DIR/hackintoios-hello"

printf 'Built host smoke test: %s\n' "$OUTPUT_DIR/hackintoios-hello"
