#!/usr/bin/env bash
# Comprueba que la configuración de Claude Code de este repositorio carga.
#
# Todo lo que revisa aquí falla **en silencio** cuando está mal: un frontmatter
# roto no avisa, un hook cuyo guion no existe deja pasar en vez de bloquear, un
# hooks.json mal colocado se comporta igual que no tener plugin, y una
# importación @archivo a algo inexistente deja al modelo creyendo que ese
# archivo está. Cada comprobación de abajo corresponde a un fallo que este
# proyecto se encontró de verdad.
#
#   ./.claude/verificar-configuracion.sh          # informe
#   ./.claude/verificar-configuracion.sh --breve  # solo lo que falla
set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BREVE=${1:-}
fallos=0
avisos=0

bien() { [ "$BREVE" = "--breve" ] || printf '  \033[32m✓\033[0m %s\n' "$1"; }
mal()  { printf '  \033[31m✗\033[0m %s\n' "$1"; fallos=$((fallos + 1)); }
ojo()  { printf '  \033[33m!\033[0m %s\n' "$1"; avisos=$((avisos + 1)); }
titulo() { [ "$BREVE" = "--breve" ] || printf '\n\033[1m%s\033[0m\n' "$1"; }

# ── frontmatter de habilidades, agentes y reglas ─────────────────────────────
# Un frontmatter que no parsea no detiene la carga: se descartan TODOS sus
# campos y la pieza queda con el nombre de su directorio y una descripción
# tomada de la primera línea del cuerpo. Nada lo advierte.
revisar_frontmatter() {
  local archivo="$1" exigidos="$2"
  python3 - "$archivo" "$exigidos" <<'PY'
import re, sys, yaml
archivo, exigidos = sys.argv[1], sys.argv[2].split(",")
texto = open(archivo, encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
if not m:
    print("sin frontmatter delimitado por --- en la primera línea"); sys.exit(1)
try:
    d = yaml.safe_load(m.group(1)) or {}
except Exception as e:
    print(f"YAML inválido ({e.__class__.__name__}) — se descartarían todos los campos")
    sys.exit(1)
faltan = [k for k in exigidos if k and not d.get(k)]
if faltan:
    print("faltan campos: " + ", ".join(faltan)); sys.exit(1)
sys.exit(0)
PY
}

titulo "Habilidades"
hallada=0
while IFS= read -r f; do
  hallada=1
  rel="${f#"$RAIZ"/}"
  if salida=$(revisar_frontmatter "$f" "name,description"); then
    bien "$rel"
  else
    mal "$rel — $salida"
  fi
done < <(find "$RAIZ/.claude/skills" -name SKILL.md 2>/dev/null)
[ $hallada -eq 0 ] && bien "no hay habilidades en este repositorio"

titulo "Agentes"
hallada=0
while IFS= read -r f; do
  hallada=1
  rel="${f#"$RAIZ"/}"
  if salida=$(revisar_frontmatter "$f" "name,description"); then
    bien "$rel"
  else
    mal "$rel — $salida"
  fi
done < <(find "$RAIZ/.claude/agents" -name '*.md' 2>/dev/null)
[ $hallada -eq 0 ] && bien "no hay agentes en este repositorio"

titulo "Reglas con ámbito"
hallada=0
while IFS= read -r f; do
  hallada=1
  rel="${f#"$RAIZ"/}"
  if salida=$(revisar_frontmatter "$f" "paths"); then
    bien "$rel"
  else
    mal "$rel — $salida"
  fi
done < <(find "$RAIZ/.claude/rules" -name '*.md' 2>/dev/null)
[ $hallada -eq 0 ] && bien "no hay reglas en este repositorio"

# ── guiones invocados por hooks ──────────────────────────────────────────────
# Un hook cuyo comando no existe no falla ni avisa: la llamada sigue adelante.
titulo "Guiones de hooks"
hallada=0
while IFS= read -r s; do
  while IFS= read -r cmd; do
    [ -z "$cmd" ] && continue
    guion=$(printf '%s' "$cmd" | awk '{print $1}' | sed "s#\$CLAUDE_PROJECT_DIR#$RAIZ#; s#\${CLAUDE_PROJECT_DIR}#$RAIZ#")
    case "$guion" in *.sh|*.py) ;; *) continue ;; esac
    hallada=1
    rel="${guion#"$RAIZ"/}"
    if [ ! -f "$guion" ]; then
      mal "$rel — el hook lo invoca y no existe (dejaría pasar sin avisar)"
    elif [ ! -x "$guion" ]; then
      mal "$rel — existe pero no es ejecutable (chmod +x)"
    else
      primera=$(head -1 "$guion")
      if ! printf '%s' "$primera" | grep -q '^#!'; then
        mal "$rel — la línea 1 no es un shebang"
      elif printf '%s' "$primera" | grep -q $'\r'; then
        mal "$rel — el shebang termina en retorno de carro (finales de línea de Windows)"
      elif head -c 3 "$guion" | grep -q $'\xef\xbb\xbf'; then
        mal "$rel — lleva BOM antes del shebang"
      else
        bien "$rel"
      fi
    fi
  done < <(jq -r '.. | objects | select(.type=="command") | .command // empty' "$s" 2>/dev/null)
