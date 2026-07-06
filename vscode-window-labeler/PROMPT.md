# Give this to your Claude Code

Two ways to use this pack:

## Option A — just run the script (fastest)

```bash
python3 vscode-window-labeler.py ~/projects
```

Then reload each VS Code window. Done.

## Option B — paste this to Claude Code and let it do everything

Copy the block below and paste it into a Claude Code session opened in the folder
that holds your projects. It will set up global window names + per-project colors
for you (it can even write the script itself if this pack isn't handy):

```
I have a lot of VS Code windows open and can't tell which project each one is.
Set up two things for me:

1. GLOBAL auto-name: add "window.title": "${rootName}  ${separator}  ${activeEditorShort}"
   to my VS Code User settings.json (and, if I'm on WSL, also to
   ~/.vscode-server/data/Machine/settings.json) so EVERY window I ever open shows
   its folder name in the title bar automatically. Merge it in — do not remove my
   other settings.

2. PER-PROJECT colors: for each project folder under <PUT YOUR PROJECTS FOLDER HERE>,
   add to that project's .vscode/settings.json:
     - "window.title": "<EMOJI> <PROJECT-NAME-IN-CAPS>  ${separator}  ${activeEditorShort}"
     - "workbench.colorCustomizations" with titleBar.activeBackground /
       activeForeground / inactiveBackground / inactiveForeground.
   Give each project a DIFFERENT color, derived deterministically from its folder
   name (hash the name to a hue -> dark background, white text) so the same project
   is always the same color. MERGE into any existing .vscode/settings.json, never
   overwrite my other keys, and skip projects that already have a window.title.

Do it idempotently and tell me to reload my windows when done. If it's easier,
write a small reusable Python script that does all of the above and run it.
```

Replace `<PUT YOUR PROJECTS FOLDER HERE>` with your actual path (e.g. `~/projects`).
