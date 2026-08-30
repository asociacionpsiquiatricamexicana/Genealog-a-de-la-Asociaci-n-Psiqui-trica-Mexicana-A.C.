---
name: tanda
description: Cierra una tanda de correcciones del libro Genealogía APM, de principio a fin — aplicar los cambios sobre la fuente, recomponer el PDF, verificarlo con las sondas, sellarlo, anotarlo en el registro y publicarlo. Úsala siempre que el compilador dicte correcciones al libro, pida recomponer o resellar el PDF, señale una errata de composición, pida verificar el volumen, o encargue publicar una tanda; y también cuando haya que insertar, borrar o retipar bloques, porque el orden de los pasos y la reancla del Contenido son justo lo que se olvida.
---

# Cerrar una tanda del libro

Una tanda es un conjunto de correcciones que se decide, se aplica, se verifica y
se publica **junto**. No es un commit de conveniencia: es la unidad en que este
libro cambia y en que queda constancia de por qué cambió.

El orden de abajo importa. Cada paso existe porque saltárselo ya costó trabajo
rehecho, y los motivos están en `referencia.md`.

## 1. Aplicar

El texto vive en un solo sitio —`genealogia/taller/assets/*.bin`— y se toca con
`scripts/parche.py`, que exige que **cada** reemplazo case exactamente una vez y
aborta entero si alguno no. Un parche que casa donde no debía no se ve hasta que
alguien lee el PDF impreso.

```
python3 .claude/skills/tanda/scripts/parche.py parches.json --ensayo   # comprobar
python3 .claude/skills/tanda/scripts/parche.py parches.json           # aplicar
```

Antes de tocar nada, la capa cero de `.claude/CLAUDE.md`: no se altera texto
ajeno. Si insertas o borras bloques, lee **`referencia.md` § Reanclar el
Contenido** antes de seguir: sus entradas guardan índices, y se rompen en
silencio.

## 2. Recomponer y verificar

```
cd genealogia/taller
python3 libro.py                       # -> pdfs/libro.pdf
python3 extraer_texto_pdf.py pdfs/libro.pdf     # la ruta, siempre
python3 build.py
python3 cmp.py
```

`cmp.py` da un número de diferencias. **Ese número es la señal**: si sube tras
un cambio que debía ser solo visual, algo se movió que no debía; si no se mueve
tras un cambio de composición, la corrección es puramente visual y el contenido
quedó intacto. Anótalo en los dos sentidos.

Luego corre las sondas que correspondan a lo que tocaste —el catálogo, con qué
mide cada una, está en `referencia.md`—. Y mira el PDF: recorta la zona afectada
antes y después. Varias veces en este proyecto la sonda estaba mal y el libro
bien.

## 3. Sellar y publicar

```
python3 sellar_pdf.py
python3 sync_flipbooks.py
```

Copia el PDF sellado y los flipbooks a `genealogia/`, que es lo que el lector
recibe. Anota la tanda en `genealogia/REGISTRO_DE_CORRECCIONES.md`: qué
cambió, **cómo se comprobó** y qué quedó declarado sin corregir. Confirma y
publica según `docs/git-instructions.md`.

## Cuándo no seguir adelante

Si una comprobación sale rara, sospecha primero del instrumento. Si un dato no
se sostiene con fuente independiente, decláralo en el apéndice que corresponda
en vez de rellenarlo con lo probable. Y si una corrección exige tocar una cita,
un asiento bibliográfico o el nombre firmado de un autor, no es una corrección:
es una nota.

## Los otros archivos

- **`referencia.md`** — la estructura del `.bin` y sus tipos de bloque, cómo se
  reancla el Contenido, y el catálogo de sondas. Léelo cuando vayas a tocar
  estructura o no sepas con qué medir.
- **`ejemplos.md`** — tandas reales de este libro, con el parche que se aplicó y
  la comprobación que lo respaldó. Útil para calibrar qué se considera
  verificado aquí.