done < <(find "$RAIZ/.claude" -name 'settings*.json' -o -name 'hooks.json' 2>/dev/null)
[ $hallada -eq 0 ] && bien "ningún hook invoca guiones propios"

# ── importaciones @archivo ───────────────────────────────────────────────────
# Comprobado en este proyecto: @archivo NO trae el contenido al contexto, y si
# además el archivo no existe, deja al modelo infiriendo que sí.
titulo "Importaciones @archivo en la memoria"
hallada=0
while IFS= read -r mem; do
  while IFS= read -r destino; do
    [ -z "$destino" ] && continue
    hallada=1
    if [ -e "$RAIZ/$destino" ]; then
      ojo "@$destino existe, pero su contenido NO se inlinea: la referencia solo nombra el archivo"
    else
      mal "@$destino no existe — el modelo inferirá que sí"
    fi
  done < <(grep -oE '(^|[[:space:]])@[A-Za-z0-9_./-]+' "$mem" 2>/dev/null | tr -d ' @')
done < <(find "$RAIZ/.claude" -name 'CLAUDE.md' -o -name 'CLAUDE.md' -maxdepth 2 2>/dev/null; [ -f "$RAIZ/CLAUDE.md" ] && echo "$RAIZ/CLAUDE.md")
[ $hallada -eq 0 ] && bien "sin importaciones @archivo"

# ── estructura de plugin, si lo hay ──────────────────────────────────────────
titulo "Estructura de plugin"
if [ -d "$RAIZ/.claude-plugin" ]; then
  sobrantes=$(find "$RAIZ/.claude-plugin" -type f ! -name 'plugin.json' ! -name 'marketplace.json' 2>/dev/null)
  if [ -n "$sobrantes" ]; then
    mal ".claude-plugin/ debe contener solo plugin.json — sobra: $(basename "$sobrantes")"
  else
    bien ".claude-plugin/ correcto"
  fi
else
  bien "este repositorio no es un plugin"
fi

# ── resumen ──────────────────────────────────────────────────────────────────
# `${avisos:+...}` se cumple con avisos=0, porque «0» no es cadena vacía: el
# sufijo se decide contando, no por si la variable trae algo.
cola=''
[ "$avisos" -gt 0 ] && cola=" · $avisos aviso(s)"
printf '\n'
if [ $fallos -eq 0 ]; then
  printf '\033[32m%s\033[0m\n' "sin fallos$cola"
  exit 0
fi
printf '\033[31m%s\033[0m\n' "$fallos fallo(s)$cola"
exit 1
