# auto-advance

Rotación + reanudación automática para Claude Code ante límites de uso/sesión. Cuando
ocurre una pausa por límite de uso, cambia tu sesión a la cuenta sana más fresca y —en
bucles headless/autopilot— relanza `claude --continue` para que el trabajo nunca se
detenga. Las sesiones interactivas de VS Code / CLI son solo-cambio por diseño. Se apoya
en `account-orchestrator`.

## Qué hace
- Detecta la pausa por límite de uso y cambia a la cuenta más fresca (tope anti-monocultivo,
  enfriamiento anti-rebote, nunca a una cuenta agotada).
- **Headless / autopilot** (`claude -p`): totalmente automático — cambia **y** relanza
  `claude --continue`.
- **Interactivo**: solo-cambio — el cambio es instantáneo, luego pulsas ↑+Enter para
  continuar en la cuenta nueva. No falseamos una reanudación interactiva sin manos.

## Instalación
```bash
curl -fsSL -o auto-advance.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/auto-advance.tar.gz
tar xzf auto-advance.tar.gz
cd auto-advance
bash install.sh
```
Requiere `jq`, `curl` y las herramientas `claude-acct-*` (de `account-orchestrator`).

## Uso
Pega en Claude Code:
> Instala auto-advance desde el Gnesis Vault y arráncalo para que mi autopilot cambie de
> cuenta automáticamente cuando llegue al límite.

O ejecútalo directamente: `/auto-advance start` · `/auto-advance status` · `/auto-advance stop`.

## Fuente
https://github.com/primovera12/gnesis-vault/tree/main/auto-advance
