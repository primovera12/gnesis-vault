# VS Code Window Labeler

Give every VS Code window a visible name **and** a distinct title-bar color, so you can tell your projects apart at a glance — even from the taskbar.

## What it does

- **Global auto-name** — one line in your VS Code User settings makes *every* window you ever open show its folder name in the title bar. Set once, works forever, for any project.
- **Per-project color** — stamps a small `.vscode/settings.json` into each project with a color + emoji derived from its name. The same project is always the same color; different projects always look different.

It merges into your existing settings (never deletes your keys), is idempotent, skips projects you already labeled, and has a `--dry-run`.

## Install

```bash
curl -fsSL -o vscode-window-labeler.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/vscode-window-labeler.tar.gz
tar xzf vscode-window-labeler.tar.gz && cd vscode-window-labeler && bash install.sh
```

## Use it

```bash
# Preview (writes nothing):
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py ~/projects --dry-run

# Apply — point it at the folder that holds your projects:
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py ~/projects
```

Then reload each VS Code window (`Ctrl/Cmd+Shift+P` → **Reload Window**). Want new projects to color themselves automatically? The installer can wire a 90-second timer — VS Code applies the color live, no reload.

## Give it to Claude Code

Paste this into a Claude Code session opened in your projects folder:

```
I have too many VS Code windows open and can't tell which project is which.
Set my VS Code User settings window.title to "${rootName}  ${separator}  ${activeEditorShort}"
so every window shows its folder name, and for each project folder under ~/projects add a
.vscode/settings.json with a window.title (emoji + NAME) and a workbench.colorCustomizations
titleBar color derived deterministically from the folder name. Merge, don't overwrite my
other keys, and skip projects that already have a window.title.
```

## Repo

https://github.com/primovera12/gnesis-vault/tree/main/vscode-window-labeler
