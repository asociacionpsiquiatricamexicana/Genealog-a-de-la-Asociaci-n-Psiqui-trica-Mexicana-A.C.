# Referencia: la fuente, el Contenido y las sondas

## La fuente de verdad

`genealogia/taller/assets/08fffc00-d395-438c-88b0-a0545e4c4793.bin` es un JSON
con tres claves: `blocks` (todo el texto), `toc` (las entradas del Contenido) y
`anchors`. Un bloque tiene un tipo (`t`) y una lista de fragmentos (`parts`);
cada fragmento lleva su texto en `x` y sus marcas: `i` cursiva, `b` negrita,
`sc` versalita, `sup` superíndice, `ls` seguimiento ampliado, `url` dirección,
`br` salto de línea, `cap` capitular.

### Los tipos de bloque, y qué es cada uno

| Tipo                    | Cuántos  | Qué es                                                                                           |
| ----------------------- | -------- | ------------------------------------------------------------------------------------------------ |
| `p`                     | 526      | párrafo de cuerpo                                                                                |
| `rot`                   | 426      | rótulo de subsección (H3); con `kicker`, antetítulo en gris                                      |
| `trow` / `thead`        | 373 / 33 | fila y cabecera de tabla; cada fila es un bloque, para que el paginador pueda partir entre filas |
| `epi`                   | 155      | voz transcrita: **cita atribuida, capa cero**                                                    |
| `note` / `fnote`        | 124 / 36 | nota al final y nota al pie                                                                      |
| `ref`                   | 93       | asiento bibliográfico: **capa cero**                                                             |
| `field`                 | 79       | caja de datos                                                                                    |
| `pb`                    | 59       | salto de página                                                                                  |
| `ent`                   | 45       | nota de encuadre en cursiva: **capa cero**                                                       |
| `anchor`                | 46       | ancla invisible del Contenido                                                                    |
| `rule` / `orn`          | 40 / 1   | filete y ornamento                                                                               |
| `major`                 | 40       | apertura mayor (H1)                                                                              |
| `ficha`                 | 30       | ficha de expresidente (H1)                                                                       |
| `sec`                   | 20       | subtítulo temático (H2)                                                                          |
| `auth` / `attrib`       | 15 / 2   | autoría y atribución                                                                             |
| `sub`                   | 13       | subtítulo menor                                                                                  |
| `plate`                 | 11       | portadilla a sangre                                                                              |
| `fbox`                  | 6        | caja del diagrama de flujo (Apéndice II)                                                         |
| `resumen` / `fclose`    | 4 / 4    | caja de puntos clave y cierre de ficha                                                           |
| `display`               | 3        | página a sangre no-portadilla                                                                    |
| `autotoc`               | 1        | el Contenido, que se rellena solo                                                                |
| `cardStart` / `cardEnd` | 1 / 1    | apertura y cierre de tarjeta                                                                     |

Los invisibles —`anchor`, `pb`, `cardEnd`, `rule`— no pintan nada pero ocupan
índice: cuentan al insertar o borrar.

## Reanclar el Contenido

**Este es el fallo más caro del proyecto.** Las entradas de `toc` guardan el
índice del bloque al que remiten. Al insertar o borrar bloques, esos índices
dejan de apuntar donde creen y el Contenido remite a páginas equivocadas sin
que nada avise. Ya ocurrió: entradas que erraban hasta treinta páginas en los
apéndices, y se descubrió por casualidad.

Después de cualquier inserción o borrado, hay que reanclar **por identidad**:
localizar cada entrada por el texto de su destino, no por su posición anterior.
Dos criterios que la reancla debe respetar, aprendidos a golpes:

- Si el ancla precede a su portadilla, la entrada apunta a la portadilla, no al
  ancla, o el lector cae en la página anterior.
- Portada y contracubierta son casos aparte: remiten a la primera y la última
  página, y no imprimen folio.

Se comprueba con `sondas/verificar_toc.py`, que sigue cada entrada hasta la
página cuyo folio anuncia. Necesita el PDF **ya sellado**, porque lee sus
etiquetas de página.

Y al insertar varios bloques en una pasada, hazlo **de mayor a menor índice**:
insertar en el 100 desplaza el 200, y una lista procesada en orden ascendente
acaba escribiendo en el sitio equivocado.

## Catálogo de sondas

En `genealogia/taller/sondas/`. Todas miden el PDF construido, no el código.

| Sonda                   | Qué responde                                                                                   | Cuándo usarla                        |
| ----------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------ |
| `cierre_pdf.py`         | estado general: páginas, tipografías incrustadas, roturas al copiar, búsquedas                 | al cerrar cualquier tanda            |
| `chk_colas.py`          | si alguna cola de bloque se perdió al paginar                                                  | tras tocar contenido o paginación    |
| `verificar_toc.py`      | si cada entrada del Contenido cae donde anuncia                                                | tras insertar o borrar bloques       |
| `debug_espacios.py`     | huecos anómalos entre palabras, glifo a glifo                                                  | tras tocar justificado o seguimiento |
| `depurar_pdf.py`        | tipografías, páginas sin texto, tipos sin compositor, marcadores, bloques compuestos dos veces | revisión periódica                   |
| `techo_por_elemento.py` | el seguimiento máximo que admite cada rótulo sin romper la copia                               | antes de cambiar `letter-spacing`    |
| `recuperable.py`        | qué se puede reconstruir desde el repositorio y qué no                                         | al tocar el taller                   |

Las que leen el PDF lo reciben como argumento; sin él toman el publicado.

## Trampas del proceso

- `extraer_texto_pdf.py` toma por omisión el PDF **ya sellado**, no el recién
  compuesto. Sin pasarle la ruta se compara contra el anterior y todo parece
  correcto cuando no lo es.
- El módulo de estilo tiene un gemelo en `assets/*.js`, el que viaja en los
  flipbooks. Toda edición de estilo va a los dos.
- No regeneres `fuentes/fuentes.css` sin motivo: otras métricas repaginan el
  libro entero.
