# Mediciones de semillas — banco DSP

Citado desde `album-in-absentia.md` §1. Todas las mediciones son de
`analisis-semilla-medina`. La tonalidad es estimada por correlación y el BPM
admite ambigüedad de octava; la semilla es inmutable, el texto se pliega a
ella. El documento fuente («00j-MEDICIONES-SEMILLAS.md») numeraba las pistas
cinco a diez con el orden antiguo, igual que `nomenclatura-metadatos.md`
antes de la reancla; la tabla siguiente ya está traducida a la numeración
del índice maestro (`album-in-absentia.md` §1), que se adopta en todo este
paquete.

## 1. Tabla de medición (traducida a la numeración del índice maestro)

| N.º | Pista | BPM repr. | Medio tiempo | Deriva (σ) | Nitidez | Tonalidad 1.ª | Camelot | r | 2.ª candidata | Entropía |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Preludio | 86,1 | 43,1 | 13,88 | 0,153 | Sol menor | 6A | 0,699 | La♯ mayor 6B (0,719, relativo) | 0,892 |
| 2 | El Ladrón Fantasma | 143,6 | 71,8 | — | — | Mi menor | 9A | — | — | — |
| 3 | Demian (máster ya publicado) | 117,5 | 61,5 | 20,81 | 0,486 | Re♯ menor 2A (0,829) | 2A | 0,829 | La♯ menor 3A (0,704) | 0,967 |
| 4 | Philémōn | 129,2 | 64,6 | 20,10 | 0,421 | Re menor | 7A | 0,925 | Fa mayor 7B (0,619, relativo) | 0,964 |
| 5 | Saint-Germain | 129,2 | 64,6 | 16,21 | 0,610 | Mi menor | 9A | 0,771 | Si menor 10A (0,601) | 0,957 |
| 6 | Õdế Odýnẽs | 78,3 | 47,9 | 18,64 | 0,408 | Fa menor | 4A | 0,889 | Do♯ mayor 3B (0,757) | 0,948 |
| 7 | La Voz del Desierto | 60,1 | 40,4 | 0,00 | 0,684 | Do mayor 8B (0,885) | 8B | 0,885 | La menor 8A (0,736, relativo) | 0,931 |
| 8 | Isis sin Velo | 92,3 | 46,1 | 10,03 | 0,564 | Re♯ menor | 2A | 0,727 | Sol♯ menor 1A (0,570) | 0,976 |
| 9 | El Sueño de Avalón | 99,4 | 49,7 | 9,56 | 0,596 | Mi menor | 9A | 0,823 | Sol mayor 9B (0,539, relativo) | 0,972 |
| 10 | La Casa de Dulce | 60,1 | 30,1 | 2,75 | 0,829 | Fa mayor 7B (0,503, débil) | 7A/8A | — | Do mayor 8B (0,442), Re menor 7A (0,425) | 0,976 |
| 11 | La Rueda de la Vida | 143,6 | 71,8 | 11,58 | 0,713 | Mi mayor | 12B | 0,820 | Si mayor 1B (0,697) | 0,962 |
| 12 | Postludio | 129,2 | 64,6 | 3,99 | 0,718 | Si menor | 10A | 0,687 | Si mayor 1B (0,369) | 0,982 |

**Lectura de la tabla contra el índice maestro:** en once de las doce pistas,
BPM, Camelot y tonalidad medidos coinciden con lo que el índice maestro
declara como canónico, dentro del margen de incertidumbre de §2. La
excepción real es La Casa de Dulce (10), tratada en §3.

## 2. Prueba de control del estimador — resuelta el 17 de agosto de 2026

Se generaron señales sintéticas de tempo conocido y se midieron con el mismo
guion:

| Tempo real | Medido | Error | Nitidez | Tonalidad |
|---|---|---|---|---|
| 100 BPM | 99,4 | 0,60 % | 0,951 | La menor 8A r=0,895 |
| 143 BPM | 143,6 | 0,42 % | 0,983 | La menor 8A r=0,879 |
| 72 BPM | 71,8 | 0,28 % | 0,964 | La menor 8A r=0,898 |

El estimador es exacto. La sospecha de que gravitara hacia valores centrales
queda descartada.

**Pero la comparación reveló la causa real de la convergencia: la salida
está cuantizada.** El guion devuelve valores de una rejilla discreta de la
forma `tempo = 60 × 43,0664 / desfase entero` (consecuencia de la frecuencia
de fotograma del envolvente de ataques, 22050 Hz sobre salto de 512). Los
doce valores medidos en todo el proyecto encajan en esa rejilla con error
inferior a 0,02:

60,1 (desfase 43) · 71,8 (36) · 78,3 (33) · 86,1 (30) · 92,3 (28) · 99,4 (26)
· 103,4 (25) · 117,5 (22) · 123,0 (21) · 129,2 (20) · 136,0 (19) · 143,6 (18)

**Consecuencia operativa, y es grave: la resolución empeora conforme sube el
tempo.**

