# Referencias — estado

## Escrito, con el corpus completo del álbum

| Archivo | Contenido |
|---|---|
| `album-in-absentia.md` | índice maestro de las doce pistas, mapa Camelot, doctrina de Excludes, roadmap |
| `nomenclatura-metadatos.md` | convenciones de nombre de archivo y metadatos técnicos (RIFF/ID3/BWF/XMP) |
| `mediciones-semillas.md` | banco DSP de las doce semillas, contrastado contra el índice maestro |
| `checklist-pregeneracion.md` | checklist previa a disparar una generación |
| `metadatos-distribucion.md` | plantilla de metadatos y divulgación de IA por plataforma |
| `letras/` (doce archivos) | las doce letras del álbum, en el estado en que llegaron; no se tocan |
| `produccion-studio.md`, `voice-profiles.md`, `legal-distribucion.md` | referencia técnica general de Suno, no específica del álbum |
| `../teoria-musical-compendio.md`, `../ia-musica-sota.md` | compendios generales |

## Discrepancias — qué se cerró y qué no

Cerradas con evidencia de este paquete: la numeración de pistas (confirmada
por las doce letras entregadas) y la hipótesis ternaria de Philémōn
(reforzada por la medición de semilla). Cerrada por una decisión que ya
tomó el autor, no por esta sesión: la tonalidad de La Casa de Dulce (el
índice maestro eligió La menor 8A pese a ser la medición más débil del
proyecto; no hay dato nuevo que la desplace).

Sin cerrar, y no se fuerza un cierre sin la evidencia que falta:

1. **Duración de «La Voz del Desierto».** Se contaron los versos cantados
   reales del archivo entregado: setenta y siete, no los noventa y nueve que
   supondría una de las dos notas del índice maestro. Ese conteo no confirma
   ninguna de las dos duraciones tal como están escritas.
2. **Rotulación de «Isis sin Velo».** Requiere ver el vídeo publicado
   realmente, para confirmar si comparte el error de la cabecera recuperada.
   Sin acceso a ese vídeo, no hay manera de resolverlo desde aquí.
3. **Doble concepción de «El Ladrón Fantasma».** El autor declara que existe
   una segunda letra completa e incompatible («línea v54–v59») que nunca se
   entregó a esta skill. Elegir entre las dos sin tener el segundo texto
   sería inventar cuál escribió el autor, no decidir entre dos que sí se
   tienen.

## Documentos referidos pero no recibidos por esta skill

El autor confirma que `00b-DECISIONES-PENDIENTES.md`, `00g-RUTA-OPERATIVA-REAL.md`,
`checklist-saneamiento.md` y los documentos «Parte I» y «Parte II» son notas
de trabajo superadas: no hace falta perseguirlas. Su contenido relevante ya
quedó incorporado donde correspondía (la ruta de distribución real en
`metadatos-distribucion.md`; las derogaciones de ficha en
`mediciones-semillas.md` §4).

Sigue activo, porque no es una nota vieja sino un dato operativo que se usa
en cada lanzamiento: `00d-ISRC-UPC-TRACKER.md`. Solo se conoce el ISRC de
Demian (ver `album-in-absentia.md` §1); para cualquier otra pista, declarar
la ausencia y pedir el código al autor en vez de generar uno. Igual con el
núcleo de treinta y dos términos antiglotales de la doctrina de Excludes y
el léxico proscrito §11.1/§11.2 de `checklist-pregeneracion.md`: no son
notas viejas, son listas de trabajo activas que faltan.

## Fuera del alcance de esta skill

`mediciones-semillas.md` §2 documenta un defecto real del estimador de la
skill hermana `analisis-semilla-medina` (cuantización con resolución
decreciente en tempos altos, hasta ±8 BPM por encima de 140). No se corrigió
aquí porque esa skill no formaba parte del encargo; queda anotado para quien
la mantenga.
