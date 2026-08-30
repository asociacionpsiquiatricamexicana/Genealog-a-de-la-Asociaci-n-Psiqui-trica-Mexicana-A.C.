# Instrucciones permanentes del taller · Genealogía de la Asociación Psiquiátrica Mexicana, A.C.

Para toda sesión que trabaje en este directorio. El gobierno vivo está en
`NORMA_APM60.md` (reglas exigibles), `HALLAZGOS.md` (registro H-1 en
adelante, con la relación de pendientes al cierre del archivo) y `LEEME.md`
(compilación); el estado del proyecto, en el documento
`claude/bitacora-genealogia.md` del Proyecto. Ante divergencia, la norma
gobierna y la medición gobierna sobre la norma.

## Reglas de conducta, no negociables

1. **Capa cero.** Citas textuales ajenas, entradas bibliográficas, datos
   duros, nombres propios y fragmentos en otra lengua son intangibles: se
   copian verbatim, jamás se corrigen ni se retiran en silencio. Las capas de
   aparato bibliográfico y onomástico no son autocorregibles: se propone, no
   se ejecuta.
2. **Paginación.** Ninguna corrección que mueva paginación se ejecuta sin
   declarar cuánto la mueve, medido antes y después.
3. **Derivar, no transcribir.** Lo que se transcribe envejece. Toda cifra,
   ordinal, nombre de entregable o conteo se deriva de su fuente; quien añada
   un eje lo añade a la lista única y quien invoca no enumera.
4. **Verificación honesta.** No se declara conforme lo que no se comprobó.
   Todo detector nuevo recibe su prueba de sabotaje (`sabotaje.py`), y la
   batería completa se reejecuta al cierre de cada tanda. La familia de la
   conformidad falsa (§11 de la norma) se consulta ante todo rótulo verde.
5. **Anomalía sistemática y consistente**: presúmase decisión deliberada y
   consúltese, salvo cuando produzca un dato falso en silencio, en cuyo caso
   se declara aunque no se corrija. Si una instrucción del compilador
   contradice la medición, se le contradice con la medición a la vista.
6. **Trato.** Máximo tres preguntas por turno. «Gremio», nunca
   «corporación»; «Asociación Psiquiátrica Mexicana, A.C.» con «A.C.» en
   prosa. Ausencias de entrevista: «pendiente al cierre; podrá incorporarse a
   un trabajo posterior», nunca una negativa personal. Nada privado de socios
   o expresidentes vivos; el motivo de salud del Dr. Del Bosque no se imprime
   sin su autorización expresa por escrito.
7. **Identificadores.** Un identificador que no resuelve dice que el registro
   no lo tiene, no que la fuente no exista; retirar una entrada de
   `fuentes_corroboradas.json` exige nueva consulta del ejemplar. Los sitios
   `gob.mx` bloquean consulta automatizada; el blog institucional tiene spam
   inyectado y no se cita.

## Flujo de trabajo

Compilar y verificar: `python3 build.py` (cadena completa; salida 0 o no hay
entrega). Tras cada tanda: batería de sabotaje, registro del hallazgo con su
número de serie, `python3 diagnostico.py --sellar`, confirmación con
etiqueta, y espejos del Proyecto al día (`claude/hallazgos-genealogia.md`,
`claude/bitacora-genealogia.md`, `claude/norma-editorial-genealogia.md`; la
actualización de espejos es manual y queda a cargo de quien cierra la
tanda). Los archivos subidos al Proyecto son de solo lectura para las
sesiones: los renombres se proponen en `claude/nomenclatura-proyecto.md`.
