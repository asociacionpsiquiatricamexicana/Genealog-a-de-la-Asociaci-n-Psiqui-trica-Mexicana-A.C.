---
name: suno-medina
description: >
  Pipeline operativo para construir, depurar y refinar prompts de style y letra
  para Suno v5.5, calibrado al perfil sonoro del Dr. José Carlos Medina-Rodríguez.
  Integra teoría musical práctica (métrica, instrumentación, composición, estilos),
  arquitectura y limitaciones de IA generativa musical, y contexto legal-ético.
  Actívala ante: crear/pulir canciones, letras, style prompts; ajustes de sliders,
  metatags, vocal fry, reverb, weirdness, audio influence; Voice Profile, clonación
  de voz, Suno Studio, stems, MIDI, Custom Models; conocimiento del SOTA de generación
  de música por IA; o preguntas sobre derechos, etiquetado IA, distribución.
---

# Suno v5.5 — Pipeline Medina (v3 — Integración Música + IA Generativa)

Archivos de referencia (opcionales; leer solo cuando la solicitud los toque):

- `referencias/album-in-absentia.md` — álbum «In Absentia»: DNA sonoro, mapa Camelot, doctrina de Excludes, roadmap del corpus
- `referencias/nomenclatura-metadatos.md` — convenciones de nombre de archivo y metadatos de «In Absentia»
- `referencias/mediciones-semillas.md` — banco DSP de las doce semillas del álbum, contrastado contra el índice maestro
- `referencias/checklist-pregeneracion.md` — checklist previa a disparar una generación (distinta de la de §9)
- `referencias/metadatos-distribucion.md` — plantilla de metadatos y divulgación de IA por plataforma
- `referencias/letras/` — las doce letras de «In Absentia», en el estado en que llegaron (VIGENTE o PUBLICADA); no se tocan
- `referencias/produccion-studio.md` — transiciones, instrumentales, mastering, export, Suno Studio
- `referencias/voice-profiles.md` — creación y uso del perfil vocal propio
- `referencias/legal-distribucion.md` — derechos, litigios, distribución
- `teoria-musical-compendio.md` — referencia de métrica, intervalos, escalas, estilos (de investigación)
- `ia-musica-sota.md` — arquitectura de generación, capacidades, limitaciones, contexto legal (de investigación)

**Integridad del paquete (comprobar antes de remitir a un archivo).** Listar el
directorio que contiene este `SKILL.md` y verificar que el archivo exista. Si
falta, NO se reconstruye su contenido de memoria ni se rellena con lo que parece
probable: se declara la ausencia al usuario, se le pide el dato concreto que
hacía falta (por ejemplo, KEY y BPM del mapa Camelot) y se continúa con el
perfil base dejando constancia de la sustitución. Las secciones 0.B, 0.C y 0.D
son el resumen operativo de los dos compendios y bastan para el trabajo
ordinario; los compendios solo añaden profundidad.

---

## 0. Enrutamiento (SIEMPRE primero)

Antes de construir nada, determinar el destino:

| Destino | Perfil de producción que rige |
|---|---|
| **Track del álbum "In Absentia"** | DNA del álbum (`referencias/album-in-absentia.md` §1). KEY y BPM salen del mapa Camelot del índice maestro, NO del template base. Si el archivo falta, pedir al usuario el DNA y la casilla Camelot del track antes de construir nada. |
| **Pieza suelta** | Perfil base (§1 de este archivo) + template §2.3. |

Si no es obvio, preguntar: «¿Es para "In Absentia" o pieza independiente?».
Los dos perfiles son filosofías de mezcla opuestas (seca íntima vs. densa
neo-psicodélica); nunca mezclarlos en un mismo prompt.

---

## 0.B SOTA y limitaciones de Suno v5.5 (IA generativa de música)

**Arquitectura (propietaria, inferida):** Transformer autorregresivo sobre tokens
de códec neuronal (SoundStream o EnCodec) + módulo de síntesis de voz (linaje Bark).
Clases de conditioning: texto (T5/embedding), letra (nota fonética), audio seed,
Voice Profile, melodía/tempo.

**Capacidades reales:**
- Canciones completas con voz y letra hasta ~8 minutos; coherencia rítmica degrada
  con la duración.
