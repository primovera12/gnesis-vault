# claude-auto-advance

A multi-account **auto-rotate + auto-resume** layer for Claude Code. When a running
session hits a usage/session limit, it swaps that session's account to the freshest
healthy one and — for headless/autopilot loops — relaunches automatically so work
never stops.

It is a thin orchestration layer on top of the `claude-acct-*` tool family
(`claude-acct-status`, `claude-acct-autoswap`, `claude-acct-restore`), which ship in the
companion **[`account-orchestrator`](../account-orchestrator/)** skill in this vault.
Those tools own account-health discovery, the anti-monoculture cap, anti-flap cooldown,
parking, and restore. `claude-auto-advance` adds the **trigger**, the **headless resume
loop**, and a **control surface**.

> **Prerequisite:** install the **`account-orchestrator`** skill first (it provides the
> `claude-acct-*` tools and the multi-account credential dirs). Then run `bash install.sh`
> here.

---

## TL;DR — what's fully-auto vs swap-only

| Mode | Resume behaviour | Status |
|------|------------------|--------|
| **Headless / autopilot** (`claude -p`, `gsd-autopilot`, CI) | swap creds → relaunch `claude --continue` → keep going | ✅ **FULLY AUTO, hands-off** |
| **Interactive** (VS Code extension, CLI TUI) | swap creds instantly + desktop notify; you press ↑+Enter to continue on the fresh account | ⚠️ **SWAP-ONLY** (hands-free interactive resume is **not** supported by Claude Code — see Verification) |

We do **not** fake hands-free interactive resume. The honest split above is the whole point.

---

## The trigger (precise)

1. **Reactive (authoritative)** — Claude Code's `StopFailure` hook fires with matcher
   `rate_limit` or `overloaded`. That is the documented event Claude Code emits when a
   turn ends because of a usage/rate limit. We wire `claude-auto-advance hook` on those
   two matchers.
2. **Proactive (preventive)** — `/api/oauth/usage` `five_hour.utilization` **or**
   `seven_day.utilization` ≥ `switch_pct` (default 90), read from the
   `claude-acct-status` registry. Swaps **before** the hard stop so work never pauses.
3. **Hard cap** — an account at utilization 100 / status `MAXED` is **never** a swap
   target. We only ever swap **onto** a `VALID`/`IDLE` account at or below
   `fresh_target_pct` (default 70).

---

## Install

Requires `jq`, `curl`, and the `account-orchestrator` skill installed (it provides the
`claude-acct-*` tools on `PATH`).

```bash
# from this skill folder:
bash install.sh
# which runs:  claude-auto-advance install --bin --hook
#   --bin   copy the tool to ~/.local/bin
#   --hook  print the StopFailure hook snippet to merge into ~/.claude/settings.json
```

`install` scaffolds `~/.config/claude-auto-advance/config.json` from
`config.example.json` (never clobbers an existing one). It **prints** the settings.json
hook snippet rather than auto-merging it — `settings.json` is frequently edited by other
tooling, so you merge it yourself.

### Wire the reactive trigger (`~/.claude/settings.json`)

```json
"hooks": {
  "StopFailure": [
    { "matcher": "rate_limit", "hooks": [ { "type": "command", "command": "claude-auto-advance hook" } ] },
    { "matcher": "overloaded", "hooks": [ { "type": "command", "command": "claude-auto-advance hook" } ] }
  ]
}
```

---

## Use

```bash
claude-auto-advance start            # start the proactive watch daemon
claude-auto-advance status           # daemon state + live account health + jobs + recent swaps
claude-auto-advance stop             # stop the daemon

claude-auto-advance run-job NAME     # FULLY-AUTO supervised headless loop for a configured job
claude-auto-advance swap-now [DIR]   # one-shot proactive swap (full sweep, or a single dir)
claude-auto-advance config           # print resolved config + its path

# --dry-run on any subcommand writes nothing and just shows what it would do.
```

### Fully-auto headless example

Register a job in `~/.config/claude-auto-advance/config.json`:

