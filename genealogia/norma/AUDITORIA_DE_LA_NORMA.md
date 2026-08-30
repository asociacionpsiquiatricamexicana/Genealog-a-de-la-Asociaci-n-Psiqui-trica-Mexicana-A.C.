# Auditoría de los documentos de gobierno · 28 de agosto de 2026

Lectura cruzada de `NORMA_APM60.md`, `HOJA_DE_CRITERIOS.md`, `CONTENIDO_DE_LAS_PARTES.txt`,
`ENTRADAS_SIN_ANCLAJE.md` e `INSTRUCCIONES_DEL_TALLER.md` buscando inconsistencias internas
entre ellos. No tengo el repositorio de LaTeX ni los scripts (`build.py`, `norma.py`,
`diagnostico.py`...) que estos documentos gobiernan, así que no puedo ejecutar la verificación
que ellos mismos exigen ("no se declara conforme lo que no se comprobó"); lo que sigue es
contradicción textual entre los documentos, resuelta por lectura, no por instrumento. Donde la
divergencia era clara y de qué lado se resolvía, corregí la copia en `genealogia/norma/`
aplicando la propia regla del taller: "ante divergencia, la norma gobierna y la medición
gobierna sobre la norma" (`INSTRUCCIONES_DEL_TALLER.md`). Donde no había manera de saber qué
lado es el vigente, dejo la anomalía declarada y sin tocar.

## Corregido

### 1. La línea floja de badness 5260: quedaba dicha como corregida y como vigente a la vez

- `NORMA_APM60.md` (líneas 178-180), en su lista de "Excepciones vigentes", incluye
  explícitamente "una línea floja de badness 5260, la del título del apéndice «Relación
  enlazada de expresidentes» (`libro.tex:128`)" como excepción nominada, no corregida.
- `HOJA_DE_CRITERIOS.md`, en su sección "Estado al 27 de agosto de 2026", decía en cambio: "La
  línea floja de badness 5260 se corrigió y hoy se exige cero" — y esa misma frase se contradecía
  a sí misma, porque la oración anterior dice que el umbral pasó a "cero **con excepciones
  nominadas**": si estuviera corregida no haría falta nombrarla como excepción.
- **Corregido** en `HOJA_DE_CRITERIOS.md`: ahora dice que la línea no se corrigió y queda
  nominada como excepción vigente, remitiendo a la norma. La norma (`NORMA_APM60.md`) no se tocó,
  porque es la que gobierna.

### 2. "Once papeles nominados": el título no cuadraba con su propia tabla

- `NORMA_APM60.md` encabezaba la tabla de papeles tipográficos declarados como oficio (no como
  tolerancia) diciendo "once". La tabla que sigue tiene quince filas, y la oración inmediata
  siguiente agrupa tres de ellas (9,6 · 10,5 · 17,9 pt, los tres cuerpos de la portada interior)
  como un solo papel nominado en conjunto. Aplicando esa propia regla de agrupación, el recuento
  real es trece, no once: la norma se contradecía con su propia tabla.
- `HOJA_DE_CRITERIOS.md` citaba una tercera cifra distinta, "veintiún papeles nominados", que no
  coincidía ni con el título de la norma ni con el recuento real de su tabla.
- **Corregido**: `NORMA_APM60.md` ahora dice "trece", que es lo que su propia tabla y su propia
  regla de agrupación dan. `HOJA_DE_CRITERIOS.md` se alineó a esa cifra corregida, porque la
  norma gobierna sobre la hoja de criterios.

## Reconsiderado (no era el error que parecía a primera lectura)

### 3. Los folios de las escalerillas, (118, 208, 212), en el Criterio 9 del punto cero