- Control de BPM: "X BPM half-time/double-time" → derivación típica ±3 BPM real.
- Control de tonalidad: alto sesgo hacia la inferencia de mood major/minor; raíz
  frecuentemente ignorada → depender de Sounds con key/tempo explícitos o transponer.
- Instrumentación: responde bien a denominaciones concretas (strings, piano, synth pad)
  pero mezclas densas con +5 instrumentos tienden a "papilla" sin separación.
- Stems: separación activable pero post-hoc, calidad variable.

**Artefactos característicos (cuello de botella del códec):**
- Borramiento de altas frecuencias (>8 kHz); transitorios suavizados.
- Timbre "acuático/submarino" en pasajes densos; reverb digital integrado.
- Artefactos vocales: sibilancia excesiva, ocasional autotune perceptible,
  consonantes velares blandas.
- Costuras audibles en "extend" (extensión de generación existente).
- Convergencia a la media de la distribución de entrenamiento: poca "novedad" armónica.

**Límites reconocidos:**
- Forma larga: estructura y narrativa musical colapsable en >5 minutos.
- Edición fina: imposible editar una pista individual dentro de la mezcla.
- Modulación cromática: disonancias y tritono rara vez convincentes.
- Poliritmo: heterorritmo (3:2 hemiola, 5:4) poco fiable; ritmo estable <100 BPM.

**Mitigaciones operativas (Suno Custom Mode):**
- Generar tramos más cortos (2–3 min) y empalmar en DAW.
- No depender de key exacta; transponer después.
- Instrumentación ≤4 elementos principal + texturas; riqueza mediante stacking
  en DAW.
- Render múltiples seeds; clasificar por coherencia rítmica y timbre antes de
  elegir.
- Audio seed + style influence: 55–75%; Voice Profile: 55–75% si se necesita
  reconocimiento de voz.

---

## 0.C Fundamentos musicales para Suno — compendio operativo

**Métrica y ritmo:** Especificar compás y subdivisión acelera la estructura.
Suno responde bien a pautas simples: "4/4, half-time 70 BPM" o "6/8 compound meter,
waltz feel". Hemiola (3:2) y métricas irregulares (5/8, 7/8) tienen baja fiabilidad;
preferir recomposición post-Suno en DAW. El tresillo (corchea punteada + semifusa)
es relatable en swing/jazz; explicitarlo: "swing feel, triplet hi-hat".

**Intervalos y armonía:** Suno capta bien las "texturas" de modo (dórico, mixolidio)
pero no intervalos exactos desde texto. La Picardy third (cambio a relativo mayor
en final en clave menor) es rescatable con: "gradual outro fade with quiet major
resolution". El tritono y disonancias sustentadas fallan; usar armonía consonante
y postprocesar.

**Escala:** La escala pentatónica, blues, y modo menor natural son "seguras". El
cromatismo excesivo se traduce en "fuzzy" armonía si no va acompañado de
instrumentación clara. Para blues, incluir: "twelve-bar blues structure, blue notes,
walking bass".

**Inversiones de acordes y funciones armónicas:** El cambio "I–IV–V–I" o ii-V-I de jazz
es conceptualmente capturado si lo especificas narrativamente: "ii–V–I in jazz
reharmonization" pero sin garantía de inversiones de bajo exactas. Depender de post-edición
en DAW para bajo continuo preciso.

**Modulación:** Cambio de tonalidad en la misma generación: no soportado. Generar por
secciones (verso en Dm, coro en F mayor) y enlazar en DAW con puentes transicionales.

**Forma de canción:** Suno obedece tags estructurales [Verse], [Chorus], [Bridge],
[Outro]. El diagrama [Intro]→[Verse 1]→[Pre-Chorus]→[Chorus]→[Verse 2]→...
es el patrón más predecible (§3.4).

**Instrumentación y timbre (especificación para Suno):**
- Cuerda: "strings", "violin", "cello", "pizzicato" bien diferenciados.
- Viento-madera: "flute", "oboe", "clarinet" atienden al nombre pero con rango impreciso;
  post-transposición recomendada si la altura importa.
- Viento-metal: "trumpet", "trombone", "french horn" reconocidos; timbre brillante pero
  transitorios suavizados por códec.
