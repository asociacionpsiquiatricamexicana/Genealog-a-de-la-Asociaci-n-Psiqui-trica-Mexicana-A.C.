# Norma editorial · Sexagésimo aniversario de la Asociación Psiquiátrica Mexicana, A.C.

## Genealogía de la Asociación Psiquiátrica Mexicana, A.C. · Primera edición digital, 2026

Esta hoja fija las reglas de composición, nomenclatura y aparato del volumen y de su cuaderno
compañero. Cada una de las **diez cláusulas** tiene una prueba que la hace exigible en `norma.py`;
una cláusula incumplida detiene la entrega. Lo que no puede medirse se declara como criterio y se
somete al autor, no se da por cumplido.

**Alcance.** Primera edición digital de 2026. Los controles propios de la edición impresa (demasía,
marcas de corte, perfil de color, aplanado de transparencias, laminación, cálculo de lomo) quedan
deliberadamente fuera y se retomarán, si procede, en 2027.

**Derechos.** La obra se publica en acceso abierto bajo licencia Creative Commons
Atribución-NoComercial-SinDerivadas 4.0 Internacional. Los testimonios conservan la titularidad de
quienes los pronunciaron y se difunden bajo esa licencia en los términos de sus cartas de cesión; los
materiales de terceros que la obra cita o reproduce se rigen por sus propias condiciones.

**Precedencia.** Ante conflicto entre cláusulas, manda la capa cero: el contenido de terceros es
intangible. Ninguna regla de forma autoriza a alterar una cita textual, una entrada bibliográfica,
un dato duro, un nombre propio o un fragmento en lengua distinta del español.

---

## §1 · Nomenclatura y etiquetas

Cada sección vive en un archivo y cada archivo en una sección. El nombre codifica el lugar:
`FF-NN_Descriptor.tex`, donde `FF` es la familia (00 gobierno, 10 umbral, 20 capítulos,
30 periodos y fichas, 40 piezas testimoniales, 50 cierre y aparato, 60 apéndices) y `NN` el orden
dentro de ella. La familia nombra la procedencia del archivo y no la parte donde hoy se imprime:
la reestructuración del 26 de agosto de 2026 movió secciones de parte sin moverlas de familia, y
lo que manda sobre el orden es `libro.tex`. Cada archivo se
llama exactamente una vez desde `libro.tex` mediante la macro `\seccion`.

Renombrar una sección obliga a actualizar, en el mismo acto, su línea de Contenido y su cornisa.
La divergencia entre la clave del nombre y la posición en el volumen no es defecto, pero se declara:
anuncia una reestructuración pendiente.

**Todo título se compone con macro declarada**, nunca a mano. Un título construido con `\fontsize`
suelto se sale de la escala, pierde la sangría correcta y deja de responder a los cambios del
sistema: así el prefacio llegó a llevar un título de 26 pt donde el resto del volumen lleva 19.

**Rótulos y notas se alinean con el borde de la mancha**, no con la sangría de primera línea: son
rótulos, no párrafos.

**Prohibido** `\enlargethispage`. Forzar una página a contener más de lo que su caja admite empuja el
texto sobre el folio y sobre las notas, y el defecto solo aparece cuando el contenido crece, esto es,
mucho después de que la muleta se puso. Si algo no cabe, se recompone o se deja correr a la página
siguiente.

**Prohibido** coser bloques de PDF por fuera del documento maestro. La foliación, las cornisas y el
Contenido los resuelve LaTeX o no se resuelven.

**Toda sección de cuerpo se llama precedida de su marcador de navegación** `\unidad`, que crea a la
vez la entrada del índice del documento y la etiqueta con que el Contenido la alcanza. Una sección
sin marcador compone bien, cumple el resto de la norma y no existe para quien navega el documento:
así se coló una pieza testimonial entera, once páginas, fuera del índice. Quedan exentas las piezas
que disponen de su propia cabeza de página, esto es, las portadillas de parte y las de estilo vacío.

**Ningún conteo se escribe a mano en la prosa sin que el verificador lo coteje.** El volumen enuncia
cardinales (las piezas de la segunda parte, las fichas prosopográficas, los apéndices) que dejan de ser
verdad en cuanto se inserta una sección. La cláusula primera los deriva del corpus y compara cada
mención; la hoja de ruta de la entrega por partes los deriva también, en lugar de imprimirlos fijos.

**El ordinal de los apéndices no se escribe en ningún archivo.** Lo cuenta un contador y el orden
lo dicta `libro.tex`, que abre cada uno con `\apendice`; la enumeración del Contenido y los
ordinales en letra que el cuerpo usa en prosa los deriva `apendices.py` de ahí. Estuvo transcrito
en tres sitios y los tres llegaron a decir cosas distintas.

## §2 · Cornisas, folios y jerarquía

Toda sección de cuerpo declara su cornisa con `\marcas{verso}{recto}`. Ninguna sección hereda la
cornisa de la anterior. La exención **no se declara por lista**, que se desincroniza en cuanto una
pieza adopta cornisa, sino por lo que la propia sección dispone: quedan exentas las portadillas de
parte y las páginas que fijan estilo vacío. Cualquier otra sección sin `\marcas` hereda la cornisa
ajena, y eso es defecto.

