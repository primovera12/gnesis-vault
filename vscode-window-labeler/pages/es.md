# VS Code Window Labeler

Asigna a cada ventana de VS Code un nombre visible **y** un color distinto en la barra de título, para que puedas distinguir tus proyectos de un vistazo, incluso desde la barra de tareas.

## Qué hace

- **Auto-nombrado global** — una sola línea en la configuración de usuario de VS Code hace que *cada* ventana que abras muestre el nombre de su carpeta en la barra de título. Configúralo una vez, funciona para siempre, en cualquier proyecto.
- **Color por proyecto** — genera un pequeño archivo `.vscode/settings.json` en cada proyecto con un color y un emoji derivados de su nombre. El mismo proyecto siempre tendrá el mismo color; los proyectos diferentes siempre se verán distintos.

Se integra con tu configuración existente (nunca elimina tus claves), es idempotente, omite los proyectos que ya hayas etiquetado y cuenta con una opción `--dry-run`.

## Instalación

```bash
curl -fsSL -o vscode-window-labeler.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/vscode-window-labeler.tar.gz
tar xzf vscode-window-labeler.tar.gz && cd vscode-window-labeler && bash install.sh
```

## Uso

```bash
# Preview (writes nothing):
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py ~/projects --dry-run

# Apply — point it at the folder that holds your projects:
python3 ~/.local/share/vscode-window-labeler/vscode-window-labeler.py ~/projects
```

Luego, recarga cada ventana de VS Code (`Ctrl/Cmd+Shift+P` → **Reload Window**). ¿Quieres que los nuevos proyectos se coloreen automáticamente? El instalador puede configurar un temporizador de 90 segundos; VS Code aplicará el color en tiempo real, sin necesidad de recargar.

## Pásaselo a Claude Code

Pega esto en una sesión de Claude Code abierta en la carpeta de tus proyectos:

```
I have too many VS Code windows open and can't tell which project is which.
Set my VS Code User settings window.title to "${rootName}  ${separator}  ${activeEditorShort}"
so every window shows its folder name, and for each project folder under ~/projects add a
.vscode/settings.json with a window.title (emoji + NAME) and a workbench.colorCustomizations
titleBar color derived deterministically from the folder name. Merge, don't overwrite my
other keys, and skip projects that already have a window.title.
```

## Repositorio

https://github.com/primovera12/gnesis-vault/tree/main/vscode-window-labeler