- Teclado: "piano" (ataque nítido, bueno), "synth pad" (difuso, requiere post-procesado
  para definición).
- Percusión: "drums", "drum kit", "snare", "hi-hat", "crash cymbal" bien; "live drums"
  vs. "programmed" discernible.
- Bajista: "bass", "upright bass" (warm), "electric bass" (punchy); "walking bass"
  explícito en jazz.

Ver §2.4: NO nombres de artistas ni equipos de estudio (Neve, SSL); traducir a descriptores
audibles mediante la tabla Fridmann de `referencias/album-in-absentia.md` §4. Si la tabla
falta, traducir sobre la marcha a descriptores de timbre, dinámica y espacio
(por ejemplo, «tape saturation, soft transients, narrow stereo») y declarar que se
hizo sin la tabla.

**Voz y producción vocal:**
- Range: "countertenor" (head voice agudo, nuestro por defecto). "Tenor", "baritone",
  "alto" mapeables.
- Articulación: "legato", "staccato", "marcato" usables; "legato through phrase
  endings, soft sibilant articulation" para suavidad.
- Vibrato/color: "vibrato" explícito; "breathy" activador de fry (usar "airy falsetto"
  en su lugar).
- Dinámicas: Especificar en style, no entre corchetes: "dynamic range, crescendo into
  chorus".

**Estilos y géneros:** Suno vuelca patrones de entrenamiento. El "indie rock melódico"
es el lugar de menos resistencia para nuestro perfil. La "chamber pop" con orquestación
mínima maximiza claridad. La "neosicodelia oscura" sin lo darkwave (que activa fry;
negative: no darkwave) funciona como amplificador de Weirdness §4.

---

## 0.D Contexto legal-ético de Suno y música con IA (julio 2026)

**Estado del litigio:** RIAA v. Suno (District of Massachusetts, jun 2024) y RIAA v. Udio
(SDNY, jun 2024). Demandas coordinadas por Universal Music Group, Warner Music Group y
Sony Music; ambas empresas admitieron entrenar con grabaciones protegidas y alegan fair use.
Reclamos hasta 150.000 USD por obra por infracción dolosa (17 U.S.C. §504(c)). Estado
procesal exacto a mediados de 2026: sin resolución final; esperar mociones de desestimación,
discovery disputes, posibles enmiendas por DMCA §1202. No se asuma conclusión anticipada.

**Registrabilidad en EE.UU.:** U.S. Copyright Office, "Copyright and Artificial Intelligence"
Parte 2 (ene 2025): **salida puramente generada por IA NO ES REGISTRABLE**. Se requiere
autoría humana sustancial. Los prompts por sí solos no confieren titularidad; debe haber
selección, arreglo, mezcla o modificación humana verificable. Las obras con elementos
humanos (reescritura de letra, arreglo, mastering) pueden protegerse en esa medida.

**Fair use del entrenamiento:** Copyright Office, Parte 3 (prepublicación, may 2025):
**fair use es análisis caso-por-caso**. Expresó escepticismo ante uso comercial masivo
que genera contenido competidor en el mismo mercado = sustitución de mercado = no fair use.
Ambas empresas alegan "transformación", pero la dilución de mercado es un factor negativo.
Resultado: incertidumbre jurídica persistente.

**Jurisdicciones clave:**
- **Japón, Art. 30-4:** permite machine learning sin autorización (salvo competencia
  directa con expresión creativa específica). Vía de entrenamiento "más permisiva".
- **UE, AI Act (Reg. 2024/1689):** obligatoria publicación de "resumen suficientemente
  detallado" de datos de entrenamiento y política de cumplimiento copyright. Respeto a
  opt-out de minería de textos y datos. Compliance requerido.
- **Reino Unido:** consulta "Copyright and AI" (dic 2024) prefiere **excepción TDM con
  opt-out** (similar a UE), fuertemente impugnada por músicos.

**Implicaciones prácticas:**
- **Uso de bajo riesgo:** BGM, demos, asistencia compositiva. Ya utilizable.
- **Uso comercial:** registrabilidad dudosa; riesgo de reclamación de sellos. Alternativa:
  buscar licencia explícita (aún no consolidada; Suno ofrece derechos limitados a
  suscriptores Pro/Max, pero titularidad última incierta). **Recomendación:** no
  depender de Suno para master comercial hasta que licencias estén formalizadas.
