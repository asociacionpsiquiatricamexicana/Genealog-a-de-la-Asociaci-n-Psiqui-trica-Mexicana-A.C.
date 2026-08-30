---
paths:
  - "genealogia/taller/*.py"
  - "genealogia/taller/sondas/*.py"
---

# Componer y verificar

El orden importa, y está en `genealogia/taller/LEEME.md`:

```
python3 libro.py                       # -> pdfs/libro.pdf
python3 extraer_texto_pdf.py pdfs/libro.pdf
python3 build.py
python3 cmp.py                         # integridad: el PDF contra la fuente
python3 sellar_pdf.py                  # metadatos, marcadores, etiquetas
python3 sync_flipbooks.py
```

**`extraer_texto_pdf.py` toma por omisión el PDF ya sellado, no el recién
compuesto.** Hay que pasarle la ruta. Sin ella se compara contra el anterior y
todo parece correcto cuando no lo es: ya costó una tanda entera de confusión.

## Verificar es medir el archivo, no leer el código

Las sondas responden preguntas concretas sobre el PDF construido —huecos entre
palabras, colas de bloque perdidas, tipografías incrustadas, anclaje del
Contenido, roturas al copiar—. Cuando una sonda da un resultado raro, sospechar
primero del instrumento: en este proyecto, cuatro de seis sondas fallaron la
primera vez por su propia geometría, no por defectos del libro.

`cmp.py` coteja palabra por palabra el texto extraído contra la fuente. Su
número de diferencias es la señal: si sube tras un cambio que debía ser solo
visual, algo se movió que no debía. Las diferencias que persisten son de
extracción —versalitas, direcciones partidas— y están descritas en
`genealogia/REGISTRO_DE_CORRECCIONES.md`.

## No regenerar la hoja de tipografías sin motivo

`fuentes/fuentes.css` lleva las tipografías incrustadas. Volver a pedirlas puede
traer versiones con otras métricas y repaginar el libro entero.
`fetch_fonts.py`, `fetch_griego.py` y `fuentes_griego.py` están para
trazabilidad, no para uso rutinario.