```json
"headless_jobs": [
  {
    "name": "my-autopilot",
    "config_dir": "~/.claude-acct1",
    "project_dir": "~/projects/my-app",
    "relaunch": true,
    "resume_cmd": "claude -p --continue --dangerously-skip-permissions 'continue the task'"
  }
]
```

Then:

```bash
claude-auto-advance run-job my-autopilot
```

`run-job` ensures a non-maxed account before each launch, runs `resume_cmd`, and on a
limit-stop (non-zero exit, or exit-0-but-account-now-maxed) swaps creds and relaunches
`claude --continue` — until the job finishes or `headless_max_retries` is reached.

---

## Configuration

All knobs live in `~/.config/claude-auto-advance/config.json` (generic, **no secrets**;
credentials stay in each `CLAUDE_CONFIG_DIR/.credentials.json`, managed by the
`claude-acct-*` tools). See `config.example.json`. Key fields:

| Field | Default | Meaning |
|-------|---------|---------|
| `interval_seconds` | 60 | proactive daemon sweep interval |
| `switch_pct` | 90 | swap when an account's max(5h,7d) utilization ≥ this |
| `fresh_target_pct` | 70 | only swap **onto** an account at/below this util |
| `max_per_account` | 2 | anti-monoculture: never pile more than N dirs on one account |
| `flap_cooldown_seconds` | 600 | anti-flap: don't re-swap the same dir within this window |
| `headless_max_retries` | 200 | supervised-loop relaunch ceiling |
| `notify` | true | desktop notification on swap (notify-send / Windows toast) |
| `dry_run` | false | global no-op mode |
| `headless_jobs` | `[]` | the fully-auto supervised loops |

---

## Safety

- **Stay-in-your-lane.** Only swaps cred **files** inside your own account pool
  (`~/.claude`, `~/.claude-acct[0-9]*`), and only relaunches **headless jobs you
  registered** in the config. It never inspects, kills, pauses, or relaunches any other
  project's processes.
- **Reversible.** Swapped-out creds are **parked** by `claude-acct-autoswap`; bring them
  back with `claude-acct-restore` once they cool.
- **Logged.** Every swap / hook / resume is appended to
  `~/.local/state/claude-auto-advance/auto-advance.log`.
- **Dry-run.** `--dry-run` (or `"dry_run": true`) writes nothing.

---

## Verification (why interactive is swap-only)

Verified against Claude Code's documented behaviour (2026-06-10):

- **Headless resume — CONFIRMED.** `claude --continue` / `claude --resume <session-id>`
  is a documented, supported way to continue a prior conversation. Session ids are stored
  in `~/.claude/projects/<project>/<session-id>.jsonl` and surfaced in
  `--output-format json` as `session_id`. A wrapper can detect the stop, swap creds, and
  relaunch — hands-off.
- **`StopFailure` hook — CONFIRMED.** Fires when a turn ends due to an API error;
  matchers include `rate_limit` and `overloaded`. It is advisory (cannot block) — perfect
  as a detector. There is **no** "approaching limit" hook, which is why we also poll
  utilization proactively.
- **Interactive hands-free resume — NOT SUPPORTED.** There is no documented hook, IPC,
  signal, or SDK call to re-drive a **running** interactive session, and credentials are
  loaded at process start (no documented mid-session re-read). So for interactive we swap
  instantly + notify and let your next message / a `--continue` restart land on the fresh
  account. We deliberately do **not** claim hands-free interactive resume.
- **Agent SDK.** The Claude Agent SDK exposes `RateLimitEvent` and `resume=<session_id>`,
  so the same swap-then-continue pattern works in-SDK by rotating creds between `query()`
  calls. (Not required by this tool, but the headless model maps directly onto it.)

---

## Files

```
auto-advance/
├── SKILL.md                 # the /auto-advance control-surface skill
├── README.md                # this file
├── install.sh               # installer (tool → ~/.local/bin, prints hook snippet)
├── config.example.json      # generic config template (no secrets)
└── bin/
    └── claude-auto-advance  # the daemon/CLI tool
```