- **Documentación humana:** si existe aporte humano (letra reescrita, arreglo, mastering),
  documentarlo explícitamente para reforzar reclamo de autoría.

**CISAC y Watermarking:** Confederación Internacional de Autores y Compositores proyecta
pérdidas sustanciales de ingresos para creadores por música generativa (estudio dic 2024).
Google DeepMind desarrolló **SynthID for audio** para watermarking y trazabilidad de
contenido sintético; futuro probable: watermarking obligatorio para plataformas.

---

## 1. Perfil sonoro base (piezas sueltas)

**Géneros ancla:** indie rock melódico, chamber pop, indie folk, neopsicodelia
oscura. (La estética darkwave/gótica es SOLO visual-temática; en el style prompt
va siempre al negative: `no darkwave`.)

**Carácter emocional:** bittersweet, wistful, "beautiful sadness with some hope";
tristeza aceptada, nunca pathos oscuro.

**Perfil vocal:** countertenor masculino en head voice, close-mic, íntimo,
airy pero limpio (no `breathy`: la propia skill lo marca como activador de fry en §0.C y §2.4), sin chest voice, sin vocal fry, sin aspereza.

**Tonalidad por defecto (solo piezas sueltas):** E menor / E dórico con visitas
a G mayor; Picardy third en el outro.

**Producción:** hi-fi, dry intimate mix, minimal reverb, close recording.

**Idioma:** español. `Spanish lyrics` obligatorio en el style.

---

## 2. Style prompt

### 2.1 Estructura jerárquica (orden estricto)

1. Género + mood → 2. Perfil vocal → 3. Tempo + key + idioma →
4. Instrumentación → 5. Producción → 6. Arquitectura → 7. Negative prompt

### 2.2 Límites (verificados jul 2026)

- Style: **1000 caracteres** — contar siempre antes de entregar.
- Lyrics: **5000 caracteres**; límite práctico de coherencia 40–60 líneas.
- Si el style excede: comprimir instrumentación primero, luego producción.
  Nunca comprimir perfil vocal ni negative.

### 2.3 Template base (variables entre corchetes — rellenar SIEMPRE)

```
[GÉNERO] with [SUBGÉNERO/ESTÉTICA], [MOOD] with some hope.
Close-mic countertenor, pure angelic head voice throughout, smooth legato
falsetto, soft sibilant articulation, layered harmonies.
[BPM] BPM, [KEY], Picardy third on outro. Spanish lyrics.
[INSTRUMENTACIÓN COMPRIMIDA].
Dry intimate mix, minimal reverb, close recording, hi-fi.
Sparse [INSTRUMENTO] intro building from near-silence.
Hook-driven chorus with bittersweet lift, borrowed ♭VII chord warmth.
Gradual outro fade with quiet major resolution.
No darkwave, no drum machine, no vocal fry, no chest voice breaks,
no epic swells, no hall reverb, no room reverb.
```

Para tracks del álbum: usar el DNA de `referencias/album-in-absentia.md` en su lugar.

### 2.4 Reglas críticas

- `whispered` activa fry → usar `soft head voice`. `breathy`+`intimate` juntos
  activan fry → usar `airy falsetto`.
- `gothic romance` activa sufrimiento y fry → `dark romantic visual aesthetic`.
- Nunca `male vocals` a secas → `male countertenor, head voice, airy high register`.
- `crisp falsetto` si el countertenor deriva a voz femenina.
- Género principal SIEMPRE al inicio (Suno pondera el arranque).
- 5–8 tags descriptivos; >10 genera conflicto.
- Eliminar cumplidos vacíos (`professional`, `high-quality`, `amazing`).
- Sin nombres de artistas ni equipo de estudio: traducir a descriptores
  audibles (tabla Fridmann en `referencias/album-in-absentia.md` §4; si falta,
  traducir sobre la marcha y declararlo, como en §0.C).

---

## 3. Letra

### 3.1 Ortotipografía

Delegar en la skill `correccion-medina` antes de insertar metatags.

### 3.2 Metatags — REGLA ÚNICA (resuelve la contradicción v1)

