#!/bin/sh
set -eu

PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$BIN_DIR"
ln -sf "$PROJECT_DIR/run.sh" "$BIN_DIR/archpilot"

printf 'ArchPilot launcher installed: %s/archpilot\n' "$BIN_DIR"
printf 'Make sure %s is in your PATH.\n' "$BIN_DIR"
