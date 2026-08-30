# Documentos de norma editorial del proyecto

Estos cinco archivos los aportó el autor el 28 de agosto de 2026 y describen el sistema real
de composición y auditoría del volumen: fuentes LaTeX (`libro.tex`, `secciones/*.tex`) compiladas
con XeLaTeX sobre la clase `memoir`, y un conjunto de scripts de verificación propios (`build.py`,
`norma.py`, `diagnostico.py`, `sabotaje.py`, `auditoria.py`, `trazabilidad.py`) que hacen cumplir
diez cláusulas normativas exigibles.

**Ninguno de esos archivos fuente ni scripts está disponible en esta sesión ni en este
repositorio.** Lo que esta sesión tiene es el paquete HTML autónomo del lector digital (el
flipbook, en `../Genealogia_APM_Flipbook__plano.html` y su versión con desempaquetado en
`../Genealogia_APM_Flipbook__Standalone__corregido.html`), que es una reproducción posterior y
aproximada del mismo contenido, no la fuente de composición canónica.

## Qué se pudo verificar y corregir con estos documentos

- **Extensión del volumen: 283 páginas.** `CONTENIDO_DE_LAS_PARTES.txt` y `HOJA_DE_CRITERIOS.md`
  confirman esta cifra de forma independiente entre sí y coinciden con lo que ya declaraba el
  informe del barrido léxico (`../informes/`). Se corrigió la portada y la ficha de catalogación
  del volumen, que habían quedado en 262 páginas por una corrección anterior basada en una única
  fuente que resultó no ser la vigente.
- Verificación puntual de una regla de estilo («gremio», nunca «corporación»): sin incumplimientos
  en la prosa propia del volumen.

## Qué no se pudo hacer

No fue posible compilar el volumen canónico (`APM60_Genealogia_Primera_edicion_digital_2026.pdf`,
283 páginas, dividido en las cinco partes A-E que describe `CONTENIDO_DE_LAS_PARTES.txt`) ni
ejecutar `norma.py`, `build.py`, `diagnostico.py` ni `sabotaje.py`, porque sus fuentes no están
disponibles aquí. El PDF de este repositorio (`../APM60_Genealogia__corregido.pdf`) es una
reconstrucción del **contenido** corregido a partir del lector digital, compuesta a la misma caja
del volumen (15,5 × 23 cm) y con tipografía real, pero no está certificada contra la norma
tipográfica completa que describen `NORMA_APM60.md` y `HOJA_DE_CRITERIOS.md` (jerarquía exacta de
cuerpos, filetes catalogados, cero líneas flojas, cero viudas, capa de texto legible en rótulos
espaciados, etc.), que exige compilar desde las fuentes LaTeX originales con los scripts propios
del proyecto.

`ENTRADAS_SIN_ANCLAJE.md` documenta una decisión ya resuelta por el autor el 26 de agosto de 2026
sobre ocho entradas bibliográficas; se conserva aquí como referencia y no requirió ninguna acción
de esta sesión.