Suno solo obedece fiablemente tags **estructurales, cortos, canónicos, en
inglés, uno por línea**. Los descriptivos largos se cantan como letra o se
ignoran. Por tanto:

- **Estructura:** solo tags canónicos: `[Intro]`, `[Verse]`, `[Pre-Chorus]`,
  `[Chorus]`, `[Bridge]`, `[Breakdown]`, `[Interlude]`, `[Outro]`, `[End]`,
  `[Instrumental Break]`, `[Guitar Solo]`, `[Piano Solo]`, `[Fade Out]`.
- **Delivery y dinámica:** van al campo Style, no a los corchetes.
- **Excepción quirúrgica:** un solo bracket de ≤3 palabras en inglés, solo
  cuando un verso concreto falla de forma repetida:
  `[Soft head voice]`, `[Airy falsetto]`, `[No fry]`, `[Legato]`.
  Asumir el riesgo de que ocasionalmente se cante; vigilar la generación.
- **Prohibidos siempre:** `[Whispered]`, `[Breathy]`, y cualquier bracket
  largo tipo `[Pure falsetto, legato, soft sibilants, intimate]`.

### 3.3 Pronunciación en español

1. `Spanish lyrics` en style; si hay drift: añadir `All lyrics in Spanish,
   no English` al final del style.
2. Separación silábica fonética para palabras que pronuncia mal:
   `Fi le món` en vez de `Philemon`.
3. Hooks y leitmotivs líricos: grafía exactamente idéntica en cada repetición.
4. Línea que se salta → duplicarla entre paréntesis.
5. Preferir versos de arte menor/medio; la métrica larga aumenta errores.

### 3.4 Estructura narrativa

```
[Intro] → [Verse 1] → [Pre-Chorus] → [Chorus] → [Verse 2] → [Pre-Chorus] →
[Chorus] → [Verse 3] → [Breakdown] → [Chorus] (peak) → [Outro] → [End]
```

El pre-chorus es obligatorio: evita el salto abrupto verso→coro.

---

## 4. Sliders — tabla única (unidad: %)

| Tipo de track | Weirdness | Style Infl. | Audio Infl. |
|---|---|---|---|
| Balada íntima / verso estable / mentor | 40–45 | 72–78 | — |
| Clímax, ordalía, nadir atmosférico | 65–80 | ~65 | — |
| Instrumental limpio y disciplinado | 20–40 | 80–90 | — |
| Con referencia de audio entre tracks | según tipo | según tipo | 55–75 |
| Con Voice Profile activa | según tipo | según tipo | 55–75; subir si la voz no se reconoce |

Regla operativa: cambiar UN slider a la vez, comparar secciones cortas,
y **anotar el resultado en el registro** (§8).

---

## 5. Diagnóstico de artefactos

### 5.1 Vocal fry — causas por probabilidad

1. `gothic romance`/`darkwave` en style
2. `[Whispered]` en letra
3. `breathy`+`intimate` juntos
4. Fricativas finales (S, Z, CH, C) con pausa larga

**Intervención por capa (en orden):** style (`legato through phrase endings,
soft sibilant articulation` + negative `no vocal fry, no raspy delivery,
no chest voice breaks`) → bracket quirúrgico ≤3 palabras (§3.2) → buscar
descriptor conflictivo residual (§2.4).

Nota: `no vocal fry` como negative es práctica de esta skill con buen
historial empírico propio, sin confirmación oficial. Mantener mientras
funcione; la vía principal es contra-dirigir con descriptores positivos.

### 5.2 Otros

| Síntoma | Corrección |
|---|---|
| Reverb excesivo | `dry intimate mix, minimal reverb, close recording` + negative `no hall reverb, no room reverb` |
| Tono sufriente | quitar `gothic romance`; `with some hope`; `Picardy third resolution on outro` |
| Transiciones abruptas | `smooth legato transitions`; verificar pre-chorus |
| Suno sheen / metallic shimmer / bleed / timing en rejilla | ver `referencias/produccion-studio.md` §4; si falta, aplicar las mitigaciones de §0.B (tramos cortos, ≤4 elementos, varios seeds) y declararlo |

---

## 6. Tonalidad y tempo — límites reales