**Disposición de cabeza y pie.** La cornisa encabeza la página sobre su filete; el folio la cierra al
pie, bajo el suyo, con zona propia. Dos filetes por página y no más, uno en cada extremo de la caja:
acotan la mancha, descansan la vista y suprimen los blancos sueltos. El folio nunca se compone bajo
un ornamento sin zona propia, que fue el defecto que obligó a retirar el filete de pie en la primera
tentativa. Los dos estilos de página quedan así unificados: `apertura` es `apm` sin cornisa.

Dos grosores de filete y no más: **0,30 pt** capilar (cornisa, notas, filetes menores) y **0,45 pt**
(filetes de título).

Cada nivel de la jerarquía conserva un solo cuerpo y un solo color:

| Nivel | Familia | Cuerpo | Color |
|---|---|---|---|
| H1 título mayor | Pagella versalita | 19 pt | vino |
| H2 sección | Pagella versalita | 12,5 pt | vino |
| H3 ficha | Pagella versalita | 11,5 pt | vino |
| H4 ladillo | Heros | 7 pt | vino |
| cornisa | Heros | 6,8 pt | gris |
| folio | Pagella cifras alineadas | 9,5 pt | vino |
| cuerpo | Pagella | 11 pt | tinta |

El aparato secundario se mueve en **tres escalones y no más**: 9,0 pt (cuerpo reducido), 8,6 pt
(referencias, notas de sección, apéndices) y 8,0 pt (Contenido). Un cuarto cuerpo en esa banda es
deriva, no intención.

### Escala legal de cuerpos

La tabla anterior fija la jerarquía; esta fija el catálogo completo, que es cosa distinta y que
hasta el 26 de agosto de 2026 no constaba por escrito. El eje noveno de la auditoría se llamaba
«tipografía fina» y no comprobaba ningún cuerpo: recogía las líneas mayores de 9,5 pt para buscar
viudas y no cotejaba ninguna. De ahí que la conclusión del volumen se compusiera al cuerpo de
consulta durante todos los sellados anteriores sin que nada lo dijera.

**Los cuerpos se declaran en la medida del PDF y no en la que pide la fuente.** XeTeX compone
Pagella con escala propia: los once puntos de la clase se miden en 10,9 y los dieciocho de la
portada en 17,9. Cotejar contra la cifra pedida obligaría a transcribir una equivalencia, y este
proyecto ha visto envejecer cuatro veces esa clase de dato. El catálogo vive en
`auditoria.CUERPOS`, con holgura de medición de 0,15 pt, que es redondeo del extractor y no
tolerancia de criterio.

Cuatro escalones de régimen:

| Medido | Papel |
|---|---|
| 10,9 pt | lectura seguida (los once puntos de la clase) |
| 9,0 pt | consulta: directorio, contacto, relación enlazada, agradecimientos |
| 8,6 y 8,0 pt | aparato: referencias, relaciones, notas de sección, Contenido |
| 6,6 pt | nota de estilo y rótulo menor |

Y trece papeles nominados, que no son tolerancia sino oficio declarado:

| Medido | Papel |
|---|---|
| 6,0 pt | llamada de nota, numeral volado |
| 6,2 pt | rótulo de ficha y pie de forro |
| 6,8 pt | cornisa |
| 7,0 pt | rótulo espaciado: ladillo y cintillo de serie |
| 7,4 pt | atribución del epígrafe del prefacio |
| 9,5 pt | folio |
| 9,6 pt | nombre corporativo de la portada interior |
| 10,0 pt | entradilla y epígrafe, en cursiva |
| 10,5 pt | subtítulo de la portada interior |
| 11,0 pt | dedicatoria, en cursiva |
| 11,5 pt | bajada de título mayor |
| 12,5 pt | epígrafe a página y rótulo de sección |
| 17,9 pt | título de la portada interior |
| 18,9 pt | título mayor de sección |
| 27,9 y 31,8 pt | capitular, derivada del cuerpo sobre el que cae |

Los tres cuerpos de la portada interior (9,6, 10,5 y 17,9) se nominan juntos: esa página compone su
propia escala en `secciones/10-01_Portada.tex`, con razón declarada, y no se juzga con la del
cuerpo. **Un cuerpo que no figure en el catálogo es defecto y reprueba la entrega**, y las páginas a
sangre quedan exentas por la misma razón por la que lo están de la mancha y del catálogo de filetes:
forros, portadillas de parte y láminas tienen composición propia.

Quien añada un papel lo añade al catálogo con su razón escrita al lado. Un catálogo sin razones se
convierte en la lista de lo que hubo, que es lo contrario de una norma.

El Contenido se compone con `\pageref` sobre etiquetas `\label{u:...}`: nunca con folios literales.
Cada entrada debe aterrizar en su marcador.

### Umbrales tipográficos: cero, con excepciones nominadas

Viudas, huérfanas y escalerillas de partición tenían umbral de tolerancia (menos de seis, menos de
seis, menos de diez líneas flojas) y ninguno de los tres sumaba al valor que el eje devuelve: ni
denunciándolos podía reprobar la entrega. **Los tres umbrales quedan en cero y los tres gobiernan.**
Un umbral que no reprueba no es umbral: es ornamento, y se suprime.

