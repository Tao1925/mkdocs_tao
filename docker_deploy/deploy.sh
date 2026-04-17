#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -f "$SCRIPT_DIR/deploy.env" ]]; then
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/deploy.env"
fi

HOST_PORT="${HOST_PORT:-8493}"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_command git
require_command docker

if ! git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Current directory is not a Git repository: $REPO_ROOT" >&2
  exit 1
fi

if command -v lsof >/dev/null 2>&1 && lsof -iTCP:"$HOST_PORT" -sTCP:LISTEN -Pn >/dev/null 2>&1; then
  echo "Port $HOST_PORT is already in use. Please free it or change HOST_PORT in deploy.env." >&2
  exit 1
fi

echo "Starting first deployment from: $REPO_ROOT"
"$SCRIPT_DIR/update.sh"
echo "Deployment completed. Visit: http://VM_IP:${HOST_PORT}"