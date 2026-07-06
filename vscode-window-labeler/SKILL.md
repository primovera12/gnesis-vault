---
name: vscode-window-labeler
description: |
  Give every VS Code window a visible name AND a distinct title-bar color so you
  can tell your projects apart at a glance — even from the taskbar. Two layers:
  (1) a GLOBAL auto-name set once in your VS Code User settings so every window you
  ever open shows its folder name in the title bar, forever, zero per-project work;
  (2) a per-project color + emoji derived deterministically from the folder name,
  stamped into each project's .vscode/settings.json. Safe: it MERGES into existing
  settings, is idempotent, skips projects you already labeled, and has --dry-run.
  Optional systemd/cron/Task-Scheduler timer makes NEW projects get colored
  automatically the moment you open them (VS Code applies it live, no reload).

  Use when:
  - "too many VS Code windows, I can't tell which project is which"
  - "label / color my VS Code windows", "name my editor windows per project"
  - you want every project window color-coded automatically
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
version: "1.0"
type: skill
domain: devops
owner: community
last_updated: 2026-07-06
tier: production
---

# vscode-window-labeler

Too many VS Code windows open and you can't tell which is which? This gives **every**
window a visible name **and** a unique title-bar color, so you can spot any project
at a glance.

## What it does

1. **Global auto-name** — sets one line in your VS Code *User* settings so **every
   window you ever open** (present and future, any folder) shows its folder name in
   the title bar. Zero per-project work, forever.
2. **Per-project color** — stamps a tiny `.vscode/settings.json` into each project
   giving it a color + emoji derived from its name (SHA-1 → stable hue). Same project
   is always the same color; different projects always look different.

Safe by design: it **merges** into your existing settings (never deletes your other
keys), is idempotent, skips projects that already have a `window.title`, and supports
`--dry-run`.

## Install

```bash
curl -fsSL -o vscode-window-labeler.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/vscode-window-labeler.tar.gz
tar xzf vscode-window-labeler.tar.gz && cd vscode-window-labeler && bash install.sh
```

`install.sh` copies the tool to `~/.local/share/vscode-window-labeler/`, optionally
wires a 90-second auto-labeler timer (systemd --user), and does a first pass over a
projects folder you name.

## Usage

```bash
# See what it would do (writes nothing):
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py ~/projects --dry-run

# Do it — point it at the folder that holds your projects:
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py ~/projects

# Nested projects at any depth:
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py --auto ~/work
```

Then in VS Code: `Ctrl/Cmd+Shift+P` → **Reload Window** (or just wait — the timer
applies it live). New projects get the auto-name for free; re-run (or let the timer)
to color them too.

## Options

| Flag            | Meaning                                                    |
|-----------------|------------------------------------------------------------|
| `--depth N`     | levels under each ROOT that are projects (default `1`)     |
| `--auto`        | find real project roots (.git/package.json/…) at any depth |
| `--project DIR` | stamp one exact folder (repeatable)                        |
| `--no-color`    | only turn on global auto-names                             |
| `--no-global`   | only stamp colors                                          |
| `--force`       | re-color projects that already have a title                |
| `--dry-run`     | print the plan, write nothing                              |

See `AUTOMATE.md` for the systemd / cron / Windows Task Scheduler recipes, and
`PROMPT.md` for a copy-paste prompt you can hand to Claude Code.

## Repo

https://github.com/primovera12/gnesis-vault/tree/main/vscode-window-labeler