Lo que se tolera se nombra. Las excepciones viven en `auditoria.EXCEPCIONES` y en
`notas.EXCEPCIONES`, cada una con la sección donde habita, la razón por la que se tolera y la fecha
en que se nominó. Cuando una deja de hacer falta, el eje lo dice y se retira.

**Regla general: toda excepción se nomina por sección y nunca por coordenada física.** No por página,
no por folio, no por posición en la caja. La razón es que la coordenada es derivada y la sección es
estructural: la relación anterior decía «páginas 118, 208 y 212» y el reflujo de la conclusión las
movió a 96, 249 y 253, de suerte que habría absuelto tres páginas inocentes y denunciado tres
defectos reales. Una excepción atada a una coordenada envejece en silencio, que es el peor modo de
envejecer; atada al nombre de su sección, envejece ruidosamente, y el instrumento avisa. La regla
vale para toda excepción del proyecto y no solo para las tipográficas.

Excepciones vigentes: tres escalerillas de partición, una en la galería del tercer periodo y dos en
el in memoriam, por densidad de nombres propios sin puntos de corte alternativos; y una línea floja
de badness 5260, la del título del apéndice «Relación enlazada de expresidentes» (`libro.tex:128`),
que se parte con `\\` dentro de un párrafo justificado. **Ninguna huérfana:** las dos que la relación
heredada daba por toleradas no lo eran. El volumen fija `\clubpenalty=10000`, de modo que TeX no deja
sola la primera línea de un párrafo, y lo que el detector acusaba era el primer campo de una ficha
bajo su título y una cita inserta al pie, ambos sangrados por composición. Se comprobó rebajando la
penalización a cero: sin ella aparecen diez huérfanas y el detector las denuncia; con ella, ninguna.

## §3 · Geometría, color y contraste

Página igual a corte: 15,5 × 23 cm, sin demasía. **Mancha simétrica**: 2,2 cm a cada lado, 11,15 cm
de justificación, idéntica en todas las páginas. El volumen no se imprime ni se encuaderna, de modo
que la alternancia a dos caras del libro impreso no compensa aquí ningún lomo y se percibe, con
razón, como desalineación al pasar de una página a otra en pantalla. Ninguna página excede su
mancha; los forros y las láminas de color tienen composición propia y quedan fuera de esta medida.

Paleta cerrada: vino `#7D4343`, vino oscuro `#5E3033`, rojo `#E7253F`, tinta `#1C1B1A`, gris
`#767070`, crema `#F7F4EF`. Toda la tinta del volumen pertenece a la paleta.

Todo par de tinta y soporte alcanza el nivel AA de contraste (4,5:1) para texto pequeño, medido
sobre la fórmula de luminancia relativa. Los valores vigentes: tinta sobre blanco 17,20:1; vino
sobre blanco 7,62:1; crema sobre vino 6,95:1; gris sobre blanco 4,86:1. El gris es el escalón más
bajo: cualquier aclarado suyo rompe la conformidad.

**Catálogo de filetes.** El interior no admite más filetes que estos siete rótulos de función,
que en el catálogo del código (`auditoria.FILETES`) son ocho pares legales, porque el brazo del
bolo existe en vino y en crema.
La medida no es decorativa: es lo que le dice al lector qué está mirando.

| Ancho | Grosor | Color | Función |
|---|---|---|---|
| ancho de caja | 0,30 | vino | cornisa y folio |
| ancho de caja | 0,30 | gris | cabeza de ficha prosopográfica |
| 3 cm | 0,45 | vino | filete de título mayor |
| 2,8 cm | 0,45 | vino | filete del Contenido, acortado para que quepa en una página |
| 1,6 cm | 0,45 | vino | filete corto de ficha prosopográfica |
| 1,4 cm | 0,30 | gris | regla de nota, tanto de sección como al pie |
| 1,45 cm | 0,45 | vino o crema | brazo del ornamento de bolo |

Dos grosores, no más: 0,30 para lo que separa y 0,45 para lo que marca. Las páginas a sangre —los
dos forros, las cinco portadillas de parte y la lámina del epígrafe— quedan fuera del catálogo,
porque llevan composición propia, y llevan todas el mismo marco crema a 1,12 cm del corte.

**Capa de texto (ActualText).** Todo rótulo compuesto con espaciado (`\textls`, cornisas,
títulos, ladillos, capitular) declara su texto limpio con `\legible`: la página se imprime igual y
la máquina (visores, copia, búsqueda, lectores de pantalla) lee palabras enteras y no
«M E S A S». `texto_extraible.py` lo exige con poppler en su modo por omisión, que es el hostil;
medir con el modo amable sería el modo VI de la familia. Un rótulo espaciado nuevo sin `\legible`
es defecto, y la prueba «ilegible» de la batería lo reproduce.

**Ornamento de bolo.** Dos brazos de 1,45 cm, hueco de 0,25 cm a cada lado y punto de 0,55 mm de
radio. Es la marca de las páginas de cortesía: portada, dedicatoria, semblanzas y portadillas de
parte. Se declara una sola vez, en `base.tex`, y no se dibuja a mano en ningún sitio: escrito tres
veces salía de tres maneras, y tres marcas parecidas no son una marca.

