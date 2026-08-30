# Cómo se versiona este libro

El repositorio guarda un libro que se corrige por tandas, no un programa que se
desarrolla por funcionalidades. Eso cambia lo que es un buen commit aquí.

## La rama

El trabajo va en una rama `claude/…`, nunca directamente en la rama por defecto.
La rama vive mientras dura la campaña de correcciones y se sigue por una sola
solicitud de fusión en borrador; no se abre una por tanda.

## Una tanda, un commit

Una tanda es un conjunto de correcciones que se decide, se aplica, se verifica y
se publica junto. Antes de confirmarla:

1. **Recomponer y verificar.** El PDF se rehace entero y se comprueba con
   `cmp.py` y con las sondas que correspondan a lo que se tocó. El número de
   diferencias de `cmp.py` es la señal: si sube tras un cambio que debía ser
   solo visual, algo se movió que no debía.
2. **Anotar en el registro.** `genealogia/REGISTRO_DE_CORRECCIONES.md` recibe una
   sección por tanda con qué se cambió, **cómo se comprobó** y qué quedó
   declarado sin corregir. El registro es parte del libro, no documentación
   accesoria: es donde consta que una decisión editorial se tomó y con qué
   fundamento.
3. **Copiar los entregables.** El PDF sellado y los flipbooks se copian a
   `genealogia/`, que es lo que el lector recibe.

## El mensaje del commit

Dice qué se corrigió, por qué era un defecto y **con qué se comprobó**. Las
cifras concretas valen más que los adjetivos: «de ciento cincuenta y una líneas
rotas a doce» dice algo; «mejora la calidad tipográfica» no dice nada.

Evita anunciar como corregido lo que no se verificó, y declara explícitamente lo
que se dejó sin corregir y por qué. Un límite declarado es información; un
límite callado es una trampa para quien venga después.

No se incluye el identificador del modelo en mensajes de commit, títulos ni
cuerpos de solicitud de fusión.

## Lo que no se confirma

Los artefactos que el proceso genera —`pdfs/`, `*.pkl`, `mypages.json`,
`__pycache__`— no van al repositorio: se rehacen desde el taller. Lo que sí va es
el entregable publicado en `genealogia/` y el taller que lo produce.
