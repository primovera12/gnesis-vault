# account-orchestrator

Run many Claude Code accounts as one pool — live per-account usage (5h / 7d / per-model %),
one account per project, and an automatic no-reload switch of a running chat before it hits
the limit.

## What it does
- Pulls **live** utilization from the OAuth usage endpoint → a health registry
  (VALID / MAXED / EXPIRED / THROTTLED).
- Distributes a different account to each `~/projects/*` window (auto-discovered).
- **Auto-switches** a running chat to a fresher account at ~90% — **no window reload** (the
  chat re-reads its credential file on its next message).
- **Reserves** an uncontended account for heavy probe / research / autopilot tasks.
- HTML dashboard with 5h / 7d bars + **MISSING**-account flags.

## Install
```bash
curl -fsSL -o account-orchestrator.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/account-orchestrator.tar.gz
tar xzf account-orchestrator.tar.gz
cd account-orchestrator
bash install.sh
```
Authenticate each account into its own config dir first (`~/.claude`, `~/.claude-acct1 … N`):
`CLAUDE_CONFIG_DIR=~/.claude-acctN claude /login`.

## Usage
Paste into Claude Code:
> Install account-orchestrator from the Gnesis Vault and set it up so each project gets its
> own account and running chats auto-switch before they hit the limit.

Then: `claude-acct-status` (registry) · `claude-acct-dashboard` (HTML) ·
`claude-acct-distribute --apply` (one account per project).

## Source
https://github.com/primovera12/gnesis-vault/tree/main/account-orchestrator
