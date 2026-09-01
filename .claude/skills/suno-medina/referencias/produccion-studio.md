# Producción, transiciones, mastering y exportación

Complementa §0.B, §5 y §6 del `SKILL.md`. Cubre lo que ocurre después de la
generación: cómo empalmar tramos, qué esperar de las herramientas de estudio
de Suno y qué queda mejor resuelto en un editor de audio digital externo
(DAW). Los nombres de función de Suno Studio cambian entre versiones;
verificar en la interfaz vigente antes de seguir un paso al pie de la letra.

## 1. Por qué generar por tramos

§0.B del `SKILL.md` ya establece el límite: forma larga y modulación de
tonalidad colapsan más allá de unos pocos minutos, y el códec neuronal
degrada con la duración. La consecuencia operativa es generar en tramos de
dos a tres minutos y empalmar fuera de Suno. Esta sección cubre cómo.

## 2. Empalme de tramos en DAW

1. Exportar cada tramo por separado, con margen de uno o dos segundos antes
   y después del punto de corte previsto.
2. Alinear por tempo, no por duración nominal: el BPM real de Suno deriva
   ±3 respecto al pedido (§6 del `SKILL.md`); dos tramos con el mismo BPM
   nominal pueden no estar exactamente en fase.
3. Crossfade corto (cien a trescientos milisegundos) en el punto de corte,
   ajustado por oído; un corte seco es audible incluso cuando el tempo
   coincide.
4. Si el corte cae dentro de una frase vocal, preferir cortar en un silencio
   o en el final de una palabra, nunca a mitad de una vocal sostenida.

## 3. Transiciones dentro de una misma generación

Cuando la transición cabe dentro de un solo tramo (por ejemplo,
verso→coro), el recurso es de texto, no de edición posterior:

- `smooth legato transitions` en el style ayuda a que Suno no corte
  abruptamente entre secciones (§5.2 del `SKILL.md`).
- El pre-chorus obligatorio de §3.4 existe precisamente para evitar el salto
  brusco; omitirlo traslada el problema de vuelta a esta sección.
- Un `[Breakdown]` o `[Interlude]` explícito en la letra da a Suno un lugar
  donde bajar densidad antes de subir de nuevo, en vez de forzar la subida
  directa.

## 4. Artefactos de mezcla — Suno sheen, metallic shimmer, bleed

Remitido desde §5.2 del `SKILL.md`. Son artefactos del códec, no de la
mezcla posterior, así que la corrección real ocurre antes de exportar:

- **Sheen / metallic shimmer:** brillo metálico en agudos, más audible con
  más de cuatro elementos instrumentales sonando a la vez. Reducir
  instrumentación (§0.B del `SKILL.md`) es la vía principal; un EQ de corte
  suave sobre ocho kilohercios en post ayuda pero no elimina el artefacto.
- **Bleed:** fuga tímbrica entre instrumentos que deberían sonar separados
  (por ejemplo, piano que arrastra textura de synth pad). Más frecuente en
  mezclas densas; la separación por stems (§5) ayuda si el bleed es
  tolerable en al menos un stem limpio.
- **Timing en rejilla:** los patrones rítmicos generados tienden a
  cuantizarse de forma perceptible, especialmente en `programmed drums`.
  Pedir `live drums` explícitamente en el style reduce el efecto pero no lo
  garantiza; corregir en DAW con humanización manual si el corte es
  sensible.

## 5. Separación de stems

La separación es posterior a la generación y de calidad variable (§0.B del
`SKILL.md`). Antes de depender de un stem específico:

1. Generar y separar sobre una toma ya aprobada, nunca sobre un borrador.
2. Escuchar cada stem por separado a volumen alto antes de usarlo: el bleed
   entre instrumentos (§4) suele ser más audible aislado que en la mezcla
   completa.
3. Si el stem vocal trae artefactos que la mezcla completa disimulaba,
   descartar la separación para ese track y trabajar sobre la mezcla
   íntegra.

## 6. Mastering

Suno entrega una mezcla, no un máster. Para publicación:

- Normalizar a un nivel de referencia coherente con el destino (streaming,
  video, físico); los estándares de loudness varían por plataforma y
  conviene confirmarlos antes de exportar la versión final.
- Aplicar corrección tonal suave si el sheen de §4 persiste tras reducir
  instrumentación.
- Conservar siempre una copia de la mezcla previa al mastering: si el
  máster introduce un artefacto nuevo, hay que poder volver atrás sin
  regenerar en Suno.

## 7. Exportación — formatos

Confirmar en la interfaz vigente de Suno qué formatos de exportación están
disponibles según el nivel de suscripción (WAV sin pérdida frente a MP3
comprimido, con o sin metadatos, con o sin stems). Para trabajo de mastering
posterior, exportar siempre en el formato de mayor fidelidad disponible;
convertir a formato de distribución solo en el paso final.
