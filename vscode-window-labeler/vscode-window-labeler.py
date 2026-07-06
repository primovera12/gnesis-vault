#!/usr/bin/env python3
"""
vscode-window-labeler — give every VS Code window a visible name + a distinct
color so you can tell your projects apart at a glance.

Two layers:
  1. GLOBAL auto-name  — one line in your VS Code *User* settings makes EVERY
     window (present and future, any folder you ever open) show its folder name
     in the title bar. Zero per-project work.
  2. PER-PROJECT color — this script stamps a `.vscode/settings.json` into each
     project with a color derived deterministically from the folder name, so the
     same project is always the same color. Re-run anytime to catch new projects.

Safe by design: it MERGES into existing settings (never clobbers your other
keys), is idempotent, and supports --dry-run.

Usage:
    python3 vscode-window-labeler.py [ROOT ...] [options]

    ROOT   one or more folders whose *immediate subfolders* are projects.
           Default: ./ , ~/projects , ~/code , ~/dev , ~/src  (whichever exist)

Options:
    --depth N      how many levels below each ROOT to treat as projects (default 1)
    --project DIR  stamp this exact folder as a single project (repeatable)
    --no-global    skip the global auto-name step (only stamp colors)
    --no-color     skip per-project colors (only set global auto-name)
    --dry-run      show what would change, write nothing
    -h, --help     this help

Examples:
    python3 vscode-window-labeler.py ~/projects
    python3 vscode-window-labeler.py ~/work ~/oss --depth 1
    python3 vscode-window-labeler.py --project ~/repos/my-app
    python3 vscode-window-labeler.py --no-color        # just turn on auto-names
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Emoji palette — one is picked deterministically per project name.
# ---------------------------------------------------------------------------
EMOJIS = [
    "🎯", "🚀", "🔧", "📦", "🧭", "🛰️", "⚙️", "🧪", "🗂️", "📊",
    "🔬", "🧱", "🖥️", "📡", "🛠️", "🧩", "🕹️", "📈", "🔭", "💾",
    "🧠", "⚡", "🔩", "📁", "🌐", "🧰", "🪐", "🔌", "📮", "🗜️",
]

# VS Code title variables we build the per-project title from.
TITLE_TAIL = "  ${separator}  ${activeEditorShort}"
GLOBAL_TITLE = "${rootName}  ${separator}  ${activeEditorShort}"

SKIP_DIR_NAMES = {
    "node_modules", ".git", ".vscode", "dist", "build", "out", "__pycache__",
    ".next", ".next-broken-stale", ".cache", ".venv", "venv", ".idea",
    "coverage", ".turbo", ".claude", ".kit", ".probe",
}

# Files/dirs that mark a folder as a real project root (for --auto discovery).
ROOT_MARKERS = {".git", "package.json", "pyproject.toml", "Cargo.toml",
                "go.mod", "dev_docs"}


# ---------------------------------------------------------------------------
# Color math: folder name -> stable hue -> dark title-bar palette.
# ---------------------------------------------------------------------------
def _hsl_to_hex(h, s, light):
    """h in [0,360), s & light in [0,1] -> #rrggbb"""
    c = (1 - abs(2 * light - 1)) * s
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    m = light - c / 2
    if   h < 60:  r, g, b = c, x, 0
    elif h < 120: r, g, b = x, c, 0
    elif h < 180: r, g, b = 0, c, x
    elif h < 240: r, g, b = 0, x, c
    elif h < 300: r, g, b = x, 0, c
    else:         r, g, b = c, 0, x
    return "#{:02x}{:02x}{:02x}".format(
        round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)
    )


def palette_for(name):
    """Deterministic (emoji, colors) for a project folder name."""
    n = hashlib.sha1(name.encode("utf-8")).hexdigest()
    seed = int(n, 16)
    hue = seed % 360
    return {
        "emoji": EMOJIS[seed % len(EMOJIS)],
        "active_bg":   _hsl_to_hex(hue, 0.52, 0.24),
        "active_fg":   "#ffffff",
        "inactive_bg": _hsl_to_hex(hue, 0.45, 0.16),
        "inactive_fg": _hsl_to_hex(hue, 0.35, 0.72),
    }


# ---------------------------------------------------------------------------
# Tolerant JSON: VS Code settings allow // and /* */ comments + trailing commas.
# ---------------------------------------------------------------------------
def load_jsonc(path):
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # strip block comments, line comments, trailing commas, then retry
    no_block = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    no_line = re.sub(r"(^|[^:])//[^\n]*", r"\1", no_block)
    no_trailing = re.sub(r",(\s*[}\]])", r"\1", no_line)
    try:
        return json.loads(no_trailing)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"could not parse {path}: {e}")


def write_json(path, data, dry):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if dry:
        return
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Stamp one project folder.
# ---------------------------------------------------------------------------
def stamp_project(project_dir, dry, force=False):
    project_dir = Path(project_dir)
    name = project_dir.name
    pal = palette_for(name)
    settings_path = project_dir / ".vscode" / "settings.json"
    data = load_jsonc(settings_path)

    # Respect a label you already set by hand — don't stomp it (unless --force).
    if not force and isinstance(data.get("window.title"), str) and data["window.title"].strip():
        return "kept", name, pal

    data["window.title"] = f"{pal['emoji']} {name.upper()}{TITLE_TAIL}"
    colors = data.get("workbench.colorCustomizations")
    if not isinstance(colors, dict):
        colors = {}
    colors.update({
        "titleBar.activeBackground":   pal["active_bg"],
        "titleBar.activeForeground":   pal["active_fg"],
        "titleBar.inactiveBackground": pal["inactive_bg"],
        "titleBar.inactiveForeground": pal["inactive_fg"],
    })
    data["workbench.colorCustomizations"] = colors

    write_json(settings_path, data, dry)
    return "stamped", name, pal


