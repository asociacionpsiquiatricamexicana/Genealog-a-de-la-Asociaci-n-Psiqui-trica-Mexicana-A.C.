# Ejemplos: tandas reales de este libro

No están aquí para copiarse, sino para calibrar qué cuenta como verificado en
este proyecto. En los tres casos el patrón es el mismo: **una medición
identifica el defecto, una medición confirma el arreglo**, y lo que no se pudo
arreglar queda declarado.

## 1. El defecto que no era el que parecía

El compilador reportó «espacios dobles» por todo el PDF. La reacción obvia
—buscar dos espacios seguidos en la fuente— dio **cero**: no había ninguno.

Lo que sí lo encontró fue medir el archivo: una sonda que recorre las 332
páginas y compara, glifo a glifo, cada hueco entre palabras con la mediana de su
propio renglón. Salieron las citas en bloque angostas y en cursiva, que se
justificaban de margen a margen y estiraban algunos renglones cortos hasta que
el hueco se leía como un espacio de más.

El arreglo fue de una línea —esas citas pasan a bandera, que es la convención
para la cita en bloque angosta— y la confirmación, la misma sonda: de varios
renglones sobre-justificados a ninguno.

**Lo que enseña:** el defecto que reporta el lector y la causa en el archivo
rara vez son la misma cosa. Medir antes de arreglar.

## 2. Un parche que toca lo que no debe tocarse

El libro sostenía dos versiones incompatibles de cómo se perdió el título de la
revista, y ninguna estaba sostenida por la fuente que se le atribuía: los dos
Testimonios citados decían menos de lo que se les hacía decir.

La corrección **no** tocó los Testimonios. Se retiró de ellos la atribución de
una conclusión que no era suya —eso sí es texto del libro, no de la persona— y
el dato pasó a declararse por conocimiento directo del autor, con testigo
nombrado y con su límite escrito en el apéndice de fuentes no consultadas.

```json
[
  {
    "id": "encuadre del Testimonio",
    "bloque": 1212,
    "viejo": "es la fuente principal sobre el expediente registral de la revista, cuya pérdida de título se produjo por omisión de renovación y no por litigio.",
    "nuevo": "es la fuente principal sobre la etapa de informalidad registral que precedió a la pérdida del título."
  }
]
```

**Lo que enseña:** capa cero no significa no corregir; significa corregir _lo
que el libro dice sobre_ la cita, nunca la cita. Y que un dato sin fuente
independiente se declara, no se rellena.

## 3. Una corrección con costo, medido antes de decidir

Doce líneas del PDF —las cubiertas y las tres portadillas de parte— no se
copiaban ni se encontraban al buscar: buscar «Primera parte» dentro del PDF no
devolvía nada, porque el seguimiento ancho hacía que el lector intercalara
espacios dentro de las palabras.

Bajarlo tenía un costo visible en las páginas más cuidadas del libro, así que no
se aplicó un valor único: se midió el techo de **cada** rótulo componiendo su
texto real, y cada uno recibió el máximo que admite. El ordinal de portadilla
hubo que ajustarlo dos veces, porque el sondeo aislado daba un valor que en el
libro seguía rompiendo —el umbral depende del par de letras concreto—.

Confirmación: de doce líneas rotas a ninguna, con el cotejo visual de cubierta y
portadilla antes y después para ver qué se había perdido.

**Lo que enseña:** cuando una corrección tiene costo, mídelo y decide sobre el
libro construido, no sobre el sondeo. Y deja escrito qué se perdió.

## El registro

Cada una de estas tandas dejó su sección en
`genealogia/REGISTRO_DE_CORRECCIONES.md` con la misma estructura: qué se
midió, qué se cambió, con qué se confirmó, y qué quedó declarado sin corregir.
Ese último apartado es el que hace útil el registro dentro de un año.
