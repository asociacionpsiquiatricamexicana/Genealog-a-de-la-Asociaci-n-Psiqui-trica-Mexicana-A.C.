# Compendio de teoría musical aplicable a prompting

Referencia de investigación citada desde §0.C del `SKILL.md`. Ese apartado
resume lo directamente accionable en un style o una letra; este archivo
desarrolla el fundamento teórico detrás de cada regla, para quien necesite
razonar un caso que la tabla operativa no cubre.

## 1. Métrica y compás

Un compás organiza los pulsos en grupos regulares. Los más frecuentes en la
música popular:

- **4/4 (compás simple cuaternario):** cuatro pulsos por compás, cada uno
  divisible en dos. Es el compás por defecto de indie rock, chamber pop e
  indie folk, los géneros ancla de §1 del `SKILL.md`.
- **3/4 (compás simple ternario):** tres pulsos por compás; produce sensación
  de vals. Poco frecuente en el perfil sonoro base, pero disponible si el
  encargo lo pide explícitamente.
- **6/8 (compás compuesto binario):** dos pulsos por compás, cada uno
  divisible en tres; produce una sensación de balanceo distinta al 3/4
  aunque comparta seis corcheas por compás. Suno responde razonablemente a
  «6/8 compound meter, waltz feel» como lo señala §0.C del `SKILL.md`.
- **Compases irregulares (5/8, 7/8):** grupos desiguales de pulsos (por
  ejemplo, 7/8 como 2+2+3). Baja fiabilidad generativa; preferir
  recomposición posterior en DAW, como ya indica §0.C.

**Subdivisión y tresillo:** dividir un pulso en tres partes iguales
(tresillo) en vez de dos (subdivisión binaria) es la base del *swing*. La
notación de corchea punteada más semicorchea aproxima un swing marcado sin
nombrarlo como tresillo exacto; explicitar «swing feel, triplet hi-hat» en el
style es más fiable que depender de que el modelo infiera el tresillo del
contexto rítmico.

**Hemiola:** superposición de dos patrones métricos distintos sobre el mismo
pulso (típicamente 3:2), que genera ambigüedad rítmica deliberada. Suno no la
reproduce de forma fiable por texto; es terreno de recomposición manual.

## 2. Intervalos y armonía

Un intervalo es la distancia entre dos notas. Los que más determinan el
carácter emocional de una progresión:

- **Tercera mayor frente a tercera menor:** define el modo (mayor o menor)
  de un acorde o una escala; es lo que Suno capta mejor por texto («major»,
  «minor», o adjetivos de mood asociados).
- **Tritono:** intervalo de tres tonos enteros, la disonancia más marcada de
  la escala diatónica occidental; históricamente asociado a tensión sin
  resolver. Suno rara vez lo reproduce de forma convincente y sostenida
  (§0.B del `SKILL.md`); mejor evitarlo como recurso deliberado en el texto
  del prompt.

**Picardy third (tercera picarda):** resolución de una pieza en modo menor
sobre un acorde de tónica mayor en el compás final, en vez del esperado
acorde menor. Produce una sensación de alivio o esperanza tras un desarrollo
en tono menor; es el recurso central del perfil emocional de §1 del
`SKILL.md` («bittersweet... with some hope»). Se aproxima en Suno con
descripciones de resultado («quiet major resolution on the outro») más que
con el nombre técnico del recurso.

**Acorde de séptima de dominante bemolizado (♭VII, «acorde prestado»):**
tomado del modo menor paralelo o de un modo como el mixolidio, y usado sobre
una base mayor para dar color sin modular. Suno lo capta razonablemente bien
cuando se nombra como «borrowed chord» o se describe su efecto («warm,
unresolved lift before the chorus»).

## 3. Escalas y modos

- **Escala mayor y menor natural:** las siete notas diatónicas en su
  ordenamiento estándar. Base segura para cualquier generación.
- **Modo dórico:** escala menor con la sexta elevada respecto a la menor
  natural; produce un carácter melancólico pero no oscuro, coherente con el
  perfil de §1 del `SKILL.md` («E menor / E dórico»).
- **Modo mixolidio:** escala mayor con la séptima rebajada; es la base
  armónica del acorde ♭VII descrito arriba.
- **Escala pentatónica:** cinco notas, sin semitonos consecutivos; es la
  escala de menor riesgo armónico, útil como base melódica cuando se busca
  máxima fiabilidad generativa.
- **Escala de blues:** pentatónica menor con una nota añadida (la «blue
  note», generalmente una cuarta aumentada o quinta disminuida usada como
  inflexión expresiva, no como acorde). Confirmada como segura por §0.C del
  `SKILL.md`.

## 4. Forma musical

La forma es la organización de secciones en el tiempo. §3.4 del `SKILL.md`
fija la forma operativa
(intro→verso→precoro→coro→verso→precoro→coro→verso→breakdown→coro→outro).
El fundamento teórico de por qué el precoro es obligatorio: sin una sección
de transición, el salto armónico y dinámico de verso a coro se vuelve
abrupto, y Suno, al no tener referencia de forma implícita como la tendría un
arreglista humano, tiende a resolverlo mal (silencio inesperado o cambio de
textura brusco).

## 5. Instrumentación por familia — fundamento del comportamiento descrito en §0.C

Las familias orquestales (cuerda, viento-madera, viento-metal, percusión,
teclado) tienen rangos de altura y comportamiento tímbrico bien
documentados en la práctica instrumental clásica. Lo relevante para Suno no
es el rango exacto —el modelo no respeta transposición fina— sino el
carácter tímbrico asociado al nombre del instrumento en el corpus de
entrenamiento: nombres instrumentales concretos («violin», «cello») activan
patrones tímbricos reconocibles con más fiabilidad que descripciones
genéricas («strings» a secas es más ambiguo que «string quartet» o
«solo cello»).

## 6. Aplicación práctica

Este compendio no sustituye §0.C del `SKILL.md`, que es la tabla operativa
verificada empíricamente contra la generación real. Sirve para decidir, ante
un caso no cubierto por esa tabla, qué tan razonable es esperar que Suno
capte un recurso armónico o rítmico dado, a partir de su naturaleza teórica
y de la lógica ya observada en los casos documentados.
