# Convenciones de nombre y metadatos — «In Absentia»

Citado desde §0 y §7 del `SKILL.md`, junto a `album-in-absentia.md`. Cubre el
nombre de archivo y los metadatos de entrega de las doce pistas del álbum;
transcribe el documento «Convenciones de nombre y metadatos», establecido
por el autor el diecisiete de agosto de dos mil veintiséis, con una
discrepancia de numeración señalada en §0 que hay que resolver antes de
nombrar ningún archivo nuevo.

## 0. Discrepancia de numeración — resolver antes de usar este archivo

Este documento (diecisiete de agosto) numera las pistas cinco a diez en un
orden distinto al del «Índice Maestro» (diecinueve de agosto, que se declara
a sí mismo secuencia canónica «con el intercambio 9↔10 aplicado»):

| Título | N.º en este documento | N.º en el índice maestro (`album-in-absentia.md` §1) |
|---|---|---|
| Saint-Germain | 7 | 5 |
| Õdế Odýnẽs | 5 | 6 |
| La Voz del Desierto | 6 | 7 |
| Isis sin Velo | 9 | 8 |
| El Sueño de Avalón | 10 | 9 |
| La Casa de Dulce | 8 | 10 |

El índice maestro es dos días posterior y se autodeclara canónico; este
archivo adopta su numeración para todo lo que sigue (§1, §2) y traduce los
ejemplos del documento original a ella. **Antes de nombrar un archivo real:
confirmar con el autor si ya existen archivos entregados o en curso con la
numeración antigua** (por ejemplo, un `07_Saint-Germain_seed.wav` nombrado
antes del intercambio), porque renombrar un archivo ya distribuido rompe su
trazabilidad.

## 1. Regla fundacional: los diacríticos no viajan

Las recomendaciones de entrega coinciden en que el nombre de archivo no debe
contener espacios, puntuación ni marcas diacríticas, para que sea
universalmente compatible entre sistemas de archivos, servidores de carga y
programas que reimportan el material. Cuatro títulos del fonograma los
llevan y deben transliterarse EN EL NOMBRE DE ARCHIVO, jamás en el metadato
ni en la ficha de distribución, donde el título va con su ortografía
correcta.

| N.º (índice maestro) | Título canónico (metadatos, distribución) | Nombre de archivo (ASCII) |
|---|---|---|
| 1 | Preludio | `01_Preludio` |
| 2 | El Ladrón Fantasma | `02_El-Ladron-Fantasma` |
| 3 | Demian | `03_Demian` |
| 4 | Philémōn | `04_Philemon` |
| 5 | Saint-Germain | `05_Saint-Germain` |
| 6 | Õdế Odýnẽs | `06_Ode-Odynes` |
| 7 | La Voz del Desierto | `07_La-Voz-del-Desierto` |
| 8 | Isis sin Velo | `08_Isis-sin-Velo` |
| 9 | El Sueño de Avalón | `09_El-Sueno-de-Avalon` |
| 10 | La Casa de Dulce | `10_La-Casa-de-Dulce` |
| 11 | La Rueda de la Vida | `11_Rueda-de-la-Vida` |
| 12 | Postludio | `12_Postludio` |

## 2. Patrón de nombre por tipo de archivo

Dos dígitos al frente, porque iTunes y otros reproductores los leen como
número de pista y porque garantizan el orden correcto al listar la carpeta.
Sin BPM ni tonalidad en el nombre: esos datos viven en los metadatos, no en
el nombre, que debe permanecer corto y estable.

| Tipo | Patrón | Ejemplo (con la numeración de §0) |
|---|---|---|
| Semilla de audio | `NN_Titulo_seed.wav` | `05_Saint-Germain_seed.wav` |
| Generación cruda de Suno | `NN_Titulo_gen_AAAAMMDD_N.wav` | `02_El-Ladron-Fantasma_gen_20260818_3.wav` |
| Toma aceptada, sin editar | `NN_Titulo_take.wav` | `03_Demian_take.wav` |
| Máster final entregable | `NN_Titulo.wav` | `03_Demian.wav` |
| Stems | `NN_Titulo_stem_Nombre.wav` | `03_Demian_stem_Vocals.wav` |
| Sesión de Audition | `NN_Titulo.sesx` | `03_Demian.sesx` |

Se prohíben en nombres de archivo: espacios, acentos, eñes, macrones, comas,
puntos adicionales, paréntesis, corchetes, ampersands, emojis y la palabra
«final».

## 2b. Archivos de trabajo del directorio (texto)

Mismo criterio ASCII y mismo prefijo numérico que los archivos de audio,
para que el orden de la carpeta coincida con el orden del álbum y ningún
nombre dependa de un diacrítico.

