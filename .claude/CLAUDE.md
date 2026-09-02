# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Genealogía de la Asociación Psiquiátrica Mexicana, A.C.

Este repositorio publica un libro, no un programa: `genealogia/` contiene el PDF
del volumen del Sexagésimo Aniversario, sus dos flipbooks, el registro de cada
tanda de correcciones y la norma editorial. El taller que lo compone vive en
`genealogia/taller/`, y su `LEEME.md` explica el proceso y sus trampas.

## La regla que no se negocia: capa cero

No se altera **nunca** el texto ajeno. Eso incluye:

- lo que va dentro de una cita atribuida a una persona (los bloques `epi`, `ent`
  y los cuerpos de Testimonio);
- los asientos bibliográficos, con sus títulos, revistas y direcciones;
- el nombre de un autor tal como lo firma en cada publicación, aunque en otra
  parte del libro se escriba distinto.

Corregir ahí no es mejorar el libro: es falsear una fuente. Si algo parece un
error dentro de una cita, se señala en una nota, no se toca el texto.

Antes de confirmar una tanda, lee `docs/git-instructions.md`: qué se verifica
primero, qué se anota en el registro y qué debe decir el mensaje del commit. No se
carga solo; hay que abrirlo.

## Cómo se trabaja

El compilador dirige por tandas. Cada tanda se verifica **midiendo el PDF
construido**, no leyendo el código: `genealogia/taller/sondas/` reúne las
comprobaciones escritas a lo largo del proyecto, y cada una responde una
pregunta concreta sobre el archivo. Al cerrar una tanda se anota en
`genealogia/REGISTRO_DE_CORRECCIONES.md` qué se cambió, cómo se comprobó y qué
quedó declarado sin corregir.

Un dato que no se sostiene con fuente independiente se declara como tal —el
libro tiene apéndices para eso—; no se rellena con lo que parece probable.

## Componer el libro

Instalar dependencias (el hook de arranque ya lo hace solo en el entorno remoto;
en máquina propia hay que ejecutarlo):

```
cd genealogia/taller
pip install -r requisitos.txt
python3 -m playwright install chromium
```

Componer de principio a fin, en este orden exacto — saltarse un paso o
invertirlos es la causa más común de tandas rehechas:

```
python3 libro.py                             # -> pdfs/libro.pdf (Chromium sin ventana)
python3 extraer_texto_pdf.py pdfs/libro.pdf  # pásale la ruta: por omisión toma el PDF ya sellado, no el recién compuesto
python3 build.py
python3 cmp.py                               # integridad: el PDF contra la fuente; el número de diferencias es la señal
python3 sellar_pdf.py                        # metadatos, marcadores, etiquetas de página
python3 sync_flipbooks.py                    # alinea los dos flipbooks al mismo estado
```

No hay suite de pruebas unitarias: las sondas de `genealogia/taller/sondas/`
verifican **midiendo el PDF construido**, cada una responde una pregunta
concreta. Reciben el PDF como argumento; sin él toman el ya publicado en
`genealogia/`. `verificar_toc.py` necesita el PDF ya sellado, porque lee sus
etiquetas de página. Para correr una sola:

```
python3 genealogia/taller/sondas/verificar_toc.py [ruta/al/pdf]
```

Verificar la configuración de Claude Code del propio repositorio (frontmatter
de skills y reglas, hooks referenciados):

```
bash .claude/verificar-configuracion.sh
```

## Arquitectura

**Fuente de verdad única:** `genealogia/taller/assets/*.bin` es un JSON con
`blocks`, `toc` y `anchors`; todo el texto del libro vive ahí y en ningún otro
sitio. No hay fuente LaTeX en este repositorio — ver la nota sobre
`genealogia/norma/` más abajo.

**La composición se reparte en dos capas que hay que mantener sincronizadas a
mano.** `bookstyle_extraido.js` decide tipografías, cuerpos, márgenes y cajas
por tipo de bloque; tiene un gemelo exacto en `assets/*.js`, la copia que corre
dentro de los flipbooks. Editar el estilo en uno sin el otro produce un PDF y
un flipbook que dejan de coincidir, y la diferencia no se nota hasta que
alguien compara página por página.

**`libro.py` pagina midiendo en un Chromium sin ventana:** reparte los bloques
por página, deriva el Contenido de esa paginación y escribe `pdfs/libro.pdf`.
El Contenido ancla por índice de bloque, así que insertar o borrar bloques lo
desancla en silencio — hay que reanclarlo por identidad (buscando el bloque
por su texto, no por su posición) después de cualquier edición estructural;
`sondas/verificar_toc.py` lo comprueba.

**El seguimiento tipográfico tiene techo:** por encima de cierto valor, el
lector de PDF intercala espacios dentro de las palabras y el texto deja de
copiarse y de encontrarse al buscar. El umbral no es fijo — depende del
cuerpo, de si el rótulo lleva dígitos y de si va en versalita —, así que se
mide con `sondas/techo_por_elemento.py`, nunca se supone.

**`genealogia/norma/` documenta un sistema de composición que no está en este
repositorio:** describe fuentes LaTeX (clase `memoir`, XeLaTeX) y scripts
propios (`norma.py`, `diagnostico.py`, `sabotaje.py`, `auditoria.py`) que
exigen diez cláusulas normativas sobre el volumen canónico de 283 páginas.
Ninguno de esos archivos existe aquí: lo que este repositorio compone es una
reconstrucción del contenido a partir del flipbook HTML, a la misma caja
tipográfica, pero no certificada contra esa norma completa —
`genealogia/norma/LEEME.md` explica el alcance exacto de lo que sí y no se
pudo verificar con esos documentos.

## Skills instaladas en este repositorio

`.claude/skills/tanda/` automatiza el ciclo completo de una tanda: aplicar el
parche, recomponer, verificar con las sondas, sellar y publicar. Es la vía
normal para tocar el libro, en vez de correr los pasos de composición a mano.

`.claude/skills/suno-medina/` es un pipeline de prompting para Suno (letra,
style e IA generativa musical) sin ninguna relación con el libro; vive en este
repositorio para uso personal del compilador. Un futuro turno que la vea no
debe confundirla con parte del taller editorial.

## Convenciones de la prosa

Las cifras y los años van con letra en la prosa corrida («mil novecientos
sesenta y seis»). El numeral se conserva donde es correcto: dentro de citas, en
los asientos bibliográficos y en las cajas de datos.
