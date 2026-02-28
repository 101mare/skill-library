#!/usr/bin/env bash
# Install git hooks for the skill-library repo.
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
git -C "$REPO_ROOT" config core.hooksPath scripts/hooks

echo "Git hooks installed (core.hooksPath = scripts/hooks)"
