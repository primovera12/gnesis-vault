# VS Code Window Labeler 🎨

Too many VS Code windows open and you can't tell which is which? This gives
**every** window a visible name **and** a unique title-bar color, so you can spot
any project at a glance — even from the taskbar.

![before: "Untitled" everywhere → after: named + color-coded]

## What it does

Two layers:

1. **Global auto-name** — sets one line in your VS Code *User* settings so **every
   window you ever open** (present and future, any folder) shows its folder name
   in the title bar. Zero per-project work, forever.

2. **Per-project color** — stamps a tiny `.vscode/settings.json` into each project
   giving it a color + emoji derived from its name. The same project is always the
   same color, and different projects always look different.

Safe: it **merges** into your existing settings (never deletes your other keys),
is idempotent, skips projects you've already labeled by hand, and has `--dry-run`.

## Requirements

- Python 3 (already on macOS/Linux; on Windows install from python.org or the Store)
- VS Code (works with the WSL, SSH, and local versions)

## Use it

```bash
# 1. See what it would do (writes nothing):
python3 vscode-window-labeler.py ~/projects --dry-run

# 2. Do it — point it at the folder that holds your projects:
python3 vscode-window-labeler.py ~/projects

# 3. In VS Code: Ctrl/Cmd+Shift+P -> "Reload Window" on each window.
```

Point it at more than one root if your projects live in several places:

```bash
python3 vscode-window-labeler.py ~/work ~/oss ~/code
```

Stamp a single specific folder:

```bash
python3 vscode-window-labeler.py --project ~/repos/my-app
```

## Options

| Flag            | Meaning                                                        |
|-----------------|----------------------------------------------------------------|
| `--depth N`     | how many levels under each ROOT are projects (default `1`)     |
| `--project DIR` | stamp one exact folder (repeatable)                            |
| `--no-color`    | only turn on global auto-names, skip colors                    |
| `--no-global`   | only stamp colors, don't touch global User settings           |
| `--force`       | re-color projects that already have a `window.title`          |
| `--dry-run`     | print the plan, write nothing                                  |

## New projects later?

They get the **auto-name for free** (that's the global layer). To give a new
project a **color** too, just re-run the script — it only stamps the new ones.

## Undo

- Remove the `window.title` + `workbench.colorCustomizations` lines from a
  project's `.vscode/settings.json` (or delete that file if the script created it).
- Remove `"window.title"` from your VS Code User settings to drop the global names.

## How the colors are chosen

The folder name is hashed (SHA-1) to a stable hue, then rendered as a dark
title-bar background with a white foreground. Deterministic — same name, same
color, on every machine.
