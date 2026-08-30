#!/bin/bash
# Deja el taller de composición listo para usarse desde el primer turno.
#
# El libro se compone con genealogia/taller/, que necesita cinco paquetes de
# Python y un Chromium. De esos, solo playwright viene en la imagen; el resto
# los ha ido instalando a mano cada sesión que tocó el libro, y hasta que eso
# ocurre ninguna sonda corre ni el PDF se puede rehacer. Este guion lo resuelve
# antes de que la sesión empiece.
#
# Es idempotente: si ya está todo, no hace nada y termina en un segundo.
set -euo pipefail

# Solo en el entorno remoto: en una máquina propia, quien instala decide.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
REQ="$RAIZ/genealogia/taller/requisitos.txt"
[ -f "$REQ" ] || exit 0

# Se comprueba antes de instalar: el contenedor se cachea tras el hook, así que
# en los arranques siguientes esto sale por aquí sin tocar la red.
if python3 - <<'PY' >/dev/null 2>&1
import importlib.util as u, sys
sys.exit(0 if all(u.find_spec(m) for m in
    ("playwright", "pypdfium2", "pikepdf", "fontTools", "brotli")) else 1)
PY
then
  echo "taller: las dependencias de Python ya están"
else
  echo "taller: instalando dependencias de Python…"
  python3 -m pip install --quiet --disable-pip-version-check -r "$REQ"
fi

# El navegador: la imagen ya trae uno y PLAYWRIGHT_BROWSERS_PATH lo señala.
# Descargarlo de nuevo costaría minutos y cientos de megas para nada.
if compgen -G "${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}/chromium*" >/dev/null 2>&1; then
  echo "taller: chromium ya presente en ${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}"
elif [ -n "${CHROME:-}" ] && [ -x "${CHROME:-}" ]; then
  echo "taller: chromium indicado en \$CHROME"
else
  echo "taller: instalando chromium para playwright…"
  python3 -m playwright install chromium
fi

echo "taller: listo. Se compone con «cd genealogia/taller && python3 libro.py»."