- BPM numérico en style: moderadamente fiable, deriva ±3 BPM. Va en style,
  nunca en lyrics.
- **Tonalidad exacta por prompt: NO fiable.** Suno lee el carácter mayor/menor
  como mood e ignora la raíz con frecuencia. Vías reales: (1) Sounds en Create
  mode como semilla con key/tempo explícitos; (2) transponer en DAW.
  **Todo flujo que dependa de una key concreta debe incluir uno de estos pasos.**
- Cambios de tempo dentro de una generación: no soportados. Generar por
  secciones y empalmar en DAW.
- Elementos que sí lee bien: modo dórico, Picardy third, ♭VII prestado,
  transición al relativo mayor.

---

## 7. Flujos por solicitud

**Crear canción nueva:** enrutar (§0) → establecer género/mood/vocal/key/tempo →
style con template §2.3 o DNA del álbum → letra §3.4 con tags canónicos →
sliders §4 → **checklist §9** → entregar style y letra en bloques de código
separados, con el conteo de caracteres del style →
si la key importa: paso de fijación real (§6).

**Pulir style existente:** verificar perfil según destino (§0) → detectar
descriptores conflictivos (§2.4) → checklist §9 → entregar.

**Arreglar letra:** `correccion-medina` → estructura §3.4 → tags canónicos §3.2
→ verificar prohibidos → entregar en bloque de código.

**Persiste fry:** §5.1 por capas.

**Voice Profile / export / distribución / álbum:** leer el archivo de
referencia correspondiente si existe (regla de integridad del paquete); si
falta, decirlo y responder solo con lo que consta en §0.B, §0.D y §4.
Considerar **contexto legal** (§0.D) si la salida será comercializada.

---

## 8. Registro de iteraciones

Mantener en el proyecto un registro mínimo por sesión de generación:

| Fecha | Track | Cambio probado | Resultado (fry sí/no, voz ok, reverb ok) | Decisión |

Sin registro, cada sesión reaprende lo mismo. El registro convierte la
iteración en conocimiento acumulado y alimenta futuras revisiones de esta skill.

**Criterio de aceptación por generación (binario):**
□ sin fry □ head voice sostenida (sin breaks a pecho) □ mezcla seca
□ español sin drift □ estructura respetada (no se saltó secciones)

---

## 9. Checklist previa a la entrega (obligatoria)

```
□ ≤1000 caracteres (contados)
□ Spanish lyrics presente
□ Sin [Whispered] / [Breathy] / brackets largos
□ Sin nombres de artistas ni equipo de estudio
□ Negative prompt presente
□ Género principal encabezando
□ 5–8 tags descriptivos (≤10)
□ KEY/BPM según destino (§0): mapa Camelot si es álbum
□ Sin cumplidos vacíos
□ Si la key importa: paso de fijación real incluido (§6)
□ Si es para distribución: documentación de aporte humano (§0.D)
```

## 10. Notas de entrega

- Style: bloque de código único en inglés, seguido del conteo de caracteres.
- Letra: bloque de código aparte, solo con tags canónicos (§3.2).
- Cambios: tabla de sustituciones (anterior → nuevo).
- Cierre: «¿Generamos y comparamos?» + recordar registro §8.
- **Importante (julio 2026):** si la canción tiene intención comercial, recordar
  el contexto legal §0.D: registrabilidad dudosa sin aporte humano verificable,
  y riesgo de reclamación por derechos. Documentar contribución humana.

---

## REFERENCIAS INTEGRADAS

Esta skill v3 unifica:
1. Pipeline práctico de operación Suno (v1, v2)
2. Compendio de teoría musical aplicable a prompting (`teoria-musical-compendio.md`)
3. SOTA, arquitectura e implicaciones legales de IA generativa de música (`ia-musica-sota.md`)

Fuente de verdad operativa: este `SKILL.md`. Si un compendio y este archivo
discrepan, rige este archivo y se anota la discrepancia para la siguiente revisión.

La evolución esperada es que el usuario consulte esta skill, la teoría musical subyacente
(cuando necesite profundizar en tonalidad, ritmo, instrumentación) y el contexto legal
(cuando genere contenido para distribución comercial o tenga dudas sobre titularidad).