**Cuerpo del texto.** Once puntos para lo que se lee seguido —capítulos, piezas testimoniales,
conclusión, apéndices de prosa— y nueve para lo que se consulta: directorio, contacto, relación
enlazada y agradecimientos. Componer a nueve una parte de lectura seguida la degrada a la categoría
del aparato, y la jerarquía de la página pasa a decir lo contrario que la del libro.

Sin máscaras de suavizado, sin grupos de transparencia y sin modos de fusión distintos de Normal.
Los estados de opacidad constante de los forros se admiten porque no exigen aplanado en lectura
digital; una eventual edición impresa deberá resolverlos.

## §4 · Aparato bibliográfico

Norma APA 7 con dos desviaciones declaradas: nombre de pila completo en autoría de onomástica
hispana, y conjunción «y» en lugar del signo ampersand.

Toda entrada tiene la forma «Autoría. (Fecha). Título». La ausencia de fecha se declara con
`(s. f.)`; no se omite. Las listas van en orden alfabético por autoría y, dentro de una misma
autoría, por año ascendente, con las obras sin fecha antes que las fechadas. La ordenación es
insensible a diacríticos, conforme al alfabeto español. La partícula onomástica se capitaliza cuando
abre la entrada. El designador de función se abrevia con inicial mayúscula: `(Coords.)`.

Los identificadores DOI se escriben en forma canónica `https://doi.org/10.…`.

Toda cita del cuerpo tiene entrada en alguna relación, y toda sigla corporativa citada remite a la
denominación completa de la entrada.

**Regla propia:** el testimonio oral no se cita con autoría y año en el cuerpo; se atribuye por el
nombre del entrevistado y se remite a nota.

**Tres voces, tres composiciones.** La **entradilla** de cada pieza testimonial es voz del compilador
y presenta lo que sigue: cursiva de 8,6 pt con sangría a ambos lados. El **cuerpo** es la voz del
entrevistado o del autor: redonda de 11 pt. La **nota** es aparato editorial: sans gris de 6,6 pt tras
su filete corto. Ninguna de las tres se compone a mano: cada una tiene su entorno, y una construcción
suelta con el mismo cuerpo de otra las confunde.

**Las notas no se parten ni se quedan solas.** Toda nota va encadenada al texto que la llama con
penalización infinita y con interlínea indivisible, de modo que, si no cabe, arrastre consigo las
últimas líneas de su párrafo en lugar de quedarse huérfana al principio de la página siguiente.

**Distinción semántica:** el entorno `referencias` es para fuentes y se juzga con la norma APA; el
entorno `relacion`, tipográficamente idéntico, es para índices enumerativos (el Apéndice I de
expresidentes) y no se juzga con ella. Usar uno por otro es un defecto de codificación, no de estilo.

## §5 · Terminología, glosario y siglas

El volumen desarrolla las denominaciones institucionales en su primera aparición y evita las siglas
en el cuerpo. Toda sigla que aparezca en el volumen está registrada en la sección de siglas del
glosario. Toda sigla que llegue a aparecer en prosa lleva su glosa en el primer uso.

Quedan exentos de glosa en línea los identificadores normalizados, que son códigos y no
denominaciones: ISSN, ISBN, DOI, y las formas «A.C.» y «S.C.».

El glosario cumple tres funciones que no se confunden: define términos técnicos, fija el sentido
operativo de las categorías de la investigación y recoge las expresiones propias de la corporación.

## §6 · Activos gráficos

El vector manda. Las marcas institucionales (emblema del sexagenario, monograma, código de barras)
se componen desde PDF vectorial derivado del SVG de origen; el mapa de bits queda para la fotografía.
Un emblema por forro. **Interiores sin emblemas.**

El código de barras se compone a tamaño natural: nunca se reescala, porque el ancho de módulo es una
magnitud normada y no una preferencia. Se verifica por decodificación, no por inspección.

Todo activo llamado debe existir. Está prohibido sustituir en silencio un activo ausente por un
sucedáneo: la compilación debe detenerse y decirlo.

## §7 · Compilación, integridad y punto de retorno

Motor XeLaTeX sobre memoir, dos pasadas, con `polyglossia` y `texlive-lang-spanish`. Sin este último
no hay partición silábica en español y la justificación se afloja: es dependencia dura, no adorno.

**Los forros se componen también dos veces.** Sus elementos van anclados con `remember picture,
overlay`, que en la primera pasada, sin `.aux` previo, cae en posición provisional. Con el auxiliar
de una corrida anterior el defecto no se manifiesta: solo aparece al compilar desde limpio, que es
exactamente lo que hace quien recibe el legajo. Se descubrió así, en una compilación desde cero, con
el panel del código de barras descentrado.

**La verificación debe poder fallar.** Cada instrumento devuelve código de salida distinto de cero
cuando halla defecto, y ninguna cláusula imprime conformidad sin haberla medido. Una cláusula que
declara «conforme» pase lo que pase es peor que no tenerla, porque produce confianza infundada.

El volumen se sirve desde el sitio institucional: la entrega se linealiza (vista rápida en red) para
que el lector vea la primera página antes de que termine la descarga, y conserva sus enlaces activos.

