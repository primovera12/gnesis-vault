#!/usr/bin/env bash
# Install the per-window account binder into VS Code (WSL/Remote or local).
set -uo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAME="account-orchestrator-binder-1.0.0"
installed=0
for EXTROOT in "$HOME/.vscode-server/extensions" "$HOME/.vscode/extensions" "$HOME/.cursor-server/extensions"; do
  [ -d "$EXTROOT" ] || continue
  DEST="$EXTROOT/$NAME"
  mkdir -p "$DEST"
  cp "$SRC/extension.js" "$SRC/package.json" "$DEST/"
  echo "  installed → $DEST"
  installed=1
done
[ "$installed" = 0 ] && { echo "  no VS Code extensions dir found (~/.vscode-server/extensions etc.)"; exit 1; }
cat <<DONE

✅ Installed. To activate:
   • Reload VS Code ONCE (Developer: Reload Window) — a one-time step to load the extension.
   • After that, every NEW window auto-binds to a distinct account (round-robin over the
     freshest usable accounts) — no further reloads, fully automatic.
Verify: Command Palette → "Account Orchestrator: Show this window's account".
If a window doesn't pick it up, package as a .vsix:  npx @vscode/vsce package  &&  code --install-extension *.vsix
DONE
