# Genealogía de la Asociación Psiquiátrica Mexicana, A.C.

Este repositorio publica un libro, no un programa: `genealogia/` contiene el PDF
del volumen del Sexagésimo Aniversario, sus dos flipbooks, el registro de cada
tanda de correcciones y la norma editorial. El taller que lo compone vive en
`genealogia/taller/`, y su `LEEME.md` explica el proceso y sus trampas.

## La regla que no se negocia: capa cero

No se altera **nunca** el texto ajeno. Eso incluye:

- lo que va dentro de una cita atribuida a una persona (los bloques `epi`, `ent`
  y los cuerpos de Testimonio);
- los asientos bibliográficos, con sus títulos, revistas y direcciones;
- el nombre de un autor tal como lo firma en cada publicación, aunque en otra
  parte del libro se escriba distinto.

Corregir ahí no es mejorar el libro: es falsear una fuente. Si algo parece un
error dentro de una cita, se señala en una nota, no se toca el texto.

Antes de confirmar una tanda, lee `docs/git-instructions.md`: qué se verifica
primero, qué se anota en el registro y qué debe decir el mensaje del commit. No se
carga solo; hay que abrirlo.

## Cómo se trabaja

El compilador dirige por tandas. Cada tanda se verifica **midiendo el PDF
construido**, no leyendo el código: `genealogia/taller/sondas/` reúne las
comprobaciones escritas a lo largo del proyecto, y cada una responde una
pregunta concreta sobre el archivo. Al cerrar una tanda se anota en
`genealogia/REGISTRO_DE_CORRECCIONES.md` qué se cambió, cómo se comprobó y qué
quedó declarado sin corregir.

Un dato que no se sostiene con fuente independiente se declara como tal —el
libro tiene apéndices para eso—; no se rellena con lo que parece probable.

## Convenciones de la prosa

Las cifras y los años van con letra en la prosa corrida («mil novecientos
sesenta y seis»). El numeral se conserva donde es correcto: dentro de citas, en
los asientos bibliográficos y en las cajas de datos.