Umbral de entrega: cero desbordes de caja, cero líneas flojas, cero referencias indefinidas, cero
colisiones entre ornamento y texto, cero páginas fuera de mancha, cero saltos o duplicados de folio,
código de barras decodificado y vocabulario prohibido en cero.

Todo trabajo se hace sobre repositorio con historia y con una etiqueta por pasada cerrada. Un cambio
sin marcha atrás no debe hacerse.

Todo hallazgo se registra en `HALLAZGOS.md`, en esta misma carpeta, con fecha, medición, propuesta
y estado: resuelto, declarado o pendiente de decisión del autor. Un defecto que se acepta debe
quedar escrito; un defecto que se calla vuelve.

## §8 · Forros, portada y preliminares

**Nomenclatura.** La pieza que lleva título, subtítulo, tomo, responsables y pie de imprenta es la
**portada**, no la portadilla. Una portadilla es una hoja que solo repite el título. Llamar
portadilla a la portada confunde al lector y al compositor.

**La página legal se lee, no solo se firma.** Se compone a la medida de la caja del volumen, con el
cuerpo del aparato principal y con la ficha de catalogación dentro de su recuadro, como la cédula
que es. Ninguna página legal cabe a costa de cien caracteres por renglón ni de márgenes menores que
los del resto del libro.

**La portada declara dos cosas y no repite la cubierta.** Arriba, la naturaleza del objeto: se trata
de un suplemento conmemorativo de la publicación periódica de la asociación. Abajo, la obra que
contiene y su responsabilidad, en una línea por función. Al pie, tras el filete ornamental, el
**cintillo bibliográfico**: serie, título de la publicación periódica, año, extensión, identificador
y licencia. La extensión se compone con `\pageref` sobre la etiqueta del colofón, nunca con una cifra
literal, porque el reflujo la desplaza. La portada conserva así la autoridad bibliográfica que los
catálogos y los repositorios toman de ella, sin duplicar la composición de la cubierta.

**Orden canónico de los preliminares**, conforme a la convención internacional del libro: portada,
página legal (con el aviso de derechos, la ficha de catalogación y el identificador de la
publicación), dedicatoria, lámina de epígrafe y Contenido. Después, el umbral propio del volumen:
directorio, contacto, semblanza del editor, semblanza del compilador, prefacio, nota metodológica y
glosario, que cierra el umbral porque define los términos con que se leerá todo lo demás.

**Estructura del volumen.** Un umbral decorativo, tres partes numeradas —primera, *El gremio*, con
los cuatro capítulos y las mesas directivas de cada periodo; segunda, *Los que presidieron*, con
las catorce piezas testimoniales; tercera, *Conclusión*— y catorce apéndices, seguidos de
agradecimientos, colofón y contracubierta.

Cada parte abre con su portadilla a sangre, y el marcador de navegación de la parte cae en la
portadilla y no en la primera sección de contenido: de otro modo el índice lleva a la página
siguiente a la lámina y la entrega por partes da cada portadilla a la parte anterior.

Ninguna sección repite en su título el rótulo que su portadilla acaba de dar dos páginas antes.
El colofón va al último, después de los agradecimientos.

**Forros.** Campo vino a sangre, doble filete perimetral de 0,70 y 0,30 pt en crema, y **un solo
emblema por forro**: el **monograma institucional en la cubierta**, porque no consigna fecha y
conviene a un volumen sobre el pasado, y el **emblema del sexagenario en la contracubierta**, donde
el bienio que lleva impreso significa lo que es, la administración bajo la cual se hizo la edición.
Sin mapa de bits en ningún forro: todo elemento gráfico es vectorial.

**Arquitectura de la cubierta.** El monograma encabeza la página y hace las veces de identificación
corporativa, de modo que el nombre de la asociación no se repite en sans sobre el título. El título
se compone **en una sola línea**, a 30 pt con interletraje de 3, que mide 332 pt sobre los 376 útiles
entre filetes interiores (88 por ciento del ancho, con 22 pt de holgura a cada lado). Debajo, el
nombre de la asociación en cursiva, sin artículo antepuesto. El pie del congreso se ordena en dos
escalones, no en dos líneas iguales: el nombre del congreso en versalitas de la serifa del volumen y
sus coordenadas en sans menor, de modo que el ojo distinga el acontecimiento de sus circunstancias.

**Opacidad.** Escala declarada de tres niveles sobre el campo vino: **0,90** y **0,75** para texto
(5,97:1 y 4,71:1, ambos en nivel AA) y **0,50** para filetes (3,01:1, umbral de elemento gráfico).
Ningún texto por debajo de 0,75. La opacidad rebaja el contraste efectivo, de modo que contarla no
basta: hay que calcular el color resultante y juzgarlo.

**Ritmo vertical.** Ningún hueco interior mayor que el doble del menor. En la cubierta, el aire bajo
la marca es ligeramente mayor que el aire sobre ella, conforme al centrado óptico. En la
contracubierta, el bloque de identificación (filete, serie, código y nota) se ancla al pie como
unidad, y no se dispersa dejando un agujero en el tercio inferior.

