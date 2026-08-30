---
paths:
  - "genealogia/taller/assets/*.bin"
---

# La fuente de verdad del libro

Este archivo es todo el texto del volumen y no hay copia autorizada en ningún
otro sitio: un JSON con `blocks`, `toc` y `anchors`. Cada bloque tiene su tipo
(`t`) y su lista de fragmentos (`parts`), con las marcas de cursiva, versalita,
negrita, superíndice o dirección.

**Toda inserción o borrado de bloques desancla el Contenido.** Sus entradas
guardan índices de bloque; si los bloques se mueven, el Contenido remite a
páginas equivocadas y nada avisa. Ya ocurrió una vez, con entradas que erraban
hasta treinta páginas en los apéndices. Después de cualquier edición
estructural hay que reanclarlo por identidad —buscando el bloque por su texto,
no por su posición— y comprobarlo con `sondas/verificar_toc.py`.

Al editar en lote conviene exigir que cada reemplazo aparezca **exactamente una
vez** y abortar si no: un parche que casa dos veces, o ninguna, es un error
silencioso que solo se descubre al leer el PDF impreso.

Y antes de tocar cualquier cita, asiento bibliográfico o nombre firmado, vale la
capa cero que describe `.claude/CLAUDE.md`.
