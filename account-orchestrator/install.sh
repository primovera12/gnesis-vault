#!/usr/bin/env bash
# Account Orchestrator — installer.
# Installs the tools, the heavy-work governor hook, and three systemd-user timers that
# keep your Claude accounts balanced + auto-switched. Idempotent; safe to re-run.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$HOME/.local/bin"; HOOKS="$HOME/.claude/hooks"; UNITS="$HOME/.config/systemd/user"
mkdir -p "$BIN" "$HOOKS" "$UNITS" "$HOME/.claude-accounts"

echo "→ installing tools to $BIN"
for t in "$HERE"/bin/*; do install -m 755 "$t" "$BIN/$(basename "$t")"; echo "    $(basename "$t")"; done

echo "→ installing heavy-work governor hook"
[ -f "$HERE/hooks/heavy-work-governor.sh" ] && install -m 755 "$HERE/hooks/heavy-work-governor.sh" "$HOOKS/heavy-work-governor.sh"
echo "    (wire it in ~/.claude/settings.json PreToolUse if not already — see README)"

echo "→ seeding expected-accounts list (edit with your real emails)"
EXP="$HOME/.claude-accounts/expected.txt"
[ -f "$EXP" ] || cat > "$EXP" <<'E'
# Expected Claude accounts (one email per line). The dashboard shows a MISSING card
# for any of these not authenticated in a credential dir. Replace with your emails.
you@example.com
work@example.com
E

echo "→ wiring systemd-user timers (dashboard 3m · redistribute 30m · autoswap 2m)"
mk_timer(){ # name desc execstart bootsec activesec
  cat > "$UNITS/$1.service" <<S
[Unit]
Description=$2
[Service]
Type=oneshot
Environment=PATH=%h/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=$3
S
  cat > "$UNITS/$1.timer" <<T
[Unit]
Description=$2 (timer)
[Timer]
OnBootSec=$4
OnUnitActiveSec=$5
Persistent=true
[Install]
WantedBy=timers.target
T
}
mk_timer claude-acct-dashboard    "Claude account dashboard refresh" "%h/.local/bin/claude-acct-dashboard" 2min 3min
mk_timer claude-acct-redistribute "Claude account re-distribute across projects" "%h/.local/bin/claude-acct-redistribute" 5min 30min
mk_timer claude-acct-autoswap     "Claude automatic account switch before limits" "%h/.local/bin/claude-acct-autoswap" 2min 2min
systemctl --user daemon-reload 2>/dev/null || true
for u in claude-acct-dashboard claude-acct-redistribute claude-acct-autoswap; do
  systemctl --user enable --now "$u.timer" 2>/dev/null && echo "    ✓ $u.timer" || echo "    (systemd --user unavailable; run the tools by hand or via cron)"
done

cat <<DONE

✅ Installed. Quick start:
   claude-acct-status             # the live board (per-account 5h/7d %)
   claude-acct-dashboard --open   # the HTML dashboard
   claude-acct-distribute --apply # give each ~/projects/* a different account
   claude-best -p "..."           # spawn on the freshest account (autopilots/loops)
Edit ~/.claude-accounts/expected.txt with your real account emails.
Authenticate accounts into ~/.claude-acct1 … ~/.claude-acctN first (see README).
DONE
