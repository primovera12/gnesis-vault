# Make it fully automatic (new projects get colored on their own)

The **global auto-name** already covers every new window with zero setup.
To also **color** new projects automatically (no re-running by hand), run the
script on a schedule. VS Code applies the new color/name *live* — no reload.

## Linux / WSL (systemd --user)

`~/.config/systemd/user/vscode-window-labeler.service`
```ini
[Unit]
Description=Auto-label VS Code windows (name + distinct color per project)
[Service]
Type=oneshot
ExecStart=/usr/bin/env python3 %h/.local/share/vscode-window-labeler/vscode-window-labeler.py --no-global --depth 1 %h/projects
```

`~/.config/systemd/user/vscode-window-labeler.timer`
```ini
[Unit]
Description=Run the VS Code window auto-labeler every 90s
[Timer]
OnBootSec=30s
OnUnitActiveSec=90s
Persistent=true
[Install]
WantedBy=timers.target
```
Enable:
```bash
mkdir -p ~/.local/share/vscode-window-labeler
cp vscode-window-labeler.py ~/.local/share/vscode-window-labeler/
systemctl --user daemon-reload
systemctl --user enable --now vscode-window-labeler.timer
loginctl enable-linger "$USER"   # survive logout
```

## macOS (cron)

```bash
crontab -l 2>/dev/null | { cat; echo "* * * * * /usr/bin/python3 $HOME/bin/vscode-window-labeler.py --no-global --depth 1 $HOME/projects >/dev/null 2>&1"; } | crontab -
```

## Windows (Task Scheduler, one line in PowerShell)

```powershell
$py = "python"; $script = "$HOME\vscode-window-labeler.py"
schtasks /Create /SC MINUTE /MO 2 /TN "VSCodeWindowLabeler" /TR "$py `"$script`" --no-global --depth 1 `"$HOME\projects`"" /F
```

Change `~/projects` / `$HOME\projects` to wherever your projects live. Add extra
roots by appending them, or use `--auto <root>` to find nested projects at any depth.
