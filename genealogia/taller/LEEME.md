# Taller de composición del volumen *Genealogía*

Aquí está lo que hace falta para volver a componer el libro desde cero. Hasta
esta tanda vivía solo en el entorno efímero de trabajo: el PDF publicado no se
podía regenerar desde el repositorio.

## Qué es cada cosa

**La fuente de verdad del contenido** es `assets/08fffc00-d395-438c-88b0-a0545e4c4793.bin`
—un JSON con `blocks`, `toc` y `anchors`—. Todo el texto del libro está ahí y
en ningún otro sitio. Un bloque tiene un tipo (`t`) y una lista de fragmentos
(`parts`), cada uno con su texto y sus marcas de cursiva, versalita, negrita,
superíndice o dirección.

**La composición** la reparten dos archivos:

- `bookstyle_extraido.js` decide cómo se ve cada bloque: tipografías, cuerpos,
  márgenes, cajas, tablas, portadillas, cubiertas. Tiene un gemelo en
  `assets/a4d0e564-9e95-4331-9b24-990858d9e4e7.js`, que es la copia que viaja
  dentro de los flipbooks. **Toda edición de estilo debe aplicarse a los dos.**
- `libro.py` pagina: mide en un Chromium sin ventana, reparte los bloques por
  páginas, deriva el Contenido de su propia paginación, pone cornisas y folios,
  y escribe `pdfs/libro.pdf`.

`componer.py` guarda las medidas del papel y de la caja. `fuentes/fuentes.css`
lleva las tipografías incrustadas en base64: Lora y Cormorant Garamond para el
latín, y las caras griegas de Gentium Book Plus, que Lora y Cormorant no traen.

## Qué hace falta

```
pip install -r requisitos.txt
python3 -m playwright install chromium
```

El navegador se resuelve solo: se toma de la variable `CHROME` si está definida,
si no del directorio de navegadores de Playwright, y en último término se deja
que Playwright resuelva el suyo.

`sync_flipbooks.py` necesita además la plantilla del flipbook autónomo —el visor
con su código y sus tipografías—, que es un archivo grande y no vive en el
repositorio. Se indica con `FLIPBOOK_SRC`; a falta de ella toma el flipbook ya
publicado en `genealogia/`, que sirve de plantilla de sí mismo.

## Cómo se compone

```
python3 libro.py                       # -> pdfs/libro.pdf
python3 extraer_texto_pdf.py pdfs/libro.pdf
python3 build.py
python3 cmp.py                         # integridad: el PDF contra la fuente
python3 sellar_pdf.py                  # metadatos, marcadores, etiquetas de página
python3 sync_flipbooks.py              # los dos flipbooks, al mismo estado
```

`cmp.py` coteja palabra por palabra el texto extraído del PDF contra los bloques
de la fuente. Las diferencias que quedan son de extracción, no de contenido, y
están descritas en `../REGISTRO_DE_CORRECCIONES.md`.

**Advertencia:** `extraer_texto_pdf.py` toma por omisión el PDF ya sellado, no
el recién compuesto. Hay que pasarle la ruta, o se compara contra el anterior.

## Cuidados que cuestan caro si se olvidan

- **Toda inserción o borrado de bloques desancla el Contenido.** Sus entradas
  guardan índices de bloque; si se mueven, el Contenido remite a páginas
  equivocadas sin avisar. Hay que reanclarlo por identidad después de cada
  edición estructural.
- **No se regenera `fuentes/fuentes.css` sin motivo.** Volver a pedir las
  tipografías puede traer versiones con otras métricas y repaginar el libro
  entero. `fetch_fonts.py`, `fetch_griego.py` y `fuentes_griego.py` —el que
  incorporó la cara griega y midió su `size-adjust`— están aquí por
  trazabilidad, no para uso rutinario.
- **El seguimiento tipográfico tiene techo.** Por encima de cierto valor, el
  lector de PDF intercala espacios dentro de las palabras y el texto deja de
  copiarse y de encontrarse al buscar. El techo no es común: depende del cuerpo,
  de si el rótulo lleva dígitos y de si va en versalita. `sondas/techo_por_elemento.py`
  lo mide.
- **Capa cero:** no se altera el texto dentro de citas atribuidas a una persona,
  ni los asientos bibliográficos, ni el nombre de un autor tal como lo firma en
  su publicación.

## Sondas

`sondas/` reúne las comprobaciones que se han ido escribiendo, cada una sobre el
PDF construido y no sobre el código:

| Sonda | Qué mide |
|---|---|
| `debug_espacios.py` | huecos entre palabras anómalos, glifo a glifo |
| `chk_colas.py` | que ninguna cola de bloque se pierda al paginar |
| `depurar_pdf.py` | tipografías, páginas sin texto, cobertura de tipos de bloque, marcadores, bloques compuestos dos veces |
| `verificar_toc.py` | que cada entrada del Contenido caiga donde anuncia |
| `techo_por_elemento.py` | el seguimiento máximo que admite cada rótulo |
| `techo_plate.py` | lo mismo, solo para el ordinal de portadilla: barre «PRIMERA», «SEGUNDA» y «TERCERA», que ceden a valores distintos |
| `cierre_pdf.py` | estado final: tipografías, roturas al copiar, búsquedas |
| `recuperable.py` | qué se puede recuperar del repositorio y qué no |

Las sondas que leen el PDF lo reciben como argumento; sin él toman el publicado
en `genealogia/`. `verificar_toc.py` necesita el PDF ya sellado, porque lee sus
etiquetas de página.

## Límite declarado

El Chromium de composición no trae diccionario de partición silábica para
español: la justificación se apoya en un silabeador propio incorporado al módulo
de estilo, y alguna línea abierta permanece.
