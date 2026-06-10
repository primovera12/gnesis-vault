# account-orchestrator

Ejecuta muchas cuentas de Claude Code como un solo grupo — uso en vivo por cuenta (5h / 7d /
% por modelo), una cuenta por proyecto, y un cambio automático sin recarga de un chat en
ejecución antes de que llegue al límite.

## Qué hace
- Obtiene la utilización **en vivo** desde el endpoint OAuth usage → un registro de salud
  (VALID / MAXED / EXPIRED / THROTTLED).
- Reparte una cuenta distinta a cada ventana `~/projects/*` (autodescubiertas).
- **Cambia automáticamente** un chat en ejecución a una cuenta más fresca al ~90% — **sin
  recargar la ventana** (el chat vuelve a leer su archivo de credenciales en su siguiente
  mensaje).
- **Reserva** una cuenta sin contención para tareas pesadas probe / research / autopilot.
- Panel HTML con barras de 5h / 7d + marcas de cuentas **MISSING**.

## Instalación
```bash
curl -fsSL -o account-orchestrator.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/account-orchestrator.tar.gz
tar xzf account-orchestrator.tar.gz
cd account-orchestrator
bash install.sh
```
Autentica cada cuenta en su propio directorio de configuración primero (`~/.claude`,
`~/.claude-acct1 … N`): `CLAUDE_CONFIG_DIR=~/.claude-acctN claude /login`.

## Uso
Pega en Claude Code:
> Instala account-orchestrator desde el Gnesis Vault y configúralo para que cada proyecto
> tenga su propia cuenta y los chats en ejecución cambien automáticamente antes del límite.

Luego: `claude-acct-status` (registro) · `claude-acct-dashboard` (HTML) ·
`claude-acct-distribute --apply` (una cuenta por proyecto).

## Fuente
https://github.com/primovera12/gnesis-vault/tree/main/account-orchestrator
