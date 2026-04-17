#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -f "$SCRIPT_DIR/deploy.env" ]]; then
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/deploy.env"
fi

CRON_EXPR="${CRON_EXPR:-*/10 * * * *}"
UPDATE_LOG_FILE="${UPDATE_LOG_FILE:-$SCRIPT_DIR/update.log}"
UPDATE_SCRIPT="$SCRIPT_DIR/update.sh"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_command crontab
require_command bash

mkdir -p "$(dirname "$UPDATE_LOG_FILE")"
touch "$UPDATE_LOG_FILE"

CRON_LINE="$CRON_EXPR /bin/bash $UPDATE_SCRIPT >> $UPDATE_LOG_FILE 2>&1"
TMP_FILE="$(mktemp)"

crontab -l 2>/dev/null | grep -Fv "$UPDATE_SCRIPT" > "$TMP_FILE" || true
printf '%s\n' "$CRON_LINE" >> "$TMP_FILE"
crontab "$TMP_FILE"
rm -f "$TMP_FILE"

echo "Cron job installed for repository: $REPO_ROOT"
echo "Installed entry:"
crontab -l | grep -F "$UPDATE_SCRIPT"
echo "Update log file: $UPDATE_LOG_FILE"