| Tipo | Patrón | Ejemplo |
|---|---|---|
| Letra vigente | `NN_Titulo_letra_vN_VIGENTE.txt` | `04_Philemon_letra_v4_VIGENTE.txt` |
| Alterno para A/B | `NN_Titulo_tipo_vN_alterno.txt` | `02_El-Ladron-Fantasma_style_v24_alterno.txt` |
| Toma publicada | `NN_Titulo_letra_vN_PUBLICADA.txt` | `03_Demian_letra_v1_PUBLICADA.txt` |
| Style vigente | `NN_Titulo_style_vN_VIGENTE.txt` | `04_Philemon_style_v3_VIGENTE.txt` |
| Exclude vigente | `NN_Titulo_exclude_vN_VIGENTE.txt` | `04_Philemon_exclude_v2_VIGENTE.txt` |
| Versión superada | mismo patrón con `_archivo` | `04_Philemon_style_v2_archivo.txt` |

Tres estados y solo tres: `_VIGENTE` (lo que se usa hoy, uno por elemento),
`_alterno` (la variante conservada para A/B) y `_PUBLICADA` (el texto
efectivamente distribuido, que no se toca jamás aunque la línea de
regeneración avance). Una sola versión por elemento lleva `_VIGENTE` en cada
carpeta. Al promover una nueva, la anterior pasa a `_archivo` en el mismo
acto, nunca se borra.

## 3. Uniformidad técnica del lanzamiento

Todas las pistas de un mismo lanzamiento deben compartir profundidad de
bits, frecuencia de muestreo y número de canales; mezclar dieciséis y
veinticuatro bits, o 44,1 y 48 kHz, dentro de la misma entrega puede
disparar conversiones no deseadas dentro del distribuidor. Fijar un solo par
y no cambiarlo a mitad del álbum. Si hay que reducir profundidad, hacerlo
deliberadamente con dithering en Audition, no dejando que lo resuelva la
plataforma.

## 4. Metadatos en Adobe Audition — qué pestaña sirve para qué

El panel de metadatos de Audition (Ventana > Metadatos) expone cuatro
pestañas, y cada una gobierna un formato distinto. Confundirlas es la causa
habitual de que los datos «no se guarden».

**RIFF** es la pestaña que aplica a los archivos WAV. Es donde deben ir los
datos de los másteres, porque el WAV almacena metadatos como RIFF, no como
ID3.

**ID3** aplica únicamente a MP3. Rellenarla en un WAV no produce error
visible pero el dato no sobrevive a la exportación. La carátula (Album Art)
solo funciona en MP3: en cualquier otro formato el campo aparece atenuado.

**BWF** (Broadcast Wave) permite desplazamiento temporal y metadatos
descriptivos estándar, y requiere guardar en WAV. Es la vía por la que un
ISRC puede quedar incrustado en un WAV, alojado en el fragmento AXML, cosa
que el WAV corriente no admite.

**XMP** ofrece la misma información más la lista extendida común a las
aplicaciones de vídeo de Adobe. El campo Display Title de RIFF corresponde
al campo Title de la sección Dublin Core de XMP.

**Regla operativa crítica:** al guardar o exportar, marcar siempre la
casilla «Include Markers and Other Metadata». Sin ella, todo lo capturado se
pierde.

**Limitación conocida:** Audition no importa ni exporta plantillas de
metadatos, de modo que cada archivo se rellena a mano. La práctica
recomendada por su comunidad es mantener un archivo plantilla con los campos
comunes ya escritos y copiar de él; de ahí la ficha de §5.

## 5. Ficha de metadatos común a las doce pistas (copiar en RIFF/XMP)

Estos campos son idénticos en todo el fonograma y solo cambian los tres
marcados por pista.

- Artist / Author: José Carlos Medina-Rodríguez
- Album: In Absentia
- Album Artist: José Carlos Medina-Rodríguez
- Composer: José Carlos Medina-Rodríguez
- Publisher / Label: Palabra Oculta
- Copyright: ℗ 2026 José Carlos Medina-Rodríguez
- Year: 2026
- Genre: Alternative
- Language: Spanish
- Comment: Producido con asistencia de inteligencia artificial generativa
  (DDEX: AI-assisted)
- **Title** (cambia por pista): título canónico con su ortografía completa
- **Track number** (cambia por pista): 1 a 12, según la numeración de §0
- **ISRC** (cambia por pista): ver `00d-ISRC-UPC-TRACKER.md`, archivo no
  recibido por esta skill; declarado ausente, no inventado

## 6. Advertencia que ahorra trabajo

Para las cargas en WAV hacia distribución, las etiquetas embebidas NO se
usan: todo se introduce a mano en el panel del distribuidor, y la mayoría de
las plataformas ignora los metadatos incrustados. Lo que importa para la
publicación es la exactitud del formulario, no la del archivo. Rellenar los
metadatos en Audition sigue valiendo la pena por archivo propio,
trazabilidad de autoría y prueba de intervención humana
(`legal-distribucion.md` §1), pero no sustituye ni acelera el formulario del
distribuidor.