En una primera lectura marqué como contradicción que `HOJA_DE_CRITERIOS.md`, Criterio 9 (línea
33), siga citando los folios "(118, 208, 212)", mientras que `NORMA_APM60.md` usa exactamente
esos números como el ejemplo canónico de una coordenada que envejeció con el reflujo y que se
corrigió a "(96, 249, 253)". Pero el propio `HOJA_DE_CRITERIOS.md` encabeza esa sección como
"Punto cero" y advierte, en su sección siguiente, que "el punto cero de arriba queda como
registro del estado en que la auditoría comenzó; sus cifras corresponden a su fecha" — es decir,
declara por diseño que esos folios no se actualizan ahí, porque son fotografía histórica del 26
de agosto. Y en efecto, la sección "Estado al 27 de agosto de 2026" ya corrige el criterio 9 sin
arrastrar los folios viejos: dice que las escalerillas "hoy [están] nominadas por sección y no
por página". No lo toqué: no es una anomalía, es la convención del propio documento funcionando
como debe.

## Declarado, sin corregir (no hay manera de saber qué lado es el vigente)

### 4. Mancha simétrica: 11,15 cm declarados vs. ~11,08 cm que dan los puntos

`NORMA_APM60.md` §3 declara "2,2 cm a cada lado, 11,15 cm de justificación". `HOJA_DE_CRITERIOS.md`
da la misma mancha en puntos, 314,0 pt, que convertidos (1 cm = 28,3465 pt) dan ≈ 11,08 cm, no
11,15 cm — una diferencia de ~0,7 mm. Puede ser redondeo de la cifra en centímetros para el
lector y no una divergencia real de composición; no tengo forma de medir el PDF real para
decidir, así que lo dejo declarado y no lo corrijo.

### 5. "Cierre" como posible sexta portadilla, o solo nombre de familia de archivo

`NORMA_APM60.md` línea 397 describe "(umbral, las tres partes numeradas, cierre y apéndices)",
que a primera lectura podría sugerir una portadilla de "cierre" aparte de la tercera parte. Pero
`NORMA_APM60.md` §3 declara explícitamente "cinco portadillas de parte" y `CONTENIDO_DE_LAS_PARTES.txt`
(cuya aritmética de folios y páginas sin numerar verifiqué: cuadra exacta con las 283 páginas y
con el inventario de 8 páginas a sangre de `NORMA_APM60.md` §3) solo tiene cinco partes. Es más
probable que "cierre y apéndices" sea el nombre de la familia de archivos "50" del §1 (`50 cierre
y aparato`), no una sexta división impresa. Es ambigüedad de redacción, no un dato falso en
silencio, así que lo declaro sin corregirlo.

## Verificado sin error

- **281 → 283 páginas**: no es contradicción. `HOJA_DE_CRITERIOS.md` declara 281 en su punto cero
  (26 de agosto) y en su sección "Estado al 27 de agosto de 2026" anota explícitamente el cambio
  a 283, atribuido a `build.py`. Queda bien reconciliado dentro del propio documento.
- **`CONTENIDO_DE_LAS_PARTES.txt`**: la aritmética de folios y páginas sin numerar de las cinco
  partes cuadra exactamente con el total de 283 páginas y con el inventario de 8 páginas a sangre
  de `NORMA_APM60.md` §3 (2 forros + 5 portadillas de parte + 1 lámina de epígrafe).
- **`ENTRADAS_SIN_ANCLAJE.md`**: las ocho entradas resueltas se reparten en 4 "atribuidas e
  invocadas" + 4 "trasladadas a la nota", suma consistente con "ocho entradas"; la novena (El
  Colegio Nacional) queda aparte y explícitamente diferida. Sin contradicción interna.
- **`INSTRUCCIONES_DEL_TALLER.md`**: cita como "gobierno vivo" a `HALLAZGOS.md` y `LEEME.md` del
  propio proyecto, que no están entre los archivos compartidos conmigo — no es un error del
  documento, solo una fuente que no tengo a la vista (ya señalado en `LEEME.md` de esta carpeta).

## Nota de método

Las dos correcciones de arriba tocan solo la cifra en disputa y su frase inmediata; no toqué
ningún dato bibliográfico, testimonial ni de aparato (capa cero), y ninguna corrección aquí mueve
paginación del volumen. Si el compilador tiene acceso a `build.py` y a la relación real de
papeles, y la cifra correcta no es trece, esta corrección se revierte con la cifra que el
instrumento devuelva — la medición gobierna sobre la norma, y sobre esta auditoría también.