**Código de barras y e-ISSN.** El identificador es un **e-ISSN**, no un ISSN impreso, y así debe
rotularse en todas partes: el volumen circula solo por medio digital y no habrá tiraje. El código se
compone sobre panel blanco, centrado en el eje de la
caja con tolerancia de un punto, con el identificador legible encima y sin que ningún texto lo
invada. El ancho de módulo es 0,30 mm, por encima del mínimo normado de 0,264 mm. Se verifica por
decodificación efectiva, nunca por inspección visual.

**Portadillas de parte.** Cada gran división del volumen (umbral, las tres partes numeradas, cierre
y apéndices) abre con una lámina de campo vino a sangre, sin folio ni cornisa, que compone el
ordinal en sans, el nombre de la parte en versalitas de la serifa, el filete con punto y una bajada
en cursiva. La lámina no informa: separa. Existiendo portadillas, el Contenido puede volver a
numerar las partes que el cuerpo compone.

**Láminas de cortesía.** Ninguna página del volumen queda en blanco puro: donde la estructura pide
respiro, se compone una lámina sobria, con epígrafe o campo de color, y sin cornisa ni folio.

**Lomo.** La edición digital no tiene lomo. Su cálculo, y con él la laminación y el perfil de color,
pertenecen al pliego de la edición impresa y quedan fuera de esta norma.

## §9 · Imágenes y activos derivados

**Formatos.** Marcas institucionales en SVG como fuente de verdad y PDF vectorial como forma de
composición; fotografía en JPEG. Prohibido componer una marca desde mapa de bits habiendo vector.

**Resolución.** Toda fotografía **del volumen** alcanza al menos **200 puntos por pulgada medidos al
tamaño final de colocación**, umbral propio de la edición digital. Los dos retratos del volumen están
hoy en 686 y 1270 puntos por pulgada, de modo que también satisfarían el umbral de impresión de 300
si alguna vez se decidiera imprimir.

**Salvedad declarada para el cuaderno de acervo.** Allí el umbral baja a **165 puntos por pulgada**, y
el motivo es que el volumen y el cuaderno hacen cosas distintas con sus imágenes. El volumen las
elige: si una no alcanza, se sustituye o se retira. El cuaderno reproduce el acervo **entero**, tal
como está, y su función es que alguien reconozca lo que ve. Aplicarle los 200 obligaría a componer
siete piezas por debajo de su medida útil, y la peor de ellas, un congreso nacional sin identificar,
quedaría en 2,96 cm de ancho: ilegible justamente para lo único que se le pide. Se prefiere una
reproducción algo menos densa y legible a una intachable y muda. La salvedad tiene dos límites: rige
solo en el cuaderno, y **ninguna pieza se amplía por encima de lo que su archivo sostiene**, regla que
`acervo.py` aplica antes que cualquier medida de la retícula.

**Derivación reproducible.** El PDF de cada marca se obtiene del SVG con una orden registrada:

    python3 -c "import cairosvg; cairosvg.svg2pdf(url='arte/X.svg', write_to='arte/X.pdf')"

Se comprobó que esta orden reproduce los activos vigentes con diferencia máxima de 2 sobre 255 en
el trazado, atribuible al suavizado y no a la geometría. Toda marca en PDF conserva su SVG de origen
en la misma carpeta: sin fuente no hay reproducción.

**Archivo limpio.** La carpeta de activos contiene solo lo que las fuentes usan. Un archivo gráfico
que ofrece variantes no usadas invita al error: el volumen llegó a tener un logotipo en JPEG de 600
píxeles conviviendo con su versión vectorial. Las variantes retiradas se conservan en `_retirados/`,
recuperables, no borradas.

## §10 · Cuaderno de acervo

El cuaderno de acervo es obra distinta del volumen y se rige por esta cláusula, no por las que
gobiernan el libro. Comparte con él la paleta, los tipos y la geometría de página; se aparta en lo
demás, y cada apartamiento se declara aquí.

**Un solo registro.** Pies, signaturas, secciones y estados viven en `datos_acervo.json`. La fuente
`acervo.tex` y las cifras de `acervo_cifras.tex` se generan de ahí y **no se editan a mano**: por eso
ninguna de las dos se versiona. Editar el archivo generado es el modo de perder el trabajo en la
siguiente compilación.

**Nada se transcribe.** Toda cifra que el cuaderno enuncia (piezas, secciones, pendientes, láminas a
página sola) se deriva del registro, y todo folio que el sumario o el catálogo citan se toma por
referencia cruzada. La advertencia llegó a decir «treinta y seis piezas esperan ese auxilio» tomando
la cuenta de la sección «Sin fecha establecida», que no es lo mismo: una pieza puede estar fechada y
seguir sin identificar. Eran veinte.

**Revisión visual antes de cada entrega.** Ninguna pieza entra al cuaderno sin que se haya mirado.
La primera depuración se hizo por nombre de archivo y descripción, y dejó pasar nueve piezas que no
eran fotografías: dos capturas de transmisión, una de videoconferencia, tres carteles, dos plantillas
gráficas y un comunicado electoral, una de ellas rotulada como retrato de una expresidenta cuando
mostraba una parrilla de veinte ponentes. **Un pie que no corresponde a su imagen es peor defecto que
cualquier fallo de retícula**, y ningún instrumento lo detecta: se detecta mirando.

