# Checklist pre-generación — plantilla (copiar por pista/intento)

Citada desde `SKILL.md` §9. Transcrita del documento del autor sin cambios de
contenido; solo se añadió esta cabecera y las notas entre corchetes que
señalan qué remite a un documento no incluido en este paquete.

Pista: __________ | Fecha: __________ | Intento/versión: __________

1. ¿Tiene semilla de audio anexada? Si sí, ¿ya se midió con
   `analisis-semilla-medina` (BPM, tonalidad, Camelot)? La semilla manda; sin
   medición no se declara tonalidad ni tempo. [Ver `mediciones-semillas.md`
   §2 para los márgenes de incertidumbre reales por rango de tempo.]
2. ¿La letra pasó verificación mecánica de conector inicial en cada verso?
3. ¿La letra tiene cero puntos, cero punto y coma, cero dos puntos (salvo
   ¡! ¿? sancionados)?
4. ¿Tiene blancos entre estrofas donde el aire lo pide?
5. ¿Está dentro de 5000 caracteres, y del rango de 60 a 80 versos únicos (o
   el rango vigente)?
6. ¿El Style está dentro de 1000 caracteres?
7. ¿El Style contiene algún token del léxico proscrito (§11.1/§11.2): stacked,
   double-tracked, legato, de-essed, falsetto (proscrito-condicional),
   sibilantes en positivo, tape/cassette/saturation, balanced, extended,
   resolved/resolving, Camelot o nombres de modo? [El documento que define
   §11.1/§11.2 —el léxico proscrito completo— no se incluyó en este paquete;
   declarado ausente, no reconstruido. Mientras falte, aplicar por analogía
   las reglas ya verificadas de `SKILL.md` §2.4 y §5.1, que cubren varios de
   estos mismos términos con otra numeración.]
8. ¿Alguna negación («-token», «no», «without») quedó dentro del campo Style
   en vez del Exclude?
9. ¿El Exclude contiene las sibilantes de cajón y los términos permanentes
   del proyecto? [El núcleo de treinta y dos términos antiglotales y
   antisibilantes referido en `album-in-absentia.md` §3 tampoco se recibió;
   mismo tratamiento: declarado ausente.]
10. ¿La tonalidad declarada en el Style coincide con la medición de la
    semilla, si existe? [Ver `mediciones-semillas.md` para las doce pistas
    del álbum ya medidas.]
11. ¿El cierre usa `[Ending]` + `[Fade Out]`, o hay razón documentada para
    desviarse?
12. ¿Los tags de dirección están en inglés aunque la letra esté en español?
13. ¿Se registró el paquete completo (letra + style + Exclude + sliders +
    duración) en el registro §8 de `SKILL.md` antes de disparar la
    generación?

## Cómo se relaciona con §9 del `SKILL.md`

Esta checklist es previa a la generación; la de §9 del `SKILL.md` es previa a
la entrega del paquete al usuario. No son la misma lista y no se sustituyen
entre sí: correr esta antes de generar, y la de §9 antes de entregar el
resultado.
