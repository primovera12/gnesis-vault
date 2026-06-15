#!/usr/bin/env bash
# Install the decision-page skill into your Claude Code skills dir.
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/product/decision-page"
mkdir -p "$DEST"
for f in SKILL.md README.md canonical-template-v5.html decision-server.py metadata.json install.sh; do
  [ -f "$SRC/$f" ] && cp "$SRC/$f" "$DEST/$f"
done
echo "✓ decision-page installed to $DEST"
echo "  Trigger with /decision, /decision-page, or ask Claude to 'make a decision sheet'."