El criterio que separa: **hay fotografía donde hay cámara y contexto.** La toma de una pantalla en una
sala, de una tableta sobre un escritorio o de un cartel colgado es documento fotográfico y se queda;
la imagen plana exportada de esa misma diapositiva, cartel o transmisión, no.

**Portadilla por sección.** Cada sección abre con página propia: la cifra de piezas en grande, el
rótulo y el epígrafe, centrados. No es adorno ni desperdicio: se intentó que la primera lámina
compartiera página con el rótulo y de ahí salieron tres defectos encadenados, la lámina partida de su
pie, el pie solo en la página siguiente y el rótulo abandonado arriba. No caben con holgura un
rótulo, una fotografía a página sola y su pie en dieciocho centímetros de caja. La portadilla resuelve
el conflicto en vez de administrarlo. El epígrafe no repite la cifra que la portadilla ya compone.

**Cornisa viva.** Las páginas de lámina nombran su sección. Con noventa y nueve piezas en cinco
secciones es la única manera de saber dónde se está sin volver atrás. Pierde el filete de cabecera del
volumen: en una página de láminas corre justo sobre el borde superior de las fotografías y compite
con él.

**Tres reglas de retícula**, comprobadas en cada entrega por `auditoria_acervo.py`:

1. Ninguna página mezcla orientaciones discrepantes. No basta agrupar por orientación en el reparto:
   la última fila de un grupo comparte página con la primera del siguiente si no se fuerza el corte.
2. Las fotografías se componen a **superficie constante** dentro de caja de altura constante. La caja
   iguala el arranque de los pies; la superficie iguala el peso visual. Igualar solo la altura dejaba
   las cajas alineadas y las imágenes variando hasta el doble de tamaño.
3. Las de proporción mayor que 1,9 salen de la retícula, van a línea completa y se intercalan cada
   dos filas. Agrupadas al final del grupo quedaban solas en la última página de su sección.

**Estado en la signatura.** El sufijo codifica lo que falta: `xi` por identificar, `xf` por fechar,
`cf` a cotejar. De ahí salen la columna de estado del catálogo y el punto rojo que marca las piezas
pendientes en la lámina. El rojo de la Asociación no tiene otro uso en el cuaderno: marca, no decora.

**Dos carpetas de activos y una trampa.** `arte/acervo` guarda la copia de trabajo y
`arte/acervo_plena` la de mayor tamaño, para las piezas a página sola. Los archivos son homónimos, de
modo que basta copiar uno de un sitio a otro para que una lámina se componga desde la reducción sin
que nada lo advierta: `acervo.py` comprueba en cada entrega que la copia plena tenga más puntos que
su homónima. Rige aquí, como en la cláusula novena, el archivo limpio: la carpeta contiene solo lo
que las fuentes usan, y lo retirado va a `_retirados/acervo/`.

**Lo que no se hace, y por qué.** No se recorta: el encuadre original forma parte del documento y en
más de una pieza es el fondo, un letrero o un telón lo que permitió identificarla. No se vira a
sepia: se probó con tres versiones de la misma pieza y el virado aplana la imagen y pierde
información. No se amplía por encima de lo que el archivo sostiene: una fotografía estirada más allá
de sus puntos no parece mejor, parece falsificada.

## Los prefijos de archivo, y por qué no se renombran a la ligera

Ocho archivos de sección conservan un prefijo numérico que ya no sigue el orden del volumen:
`30-00_Lamina_Segunda_parte` abre una parte cuyo cuerpo es el bloque 40, `40-00_Lamina_Tercera_parte`
abre otra cuyo cuerpo es el 50, y seis apéndices llevan prefijos 10, 40 y 50 por haber sido otra cosa
antes. Es sistemático, es consistente y se presume deliberado: los nombres registran de dónde viene
cada pieza, que en una obra reordenada tres veces no es poca información.

Pero **el nombre no es solo un nombre: dos conteos del volumen se derivan de él.** `norma.py`, en la
cláusula primera, cuenta las piezas testimoniales por `startswith('40-')` y las fichas de la galería
por `startswith('30-')`. El mismo archivo advierte, tres líneas más arriba, que los apéndices **no**
se cuentan por el patrón del nombre, porque seis conservan el que tenían cuando eran otra cosa y el
patrón publicaba siete donde hay catorce.

De ahí la regla: **ningún renombrado de archivos de sección puede ejecutarse sin regenerar los
conteos y comprobar que no han cambiado.** Un renombrado que mueva una pieza fuera del prefijo 40 o
una ficha fuera del 30 alterará en silencio los cardinales que el volumen enuncia en prosa, y el
cotejo de cardinales dará por buena la cifra nueva porque la deriva del mismo sitio que acaba de
cambiar. Quien renombre, deriva primero los conteos por otra vía y los compara.

## La familia de la conformidad falsa

Un patrón nombrado se vigila; un incidente se olvida. Este proyecto ha producido seis modos de
fallo que parecían episodios sueltos y son el mismo: **la conformidad se obtiene actuando sobre el
instrumento y no sobre la obra.** El rótulo se pone en verde y la página no cambia.

**I. El verificador que existe y no gobierna.** La prueba corre y su veredicto no llega a la
decisión. `build.py` sumaba nueve de los doce ejes de auditoría y dos de los cinco de trazabilidad;
la cláusula del cuerpo examinaba cuatro secciones, las cuatro exentas. Apareció cuatro veces.
*Remedio:* lista única de ejes, y quien invoca no enumera.

