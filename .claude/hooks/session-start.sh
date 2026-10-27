#!/bin/bash
set -euo pipefail

# Only run in Claude Code on the web
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# psycopg2 is built from source and needs libpq headers
if [ ! -f /usr/include/postgresql/libpq-fe.h ]; then
  apt-get install -y -q libpq-dev >/dev/null 2>&1 \
    || (apt-get update -q >/dev/null && apt-get install -y -q libpq-dev >/dev/null)
fi

[ -x venv/bin/python ] || uv venv --python 3.8 venv
uv pip install --python venv/bin/python --build-constraint build-constraints.txt -r requirements-dev.txt

echo "export VIRTUAL_ENV=$CLAUDE_PROJECT_DIR/venv" >> "${CLAUDE_ENV_FILE:-/dev/null}"
echo "export PATH=$CLAUDE_PROJECT_DIR/venv/bin:\$PATH" >> "${CLAUDE_ENV_FILE:-/dev/null}"
