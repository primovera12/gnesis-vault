#!/usr/bin/env bash
# vscode-window-labeler — installer. Idempotent; safe to re-run.
# Installs the labeler, optionally wires a 90s auto-labeler timer (systemd --user),
# and does a first pass over a projects folder you name.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="$HOME/.local/share/vscode-window-labeler"
UNITS="$HOME/.config/systemd/user"
mkdir -p "$APP"

echo "→ installing labeler to $APP"
install -m 755 "$HERE/vscode-window-labeler.py" "$APP/vscode-window-labeler.py"
for f in README.md AUTOMATE.md PROMPT.md; do [ -f "$HERE/$f" ] && cp "$HERE/$f" "$APP/$f"; done

# Where are your projects? (arg 1, or $PROJECTS_DIR, or common defaults)
PROJECTS="${1:-${PROJECTS_DIR:-}}"
if [ -z "$PROJECTS" ]; then
  for d in "$HOME/projects" "$HOME/code" "$HOME/dev" "$HOME/src" "$HOME/work" "$HOME/repos"; do
    [ -d "$d" ] && { PROJECTS="$d"; break; }
  done
fi

if [ -n "$PROJECTS" ] && [ -d "$PROJECTS" ]; then
  echo "→ first pass over $PROJECTS (global auto-name + per-project colors)"
  python3 "$APP/vscode-window-labeler.py" --depth 1 "$PROJECTS" || true
else
  echo "→ no projects folder found; run later with:"
  echo "    python3 $APP/vscode-window-labeler.py /path/to/your/projects"
fi

# Optional: auto-label new projects every 90s via systemd --user (Linux/WSL).
if command -v systemctl >/dev/null 2>&1 && [ -d /run/user/"$(id -u)"/systemd ] 2>/dev/null; then
  read -r -p "→ wire a 90s auto-labeler timer so new projects color themselves? [y/N] " ans || ans=""
  if [ "${ans:-}" = "y" ] || [ "${ans:-}" = "Y" ]; then
    mkdir -p "$UNITS"
    RUN="$APP/run.sh"
    cat > "$RUN" <<EOF
#!/usr/bin/env bash
set -uo pipefail
python3 "$APP/vscode-window-labeler.py" --no-global --depth 1 "${PROJECTS:-$HOME/projects}" >/dev/null 2>&1
exit 0
EOF
    chmod +x "$RUN"
    cat > "$UNITS/vscode-window-labeler.service" <<EOF
[Unit]
Description=Auto-label VS Code windows (name + distinct color per project)
[Service]
Type=oneshot
ExecStart=/usr/bin/env bash $RUN
EOF
    cat > "$UNITS/vscode-window-labeler.timer" <<'EOF'
[Unit]
Description=Run the VS Code window auto-labeler every 90s
[Timer]
OnBootSec=30s
OnUnitActiveSec=90s
Persistent=true
[Install]
WantedBy=timers.target
EOF
    systemctl --user daemon-reload
    systemctl --user enable --now vscode-window-labeler.timer
    loginctl enable-linger "$USER" 2>/dev/null || true
    echo "    timer enabled (every 90s). New projects color themselves; VS Code applies it live."
  fi
fi

echo "✓ done. Reload your VS Code windows (Ctrl/Cmd+Shift+P → 'Reload Window')."
