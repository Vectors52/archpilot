#!/bin/sh
set -eu

SCRIPT_PATH="$(readlink -f -- "$0")"
PROJECT_DIR="$(dirname -- "$SCRIPT_PATH")"

if [ -x "$PROJECT_DIR/.venv/bin/python" ]; then
    PYTHON="$PROJECT_DIR/.venv/bin/python"
else
    PYTHON="$(command -v python3)"
fi

exec "$PYTHON" "$PROJECT_DIR/app.py" "$@"
