# The Vault — skills we share

Free, open-source [Claude Code](https://claude.com/claude-code) skills from **Gnesis**.
Browse and one-click-install them at **[gnesis.dev/vault](https://gnesis.dev/vault)**.

This repo is the single source of truth for those skills. Each skill lives in its
own top-level folder. On every push to `main`, CI packages each folder into a
`<skill>.tar.gz` and publishes it to the rolling [**latest**](../../releases/latest)
release — so the download on the Vault is always the newest build, with no site
redeploy.

## Skills

| Skill                                           | What it does                                                                                                                                                               | Download                                                                     |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [`account-orchestrator`](account-orchestrator/) | Run many Claude Code accounts as one pool — live per-account usage, one account per project, and an automatic no-reload switch of a running chat before it hits the limit. | [latest tarball](../../releases/latest/download/account-orchestrator.tar.gz) |

## Install a skill

```bash
# Replace <skill> with the folder name, e.g. account-orchestrator
curl -fsSL -o <skill>.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/<skill>.tar.gz
tar xzf <skill>.tar.gz
cd <skill>
bash install.sh
```

Or grab it from the Vault UI at [gnesis.dev/vault](https://gnesis.dev/vault), which
generates a one-shot install prompt you can paste into Claude Code.

## Add / update a skill

1. Add a folder at the repo root containing at least a `SKILL.md` (plus
   `README.md`, `install.sh`, `bin/`, etc. as needed).
2. Keep it **sanitized** — no personal data. This repo is public; use placeholder
   values (e.g. `you@example.com`), never real emails or hostnames.
3. `git push`. CI repackages everything and refreshes the `latest` release.
   The Vault picks it up automatically.

## License / use

Shared as-is for the community to use and learn from. No warranty.