**II. El aviso permanentemente falso.** El veredicto llega a la decisión y siempre miente, de modo
que el lector aprende a desoírlo. La tercera familia tipográfica, cinco folios que no se imprimen por
abrir unidad, el aire de la portada medido con la vara del texto corrido, ciento cuarenta y nueve
avisos de concordancia de los cuales uno era legítimo. *Remedio:* acotar el eje a un léxico cerrado,
o derivarlo de la fuente, en vez de generalizarlo.

**III. La supresión del objeto denunciado.** El veredicto llega, se lee, y se resuelve borrando
aquello que lo produce: el aviso se vuelve verdadero sin que la obra mejore. El 26 de agosto de 2026
ocho entradas sin anclaje se suprimieron de la relación de fuentes, y desde entonces la cadena
declaró «toda entrada catalogada se invoca en el cuerpo» sin que nadie hubiera atribuido ni decidido
nada. Es el más peligroso de los cuatro, porque destruye la evidencia del defecto junto con el
defecto, y porque su rastro no está en el volumen sino en el historial del repositorio. *Remedio:*
`trazabilidad.supresiones_del_aparato()`, que compara la relación contra el último punto de retorno y
exige que lo retirado figure en la nota de obras consultadas sin cita directa. Retirar sigue siendo
posible; retirar en silencio, no.

**V. El catálogo que identifica por la medida.** El instrumento coteja una magnitud y no una función,
de suerte que un elemento pasa tomando prestada la medida de otro. El filete de la portada interior
mide 314 pt a 0,30 en vino, exactamente lo que el catálogo declara para «cornisa y folio», y no es
ninguna de las dos: la página declara estilo vacío y no lleva ni cornisa ni folio. *Remedio:* contar y
situar además de medir, y declarar por página cuántos elementos de cada clase le corresponden. Su
pariente más peligroso es la exención por clase de página: el eje de ornamentos saltaba las páginas a
sangre enteras, y allí podía vivir cualquier cosa.

**VI. El instrumento que mide lo que varía en vez de lo que es fijo.** El aire bajo el encabezado,
medido a la caja de la primera línea, da diecisiete valores entre 12,7 y 87 puntos, porque la caja
depende del glifo más alto; medido a la línea de base, que es lo que la composición fija, da 22,8 pt en
205 de 274 páginas y ocho desviaciones, todas con nombre. Una medición dispersa no prueba que la página
esté mal: puede probar que se midió lo que no era. *Remedio:* antes de declarar dispersión, comprobar
que la magnitud medida es la que la composición fija.

**IV. La excepción nominada sin caducidad.** El defecto se declara tolerado y el rótulo vuelve a
verde. Es el único que este proyecto se ha infligido a sí mismo con plena conciencia, el 26 de agosto
de 2026, al nominar tres escalerillas de partición y una línea floja. Se admite, porque hay defectos
cuyo remedio cuesta más que el defecto, y se acota: toda nominación lleva razón escrita y fecha, el
eje publica cuántas hay y avisa de la que ya no hace falta, y **una relación de nominaciones que crece
es una obra que empeora con el rótulo en verde**.

### La prueba que atrapa a los cuatro

Ante todo rótulo que pasa de rojo a verde, una sola pregunta: **¿la corrección habría cambiado la
página?** Si la respuesta es no, uno de los cuatro primeros ocurrió. Y ante todo rótulo que estaba en
verde desde el principio, la pregunta gemela: **¿qué mide exactamente, y coincide con lo que quiero
saber?** Los dos últimos modos viven ahí. Silenciar el veredicto, ahogarlo en ruido,
borrar lo medido o declararlo tolerado son cuatro maneras de responder que no.

Y su corolario para quien herede el legajo: **un instrumento que solo puede volverse verde no mide
nada.** Por eso cada detector de este proyecto se somete a sabotaje, que consiste en introducirle el
defecto que dice detectar y comprobar que falle. La batería vive en `sabotaje.py` y se reejecuta al
cierre de cada pasada, porque una corrección puede inutilizar un detector reparado antes.

## Criterios que no se automatizan, y por qué

Tres cosas se someten al autor porque una máquina no debe decidirlas:

**Formas onomásticas divergentes.** El aparato registra a una misma autora como «Sacristán, Cristina»
y como «Sacristán, María Cristina», y a una misma coautora como «Ordorika, Teresa» y como «Ordorika
Sacristán, Teresa». APA exige una sola forma por persona, pero la forma correcta es la que cada obra
lleva impresa: es cotejo documental, no criterio de estilo. Queda declarado y pendiente.

**Entradas de glosario sin uso en el cuerpo.** Un glosario puede definir la categoría operativa de un
método aunque el cuerpo la emplee flexionada. Solo se señala; no se suprime.

**Escaleras de guiones residuales.** Cinco páginas presentan tres particiones seguidas. Reducirlas
más exige aflojar el espaciado de todo el volumen, lo que empeora aquello que se quería mejorar. Se
declara el residuo y se acepta.

---

*Última revisión: 27 de agosto de 2026. Verificable con `python3 norma.py`.*
