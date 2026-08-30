---
paths:
  - "genealogia/taller/bookstyle_extraido.js"
  - "genealogia/taller/assets/*.js"
---

# El módulo de estilo tiene un gemelo

`bookstyle_extraido.js` decide cómo se ve cada bloque, y
`assets/a4d0e564-9e95-4331-9b24-990858d9e4e7.js` es la copia que viaja dentro de
los flipbooks. **Toda edición de estilo va a los dos.** Tocar uno solo produce
un PDF y un flipbook que ya no dicen lo mismo, y la diferencia no se nota hasta
que alguien compara página por página.

## El seguimiento tipográfico tiene techo

Por encima de cierto valor de `letter-spacing`, el lector de PDF intercala
espacios dentro de las palabras: el texto deja de copiarse y de encontrarse al
buscar, aunque en la página se vea perfecto. Llegó a haber ciento cincuenta y
una líneas así, entre ellas las tres portadillas de parte y el título de
cubierta.

El techo no es común: depende del cuerpo, de si el rótulo lleva dígitos —los de
Cormorant son los primeros en ceder— y de si va en versalita, que el navegador
sintetiza a un cuerpo menor. `sondas/techo_por_elemento.py` lo mide componiendo
el texto real de cada rótulo; conviene medir en vez de suponer, y decidir sobre
el libro construido, porque el umbral cambia según el par de letras concreto.

## El espacio entre palabras se cuenta dos veces

El seguimiento se suma también tras el carácter de espacio, de modo que el hueco
entre palabras crece el doble que el hueco entre letras y se lee como un espacio
doble. El ayudante `css()` lo compensa solo, con un `word-spacing` negativo; lo
que se escriba como CSS plano o como objeto de estilo fuera de `css()` queda
fuera de esa compensación y hay que compensarlo a mano.
