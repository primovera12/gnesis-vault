# decision-page

Convierte cualquier momento en que "personas razonables no estarían de acuerdo" en una hoja
de decisión interactiva de un solo clic: un único archivo HTML autónomo, con el sistema de
diseño de Genesis (claro + oscuro). Cada bifurcación muestra su estado actual, tu opinión
honesta y las opciones con una recomendación; quien revisa elige, comenta y envía —
reemplazando un largo hilo de compensaciones respuesta por respuesta.

## Qué hace
- Un archivo HTML autónomo por decisión — sin paso de compilación; para verlo basta un navegador.
- Cada tarjeta de decisión: **Desde** (estado actual) · **Mi opinión** · opciones
  seleccionables con una opción ✓ RECOMENDADA. Una barra inferior fija muestra el progreso,
  un cuadro de comentarios que crece automáticamente, "Aceptar todas las recomendaciones" y
  "Copiar y enviar".
- **Imágenes:** comparación A/B de capturas lado a lado, opciones con imagen a todo el ancho y
  un visor de galería — haz clic para ampliar, luego ‹ › / teclas de flecha / Esc. Ideal para
  comparar diseños.
- Las elecciones persisten en `localStorage`; un servidor local opcional entrega las
  elecciones automáticamente al agente.
- Estilo Genesis: títulos Outfit, cuerpo Inter, tokens exactos ink/paper/sky, temas claro y oscuro.

## Instalación
```bash
curl -fsSL -o decision-page.tar.gz \
  https://github.com/primovera12/gnesis-vault/releases/latest/download/decision-page.tar.gz
tar xzf decision-page.tar.gz
cd decision-page
bash install.sh
```

## Uso
Pega en Claude Code:
> Crea una hoja de decisión para estas bifurcaciones: <enumera tus decisiones>. Usa la
> plantilla decision-page con estilo Genesis y dame el enlace.

O actívala con `/decision`, `/decision-page` o `/alignment-canvas`.

## Fuente
https://github.com/primovera12/gnesis-vault/tree/main/decision-page
