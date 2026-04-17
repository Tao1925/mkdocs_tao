#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [[ -f "$SCRIPT_DIR/deploy.env" ]]; then
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/deploy.env"
fi

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

require_command git
require_command docker

CURRENT_BRANCH="$(git -C "$REPO_ROOT" branch --show-current 2>/dev/null || true)"

DEPLOY_BRANCH="${DEPLOY_BRANCH:-${CURRENT_BRANCH:-main}}"
GIT_REMOTE="${GIT_REMOTE:-origin}"
IMAGE_NAME="${IMAGE_NAME:-mkdocs-tao}"
CONTAINER_NAME="${CONTAINER_NAME:-mkdocs-tao}"
HOST_PORT="${HOST_PORT:-8493}"
CONTAINER_PORT="${CONTAINER_PORT:-80}"

if [[ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]]; then
  echo "Deployment checkout has local changes. Please commit, stash, or re-clone before running update." >&2
  exit 1
fi

echo "Fetching latest code from $GIT_REMOTE/$DEPLOY_BRANCH"
git -C "$REPO_ROOT" fetch "$GIT_REMOTE" "$DEPLOY_BRANCH" --prune

if git -C "$REPO_ROOT" show-ref --verify --quiet "refs/heads/$DEPLOY_BRANCH"; then
  git -C "$REPO_ROOT" checkout "$DEPLOY_BRANCH"
else
  git -C "$REPO_ROOT" checkout -b "$DEPLOY_BRANCH" --track "$GIT_REMOTE/$DEPLOY_BRANCH"
fi

git -C "$REPO_ROOT" pull --ff-only "$GIT_REMOTE" "$DEPLOY_BRANCH"

echo "Building Docker image: ${IMAGE_NAME}:latest"
docker build --pull -f "$SCRIPT_DIR/Dockerfile" -t "${IMAGE_NAME}:latest" "$REPO_ROOT"

if docker ps -a --format '{{.Names}}' | grep -Fxq "$CONTAINER_NAME"; then
  echo "Removing existing container: $CONTAINER_NAME"
  docker rm -f "$CONTAINER_NAME" >/dev/null
fi

echo "Starting container: $CONTAINER_NAME"
docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  "${IMAGE_NAME}:latest" >/dev/null

echo "Update completed successfully. Active container status:"
docker ps --filter "name=^/${CONTAINER_NAME}$"