| Bin | Vecinos | Incertidumbre real |
|---|---|---|
| 60,1 | 58,7 y 61,5 | ±1,4 BPM |
| 71,8 | 69,8 y 73,8 | ±2,0 BPM |
| 86,1 | 83,4 y 89,1 | ±2,9 BPM |
| 99,4 | 95,7 y 103,4 | ±3,8 BPM |
| 117,5 | 112,3 y 123,0 | ±5,3 BPM |
| 129,2 | 123,0 y 136,0 | ±6,5 BPM |
| 143,6 | 136,0 y 152,0 | ±8,0 BPM |

Que Philémōn y Saint-Germain dieran ambas 129,2 no es convergencia
sospechosa: cualquier tempo real entre 123 y 136 cae en ese bin.

**Regla nueva para toda medición futura:** por debajo de 100 BPM la medición
se toma como cifra; por encima de 120 se toma como intervalo y se confirma
de oído antes de declararla.

**Nota para quien mantenga la skill `analisis-semilla-medina`:** este
hallazgo (cuantización del estimador con resolución decreciente en tempos
altos) es un defecto de esa skill, no de este álbum en particular. No se
corrigió aquí porque queda fuera del encargo que dio origen a este paquete;
convendría trasladarlo a la documentación de esa skill.

## 3. Hallazgos que exigen o exigieron decisión del autor

**La Voz del Desierto (7) — explicado, no abierto.** La correlación favorece
Do mayor 8B (r=0,885) sobre La menor 8A (r=0,736, relativo), pero ambas
comparten la misma pareja de notas por ser relativas. El propio autor ya
razonó la elección en el documento fuente: «La menor mantiene la paleta
menor del fonograma sin contradecir la medición». El índice maestro adopta
La menor 8A; no es un error, es una decisión estética ya tomada sobre una
medición ambigua. Deriva 0,00, la más fiable de las doce: es material a
claqueta o secuenciado, no tocado libremente.

**La Casa de Dulce (10) — la más débil del proyecto, sigue abierta.**
Nitidez tonal r=0,503, la más baja de las doce pistas, con tres candidatas
dentro de 0,08 de diferencia (Fa mayor 7B, Do mayor 8B, Re menor 7A). El
diecisiete de agosto de 2026 se resolvió una duplicación de semilla con La
Rueda de la Vida (error de subida, confirmado por el autor; la semilla
correcta es «Time 1 (Remixed)», medida arriba). Sobre la tonalidad, dos
lecturas menores son posibles —Re menor 7A (relativa de la primera candidata)
o La menor 8A (relativa de la segunda)—; esta última coincide con una
variante histórica de folk noir «La menor, 8A, 100 BPM», de atribución
dudosa y ya superada por la medición, aunque el tempo histórico (100) no
case con el medido (60,1). El
índice maestro adopta La menor 8A a 60 BPM: usa la tonalidad de la variante
histórica pero no su tempo. Queda como la casilla del mapa Camelot con menor
respaldo de medición de las doce.

**Philémōn (4) — la hipótesis ternaria queda reforzada, no abierta.** El
índice maestro declaraba «hipótesis ternaria abierta (97)» junto al estado
de esta pista. La medición (129,2 BPM, bin de 123,0 a 136,0) es compatible
con esa hipótesis, porque 97 × 4/3 = 129,3, dentro del mismo bin. No es una
confirmación definitiva —la incertidumbre del bin sigue siendo ±6,5 BPM—
pero deja de ser una hipótesis sin apoyo.

## 4. Derogaciones respecto de fichas históricas anteriores

Notas de trabajo previas a la medición de semilla, superadas por ella; el
autor las declara viejas e innecesarias de perseguir como documentos aparte.
Se conservan aquí solo como el contraste que explica por qué el álbum
cambió de forma en dos casillas:

- **Isis sin Velo (8):** una ficha histórica decía Sol mayor lidio 9B / 94;
  la semilla dice Re♯ menor 2A / 92,3. El BPM casi coincide; la tonalidad no.
  El índice maestro ya adopta la lectura de la semilla (Re♯ menor, 2A, 92),
  de modo que esta discrepancia está resuelta en el documento canónico
  vigente; se deja constancia de que el álbum tuvo, en algún momento
  anterior, una concepción de esta pieza como pieza mayor («la excepción
  luminosa»), abandonada en favor de la medición.
- **La Rueda de la Vida (11):** una ficha histórica decía Re mayor 10B / 120;
  la semilla dice Mi mayor 12B / 143,6. El índice maestro ya adopta la
  lectura de la semilla. Sigue siendo la única pista mayor del álbum, según
  ambas fuentes.

## 5. Coherencia Camelot con la medición

Tramo confirmado por la medición (numeración del índice maestro): 1 (6A) →
2 (9A) → 4 (7A) → 5 (4A) → 6 (8B/8A) → 7 (9A) → 8 (12B) → 9 (2A) → 10 (9A) →
11 (12B) → 12 (10A). No es una progresión de casillas adyacentes; el propio
documento fuente deja abierto si la adyacencia Camelot sigue rigiendo como
criterio del proyecto o si la medición la desplaza. `album-in-absentia.md`
§2 ya declara que la adyacencia no rige la secuencia y opera solo como
desempate; esta tabla no contradice esa regla, solo confirma que no hay una
progresión adyacente continua de todas formas.
