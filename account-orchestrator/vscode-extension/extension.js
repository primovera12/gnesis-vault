// Account Orchestrator — per-window account binder.
// Each VS Code window runs its own extension-host process, so process.env is per-window.
// On activation (before you start a Claude chat) this sets process.env.CLAUDE_CONFIG_DIR
// to a DISTINCT account from the orchestrator pool (round-robin over the freshest usable
// accounts). The Claude Code extension builds its spawn env from {...process.env}, so the
// chat in this window launches on the chosen account — automatically, no reload per chat.
//
// It does NOT override a folder that already has a CLAUDE_CONFIG_DIR in
// `claudeCode.environmentVariables` (the per-project distribution wins there).
const vscode = require('vscode');
const fs = require('fs');
const os = require('os');
const path = require('path');

function homeReg()   { return path.join(os.homedir(), '.claude-accounts.json'); }
function rrFile()    { return path.join(os.homedir(), '.claude-accounts', 'window-rr.json'); }

function usableDirs() {
  try {
    const data = JSON.parse(fs.readFileSync(homeReg(), 'utf8'));
    return Object.values(data)
      .filter(a => a && (a.status === 'VALID' || a.status === 'IDLE') && a.dir)
      .sort((a, b) => Math.max(a.util_5h || 0, a.util_7d || 0) - Math.max(b.util_5h || 0, b.util_7d || 0))
      .map(a => a.dir);
  } catch (_) { return []; }
}

// round-robin claim so consecutive windows take different accounts
function claimAccount(dirs) {
  if (!dirs.length) return null;
  let n = 0;
  try { n = JSON.parse(fs.readFileSync(rrFile(), 'utf8')).n || 0; } catch (_) {}
  const dir = dirs[n % dirs.length];
  try {
    fs.mkdirSync(path.dirname(rrFile()), { recursive: true });
    fs.writeFileSync(rrFile(), JSON.stringify({ n: n + 1, last: dir }));
  } catch (_) {}
  return dir;
}

function folderAlreadyAssigned() {
  const ev = vscode.workspace.getConfiguration('claudeCode').get('environmentVariables');
  if (Array.isArray(ev)) return ev.some(e => e && e.name === 'CLAUDE_CONFIG_DIR');
  return !!(ev && ev.CLAUDE_CONFIG_DIR);
}

function activate(context) {
  try {
    if (process.env.CLAUDE_CONFIG_DIR) return;          // already bound (launch env)
    if (folderAlreadyAssigned()) return;                // per-project distribution handles it
    const dir = claimAccount(usableDirs());
    if (!dir) return;
    process.env.CLAUDE_CONFIG_DIR = dir;
    const name = path.basename(dir);
    context.subscriptions.push(
      vscode.commands.registerCommand('accountOrchestrator.show', () =>
        vscode.window.showInformationMessage('This window is bound to Claude account dir: ' + name))
    );
    console.log('[account-orchestrator] window bound → ' + dir);
  } catch (e) { console.error('[account-orchestrator]', e); }
}
function deactivate() {}
module.exports = { activate, deactivate };
