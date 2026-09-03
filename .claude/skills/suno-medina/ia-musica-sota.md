# Estado del arte de la generación musical por IA — referencia extendida

Citado desde §0.B y §0.D del `SKILL.md`. Ese apartado resume lo directamente
accionable para prompting; este archivo desarrolla el fundamento arquitectónico
y el panorama de las alternativas a Suno, para decidir con criterio cuándo una
limitación es del modelo concreto y cuándo es del enfoque generativo en
conjunto. Toda cifra o fecha relativa al litigio y a la Oficina de Derechos de
Autor proviene de lo ya consignado en §0.D del `SKILL.md`; no se repite aquí
sin necesidad. Las afirmaciones arquitectónicas sobre Suno específicamente son
inferidas por el autor a partir de comportamiento observado, no de
documentación técnica publicada por la empresa, que no divulga su
arquitectura interna; hay que tratarlas como hipótesis razonadas, no como
hecho confirmado.

## 1. Dos familias arquitectónicas en generación de audio

**Transformer autorregresivo sobre tokens de códec neuronal:** el audio se
comprime primero a una secuencia discreta de tokens mediante un códec
neuronal (arquitecturas conocidas públicamente de este tipo incluyen
SoundStream y EnCodec), y un modelo de lenguaje autorregresivo genera esa
secuencia token por token, condicionado por texto. Es la familia a la que
§0.B del `SKILL.md` atribuye a Suno, por inferencia del comportamiento
observado (degradación con la duración, coherencia rítmica que decae,
naturaleza secuencial de la generación).

**Modelos de difusión sobre espectrograma o forma de onda:** el audio se
genera por eliminación progresiva de ruido a partir de una representación
continua (espectrograma o forma de onda), condicionado por texto o por otra
señal. Suele producir mejor fidelidad espectral en pasajes cortos y mayor
control composicional cuando el condicionamiento incluye partitura o MIDI,
a costa de un control más débil sobre la coherencia narrativa larga.

La distinción importa para el prompting porque explica por qué ciertos
límites de Suno (forma larga, modulación de tonalidad) son plausiblemente
estructurales de la familia autorregresiva y no defectos de una versión
concreta: cualquier generador de esa familia enfrenta el mismo problema de
acumulación de error a medida que la secuencia de tokens crece.

## 2. Panorama de plataformas (referencia, no recomendación de uso)

| Plataforma | Familia inferida | Fortaleza relativa reportada | Limitación relativa reportada |
|---|---|---|---|
| Suno (v5.5, perfil de esta skill) | Transformer autorregresivo + síntesis vocal | Coherencia de forma-canción con letra y voz | Forma larga, tonalidad exacta, poliritmo |
| Udio | Transformer autorregresivo (litigio conjunto con Suno, §0.D) | Similar a Suno en alcance | Similar a Suno en limitaciones estructurales |
| Google Lyria (familia Gemini) | No confirmado públicamente por esta skill | Cubierto por la skill hermana `lyria-medina`, que trata su prompting específico | Fuera del alcance de este archivo |
| Modelos de difusión de investigación (referencia genérica, sin nombrar producto comercial concreto) | Difusión | Control composicional fino con condicionamiento MIDI | Producción de voz y letra generalmente menos madura que la familia autorregresiva |

Este cuadro es orientativo y puede quedar desactualizado rápidamente: el
sector cambia de mes a mes. No sustituye una comprobación directa de la
documentación vigente de cada plataforma antes de recomendarla para un uso
concreto.

## 3. Por qué el códec neuronal produce los artefactos de §0.B del `SKILL.md`

Un códec neuronal comprime el audio a una tasa de bits mucho menor que el
audio sin comprimir, entrenado para preservar lo perceptualmente relevante
según su función de pérdida. Dos consecuencias directas:

- **Borramiento de agudos:** las frecuencias por encima de unos ocho
  kilohercios contribuyen poco a la función de pérdida perceptual típica de
  estos códecs, así que el modelo tiende a suavizarlas o perderlas.
- **Timbre «acuático»:** la cuantización del códec introduce artefactos
  espectrales característicos, más audibles cuanto más denso es el pasaje
  (más pistas instrumentales compitiendo por la misma capacidad del códec).

Estas dos consecuencias son la base técnica de las mitigaciones ya listadas
en §0.B del `SKILL.md` (tramos cortos, instrumentación limitada, transponer
en DAW en vez de depender del texto): no son trucos empíricos sin fundamento,
sino la respuesta directa a una limitación de compresión.

## 4. Condicionamiento por voz (Voice Profile)

La síntesis vocal de estos sistemas suele apoyarse en un módulo separado de
generación de voz condicionada (el `SKILL.md` señala un linaje con
arquitecturas tipo Bark como hipótesis, no como hecho confirmado por Suno).
Un perfil vocal (`voice-profiles.md`) actúa como condicionamiento adicional
sobre ese módulo, derivado de tomas de referencia. Esto explica por qué la
calidad del perfil depende tanto de la limpieza de las tomas de origen
(§2 de `voice-profiles.md`): el módulo de síntesis aprende tanto los rasgos
deseados como los artefactos presentes en el condicionamiento.

## 5. Watermarking y trazabilidad

SynthID for audio (Google DeepMind) es, a la fecha de redacción del
`SKILL.md`, la iniciativa de marcaje más citada públicamente para contenido
sintético. Su función es forense: permite identificar contenido generado
por sistemas que lo implementen, sin degradar audiblemente la señal. No
consta si Suno lo implementa; si algún día una plataforma lo adopta de
forma obligatoria, cambiaría la conversación sobre atribución de autoría de
§0.D del `SKILL.md`, porque el origen sintético dejaría de depender de una
declaración voluntaria.

## 6. Cómo usar este archivo

Es fundamento explicativo, no una fuente de parámetros de prompting. Las
cifras y reglas operativas (límites de caracteres, sliders, disparadores de
fry) siguen viviendo en el `SKILL.md` y solo ahí, porque son las verificadas
empíricamente contra la generación real. Este archivo sirve para razonar el
porqué cuando una limitación no verificada empíricamente aparece en un caso
nuevo: si es coherente con la arquitectura descrita aquí, es razonable
tratarla como estructural; si no lo es, conviene sospechar primero de la
generación concreta antes de generalizar la limitación.