def is_project(path, depth_dir=False):
    if not path.is_dir():
        return False
    if path.name.startswith(".") or path.name in SKIP_DIR_NAMES:
        return False
    return True


def discover_roots_auto(roots):
    """Walk each ROOT and return real project roots (a dir holding a ROOT_MARKER),
    pruning build/vendor noise and never descending into a root once found."""
    found = []
    for root in roots:
        root = Path(root).expanduser()
        if not _safe_is_dir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            names = set(dirnames) | set(filenames)
            # prune junk so we don't descend into it
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
            # the container ROOT itself is not a project we want — only descendants
            if Path(dirpath) == root:
                continue
            if names & ROOT_MARKERS:
                found.append(Path(dirpath))
                dirnames[:] = []  # stop: this is a project root, don't go deeper
    seen, out = set(), []
    for p in found:
        rp = str(p.resolve())
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


def discover_projects(roots, depth):
    found = []
    for root in roots:
        root = Path(root).expanduser()
        if not root.is_dir():
            continue
        level = [root]
        for _ in range(depth):
            nxt = []
            for d in level:
                for child in sorted(d.iterdir()):
                    if is_project(child):
                        nxt.append(child)
            level = nxt
        found.extend(level)
    # de-dupe, keep order
    seen, out = set(), []
    for p in found:
        rp = str(p.resolve())
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# Global auto-name: set window.title in every VS Code User settings we find.
# ---------------------------------------------------------------------------
def global_settings_targets():
    targets = []
    home = Path.home()

    # Local User settings by OS
    candidates = [
        home / "AppData/Roaming/Code/User/settings.json",                    # Windows
        home / "Library/Application Support/Code/User/settings.json",        # macOS
        home / ".config/Code/User/settings.json",                            # Linux
        home / ".config/Code - Insiders/User/settings.json",                 # Linux Insiders
        home / "AppData/Roaming/Code - Insiders/User/settings.json",         # Win Insiders
    ]
    # WSL: reach the Windows-side User settings too (so Windows-host windows get it)
    win_users = Path("/mnt/c/Users")
    if _safe_is_dir(win_users):
        try:
            for u in win_users.iterdir():
                candidates.append(u / "AppData/Roaming/Code/User/settings.json")
        except OSError:
            pass
    # WSL remote-server machine settings (applies to all WSL-remote windows)
    for srv in [home / ".vscode-server/data/Machine/settings.json",
                home / ".vscode-server-insiders/data/Machine/settings.json"]:
        candidates.append(srv)

    for c in candidates:
        # only touch settings dirs that already exist (a real VS Code install)
        if _safe_is_dir(c.parent):
            targets.append(c)
    return targets


def _safe_is_dir(path):
    try:
        return path.is_dir()
    except OSError:
        return False


def set_global(dry):
    done = []
    for path in global_settings_targets():
        try:
            data = load_jsonc(path)
        except RuntimeError as e:
            print(f"  ! skip {path}: {e}")
            continue
        if data.get("window.title") and "${rootName}" not in data["window.title"] \
                and "${folderName}" not in data["window.title"]:
            # respect an existing custom global title the user set on purpose
            print(f"  = keep existing window.title in {path}")
            continue
        data["window.title"] = GLOBAL_TITLE
        write_json(path, data, dry)
        done.append(str(path))
    return done


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("roots", nargs="*")
    ap.add_argument("--depth", type=int, default=1)
    ap.add_argument("--auto", action="store_true",
                    help="recursively find real project roots (.git/package.json/"
                         "dev_docs/...) at any depth, instead of fixed --depth")
    ap.add_argument("--project", action="append", default=[])
    ap.add_argument("--no-global", action="store_true")
    ap.add_argument("--no-color", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="overwrite projects that already have a window.title")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("-h", "--help", action="store_true")
    args = ap.parse_args()

    if args.help:
        print(__doc__)
        return 0

    dry = args.dry_run
    tag = " (dry-run)" if dry else ""

    if not args.no_global:
        print(f"== Global auto-name{tag} ==")
        done = set_global(dry)
        for d in done:
            print(f"  ✓ window.title -> folder name in {d}")
        if not done:
            print("  (no VS Code User settings found to update)")

    if not args.no_color:
        roots = args.roots
        if not roots and not args.project:
            defaults = ["./", "~/projects", "~/code", "~/dev", "~/src", "~/work", "~/repos"]
            roots = [r for r in defaults if Path(r).expanduser().is_dir()]
        if roots:
            projects = discover_roots_auto(roots) if args.auto else discover_projects(roots, args.depth)
        else:
            projects = []
        for p in args.project:
            pp = Path(p).expanduser()
            if pp.is_dir():
                projects.append(pp)

        print(f"\n== Per-project colors{tag} == ({len(projects)} project(s))")
        n_stamped = n_kept = 0
        for proj in projects:
            status, name, pal = stamp_project(proj, dry, force=args.force)
            if status == "kept":
                n_kept += 1
                print(f"  = {name:<32} (kept existing label)")
            else:
                n_stamped += 1
                print(f"  {pal['emoji']} {name:<32} {pal['active_bg']}")
        print(f"  -> {n_stamped} stamped, {n_kept} kept. (use --force to restamp kept ones)")

    print("\nDone. Reload each VS Code window (Ctrl/Cmd+Shift+P -> 'Reload Window') to see it.")
    if not dry:
        print("New projects opened later already get the auto-name for free; re-run this "
              "script to give them a color too.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
