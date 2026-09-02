# Referencias — estado

## Paquete de generación completo para las cuatro pistas sin metatags

A petición expresa del autor («SI PUEDES MODIFICARLAS, NINGUNA ESTA
PUBLICADA, TODAS SON V1»): El Ladrón Fantasma, Õdế Odýnẽs, Isis sin Velo y
La Rueda de la Vida no tenían metatags de Suno (ni estructurales ni de
dirección), a diferencia de las otras ocho pistas. Se les añadió una v3 con
tags estructurales canónicos en inglés y notas de dirección por sección,
compuestas por Claude Code siguiendo el vocabulario ya establecido en las
pistas que sí los traían y la doctrina de Excludes de `album-in-absentia.md`
§3; y se redactó un Style y un Exclude por pista. Verificado por comparación
automática que ninguna palabra de la letra cambió entre v1 y v3, y que los
cuatro Style caben en el límite de 1000 caracteres.

**Segmentación en secciones: inferencia, no transcripción**, salvo en La
Rueda de la Vida, cuya v1 ya traía tags en español (Verso/Estribillo/Puente)
que se tradujeron 1:1. En las otras tres no había ninguna estructura previa;
la división en Verse/Pre-Chorus/Chorus/Bridge se apoyó en las repeticiones
reales del texto donde las hay (Õdế Odýnẽs, Isis sin Velo) y, en El Ladrón
Fantasma —texto corrido sin ningún gancho repetido—, en un solo `[Chorus]`
no repetido que marca el clímax declarativo, sin inventar una repetición
que el texto no tiene.

**Cada Exclude trae una nota explícita** donde debería ir el núcleo de
treinta y dos términos antiglotales y antisibilantes: ese núcleo sigue sin
llegar a esta skill, así que no se rellenó con términos inventados.

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

## Segunda entrega masiva: nueve pistas con contenido nuevo del autor

El autor pegó directamente, con sus propios metatags de Suno ya aplicados
en casi todos los casos, contenido nuevo para nueve de las doce pistas
(Demian, Philémōn, Saint-Germain, Õdế Odýnẽs, La Voz del Desierto —una
corrección de una palabra—, Isis sin Velo, El Sueño de Avalón, La Casa de
Dulce, La Rueda de la Vida y Postludio). Todo se transcribió verbatim, sin
ninguna alteración de Claude Code, siguiendo la convención de versiones
del propio autor: se archivó lo superado (`_archivo`, nunca se borra) y
solo la versión más reciente de cada pista quedó como `_VIGENTE`.

**Elección de «más reciente» como VIGENTE es un default de esta sesión, no
una decisión del autor.** Cinco pistas tienen ahora, archivadas, más de una
concepción o arreglo genuinamente distinto del mismo lugar del álbum, sin
que el autor haya señalado cuál prefiere:

- **Preludio (1):** v2 archivo, cinematográfico (piano, mellotron, drone) —
  frente a v3 vigente, fingerstyle con pájaros de fondo.
- **El Sueño de Avalón (9):** v2 archivo, con tags en inglés — frente a v3
  vigente, con estructura propia en español que diverge después de la
  apertura compartida.
- **La Casa de Dulce (10):** v2 archivo, «Gretel, prende el atanor» — frente
  a v3 vigente, «Nos perdimos, hermana, siguiendo migajas», concepción
  distinta sobre el mismo cuento.
- **La Rueda de la Vida (11):** v2 y v3 archivo (derivados de Claude Code) —
  frente a v4 vigente, arreglo propio del autor sobre el mismo poema base,
  con secciones fusionadas distinto.
- **El Ladrón Fantasma (2):** v2 y v3 archivo (mis derivados sobre el
  texto original) — frente a v4 vigente, recibida en el turno anterior a
  esta entrega y recuperada aquí porque no había quedado guardada. La v4
  trae versos de los dos registros que la v1 declaraba incompatibles
  («quien ose seguirme sentirá su suplicio» junto con «revelar la senda
  que guía a toda sombra perdida»), así que podría ser la resolución del
  autor a esa discrepancia; no se dio por resuelta sin que él lo confirme
  (ver album-in-absentia.md §5).

**Dos incumplimientos de checklist-pregeneracion.md §7, señalados, no
corregidos:** La Casa de Dulce v3 y La Rueda de la Vida v4 usan «falsetto»
y «de-essed» (además de «soft sibilants» en Rueda) en sus notas de
dirección, términos que el propio autor marcó como proscritos o
proscrito-condicionales para el campo Style. Es contenido pegado
directamente por el autor, no una composición de esta skill, así que no se
tocó; hay que revisarlo antes de pegar esos textos en Suno tal cual.

Ninguna de estas nueve pistas tiene todavía Style ni Exclude compuestos
(salvo las cuatro de la primera entrega, cuyos Style/Exclude siguen
vigentes pero pueden no corresponder ya a la letra más reciente si esta
entrega la reemplazó). Pendiente de encargo explícito.

## Revisión de Style/Exclude contra las letras más recientes

Las cuatro pistas con Style/Exclude (02, 06, 08, 11) recibieron después una
letra más reciente (v4 en las cuatro). Se revisó cada Style contra las notas
de dirección que la letra v4 trae incorporadas, cuando las trae:

- **El Ladrón Fantasma:** discrepancia real. El Style v1 describía un
  arreglo noir disperso; la letra v4 trae un arreglo de banda completa
  (bajo fingerstyle, batería de rock a medio tiempo, solo de guitarra,
  clavecín, mellotron). Reescrito como v2; v1 archivado.
- **Isis sin Velo:** discrepancia puntual. El Style v1 decía «Harp»; la
  letra v4 especifica «harpsichord ostinato» en su propia intro —
  instrumentos distintos. Corregido en v2; v1 archivado.
- **La Rueda de la Vida:** discrepancia real y mayor. El Style v1 describía
  un arreglo orquestal (piano de cola, cuerdas, glockenspiel, timbal); la
  letra v4 trae un arreglo de rock indie con guitarra eléctrica y delay de
  cinta. Reescrito como v2; v1 archivado.
- **Õdế Odýnẽs:** sin discrepancia detectable, pero tampoco verificado a
  fondo. La letra v4 no trae ninguna nota de dirección propia (llegó sin
  metatags, ver su propia cabecera), así que no hay con qué contrastar el
  Style instrumento por instrumento; el tema general (vals, clavecín,
  tumbas) sigue siendo coherente con el Style existente. Se dejó sin
  cambios. Si se le añaden metatags a esta letra más adelante, revisar el
  Style contra ellos.

El Exclude de las cuatro pistas no cambió: la bifurcación por pista de
`album-in-absentia.md` §3 depende del género y del contenido temático, no
de la instrumentación concreta, y ninguna letra nueva contradice esas
reglas.
