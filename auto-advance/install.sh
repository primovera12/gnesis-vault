#!/usr/bin/env bash
# auto-advance — installer.
# Copies the claude-auto-advance tool to ~/.local/bin, scaffolds a generic config, and
# prints the StopFailure hook snippet to merge into ~/.claude/settings.json. Idempotent.
#
# Prerequisite: install the `account-orchestrator` skill first — it provides the
# claude-acct-* tools (claude-acct-status / claude-acct-autoswap / claude-acct-restore)
# that this layer drives.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$HOME/.local/bin"
mkdir -p "$BIN"

echo "→ installing claude-auto-advance to $BIN"
install -m 755 "$HERE/bin/claude-auto-advance" "$BIN/claude-auto-advance"

# Warn (don't fail) if the account-orchestrator tools aren't on PATH yet.
for t in claude-acct-status claude-acct-autoswap; do
  command -v "$t" >/dev/null 2>&1 || echo "    ⚠ $t not on PATH — install the 'account-orchestrator' skill first."
done

echo "→ scaffolding config + wiring (idempotent)"
"$BIN/claude-auto-advance" install --bin --hook

cat <<'DONE'

✅ Installed. Next:
   1) Edit ~/.config/claude-auto-advance/config.json (add headless_jobs[] for hands-off autopilot).
   2) Merge the printed StopFailure hook into ~/.claude/settings.json (don't overwrite — merge the array).
   3) Start it:
        claude-auto-advance start            # proactive watch daemon (interactive swap-assist)
        claude-auto-advance run-job <name>   # FULLY-AUTO supervised headless loop
        claude-auto-advance status           # live account health + recent swaps
DONE
