# Hoja de criterios de auditoría · punto cero 26 de agosto de 2026

Convierte cada capa de la fase 2 en condición comprobable. Un criterio que no admite umbral
objetivo sin decisión del compilador se declara **pendiente**, se congela y no se renegocia.

## Punto cero

Motor XeLaTeX 3.141592653-2.6-0.999995 (TeX Live 2023). LuaHBTeX 1.17.0 también está instalado y
sería viable, pero la cadena entera está escrita para XeLaTeX y el cambio de motor es global
(fase 3, exige consulta): se audita sobre XeLaTeX y la migración sigue diferida a 2027.
Volumen 281 páginas, 439,37 × 651,97 pt (15,5 × 23 cm). Cero errores, cero desbordes de caja,
una línea floja de badness 5260, dos etiquetas duplicadas.
`APM60_Genealogia_Primera_edicion_digital_2026.pdf` sha256 9a6d66063ea115ae, 1 176 533 B.
`libro.pdf` sha256 fa697279e76a9ffe. `cubiertas.pdf` sha256 662f94332dc28d8f.

## Geometría y compaginación

1. Mancha: origen legal de la caja en 62,36 pt de lomo y de corte, ancho 314,0 pt. Exentas por
   registro: láminas a sangre, forros, portada, página legal. Tolerancia de protrusión óptica
   2,0 pt (microtipografía, deliberada).
2. Folio: banda única, declarada en `comun.py`; ningún glifo de texto por debajo de ella.
3. Cornisa: toda página de texto la declara; exención solo por declaración de la propia sección.
4. Colisiones: cero solapamientos de líneas, cero invasiones de texto sobre filete, imagen o folio.
5. Desbordes: cero cajas fuera del papel; cero `Overfull \hbox` en el registro.
6. Filetes: ancho, grosor y color han de constar en `auditoria.FILETES` (ocho pares legales).
7. Páginas a sangre: las ocho llevan marco crema a 1,12 cm del corte.
8. **Pendiente (congelado):** masa óptica, aireado, descansos de vista, reparto de huecos,
   columnado y aire del bloque de identificación. No hay umbral sin decisión del compilador.

## Microtipografía

9. Escalerillas: ninguna secuencia de más de dos líneas consecutivas terminadas en guion.
   Estado declarado: tres páginas incumplen (118, 208, 212); el remedio exige LuaLaTeX.
10. Líneas flojas: cero `Underfull \hbox (badness 10000)`. **Umbral vigente insuficiente:** una
    badness de 5260 no se denuncia hoy. Se propone 3000 como umbral de aviso.
11. Viudas y huérfanas: cero viudas; huérfanas toleradas hasta tres, declaradas.
12. Cuerpo: 11 pt en lectura seguida, 9 pt en consulta, aparato en 8,0 / 8,6 / 9,0. Sin escalones
    intermedios.
13. Ordinales, numerales y cifras: derivados, nunca transcritos. Ninguna cifra en prosa que un
    generador pueda calcular.
14. Signo ampersand proscrito; autoría múltiple en forma castellana («y», nombre de pila completo).

## Estructura y jerarquía

15. Toda unidad llamada desde `libro.tex` lleva marcador de navegación.
16. **Ninguna etiqueta definida dos veces** (criterio nuevo; hoy incumplido en dos).
17. Cero referencias cruzadas indefinidas.
18. Los aterrizajes del Contenido coinciden en tres fuentes: Contenido, `libro.aux` e índice del PDF.
19. Los cardinales que la prosa enuncia coinciden con el corpus del que se derivan.
20. Metadatos del sellado: título, autoría, asunto, palabras clave e identificador, derivados de
    la fuente.

## Aparato bibliográfico y onomástico

21. Toda cita del cuerpo tiene entrada en la relación; toda entrada de la relación es invocada.
22. Orden alfabético conforme a la norma española, con partícula onomástica capitalizada al abrir
    entrada y minúscula al restituir el orden natural.
23. Una obra se dice de una sola manera en todo el volumen.
24. Capa cero: entradas, citas textuales, nombres propios y cifras no se corrigen. **Se propone,
    no se ejecuta.**
25. Un identificador que no resuelve no prueba que la fuente no exista. Retirar una entrada de
    `fuentes_corroboradas.json` exige nueva consulta del ejemplar.

## Código de composición

26. Cero `\enlargethispage` y cero muletas de calibración manual.
27. Todo activo referido existe; ninguno se sustituye en silencio.
28. Un dato de forma (ancho, ordinal, cardinal, extensión) se declara una vez y se deriva.
29. Quien añada un eje lo añade a la lista; quien invoque la auditoría no enumera.
30. Todo detector ha de fallar cuando se le introduce el defecto que dice detectar.

## Estado al 27 de agosto de 2026

El punto cero de arriba queda como registro del estado en que la auditoría comenzó; sus cifras
corresponden a su fecha. Lo que desde entonces cambió, con su instrumento:

- Volumen de **283 páginas**; el entregable vigente y sus sumas las declara `build.py` en cada
  corrida y las sella en `bloques/`.
- Criterio 10, superado: los umbrales que absolvían pasaron a **cero con excepciones nominadas**
  (§2 de la norma). La línea floja de badness 5260 no se corrigió: queda nominada como excepción
  vigente, con su razón y su sección declaradas en la norma (`libro.tex:128`).
- Criterio 16, conforme: cero etiquetas duplicadas.
- Criterio 12, reformulado en §3 de la norma: la escala se declara **en la medida del PDF**
  (10,9 lectura; 9,0 consulta; 8,0/8,6 aparato; 6,6 nota) con trece papeles nominados, y el
  eje noveno la coteja entera.
- Criterio 6, ampliado: `auditoria.FILETES` (ocho pares) y `FILETES_A_SANGRE` para las páginas
  de composición propia.
- Criterio 30, vigente: la batería de sabotaje creció desde las ocho pruebas del punto cero y
  se reejecuta al cierre de cada tanda. El conteo no se transcribe aquí, porque envejece en
  cada tanda que añade una prueba: lo imprime `python3 sabotaje.py` al abrir.
- Criterio 9: las tres escalerillas siguen declaradas y heredadas a la edición accesible de
  2027, hoy nominadas por sección y no por página (una en las mesas del tercer periodo, dos en
  el in memoriam), porque el reflujo mueve el folio y no la causa.
- El criterio 8 (masa óptica y reparto de aire) sigue **pendiente y congelado**, sin umbral sin
  decisión del compilador.
