# Metadatos de distribución — plantilla multiplataforma (copiar por pista)

Citada desde `SKILL.md` §7, flujo de exportación/distribución, y desde
`legal-distribucion.md`. Transcrita del documento del autor sin cambios de
contenido; los corchetes señalan lo que remite a un documento no incluido en
este paquete.

Pista: __________ | Fecha de redacción: __________

## Campos comunes a toda plataforma (redactar una sola vez, reutilizar)

- Título exacto (idéntico byte a byte en todas partes): __________
- Artista: José Carlos Medina-Rodríguez
- Álbum: In Absentia (MMXXVI)
- Número de pista / ordinal: __________ (verificar contra
  `00b-DECISIONES-PENDIENTES.md` si está en disputa — documento no incluido
  en este paquete; declarado ausente)
- Compositor / letra: José Carlos Medina-Rodríguez
- Productor / arreglo / mezcla / masterización: José Carlos Medina-Rodríguez
- ℗ 2026 José Carlos Medina-Rodríguez
- Fecha de lanzamiento: __________
- Idioma de la letra: español
- ISRC: __________ (ver `00d-ISRC-UPC-TRACKER.md` — no incluido en este
  paquete; se asigna UNA vez, nunca se regenera por plataforma. El único
  ISRC confirmado que llegó a esta skill es el de Demian, transcrito en
  `letras/03_Demian_letra_v1_PUBLICADA.txt`: UPC 885975779393, ISRC
  QZMHK2632356)
- UPC/catálogo del álbum (si aplica): __________

## Divulgación de IA — mecanismo real según la ruta vigente

Ver `00g-RUTA-OPERATIVA-REAL.md` (corregido el 13 de agosto de 2026; no
incluido en este paquete) para el detalle completo. Para toda pista, la ruta
confirmada es Suno → selección propia → SoundCloud (subida primaria, ISRC de
origen) → exportación desde SoundCloud a Spotify. La divulgación de IA se
declara en el formulario de SoundCloud, ya usado y validado con Demian; queda
pendiente confirmar si la exportación a Spotify hereda esa divulgación o
exige declararla de nuevo.

| Plataforma | Mecanismo de divulgación | Texto/casilla exacta |
|---|---|---|
| SoundCloud (ruta primaria, todas las pistas) | casilla de subida + créditos en descripción | «contiene música generada con IA: sí»; crédito con etiqueta DDEX «AI-assisted» |
| Spotify (vía exportación desde SoundCloud) | por confirmar: ¿hereda la divulgación de SoundCloud, o exige formulario propio? | por confirmar en el primer uso real |
| YouTube Music | herencia de lo publicado, o subida paralela propia | verificar si aplica etiqueta adicional de «contenido alterado por IA» en la consola |
| CD Baby | no admite música generada con IA | excluido; no forma parte de esta ruta |

## Taxonomía de género — no es idéntica entre plataformas, mapear cada vez

| Plataforma | Género primario propuesto | Género secundario propuesto |
|---|---|---|
| SoundCloud (real, caso Demian) | Alternative | Indie Rock |
| Spotify (vía distribuidor) | por definir | por definir |
| YouTube Music | por definir | por definir |

## Descripción / sinopsis

Un párrafo de posicionamiento narrativo (referencia intertextual de la pista
dentro del monomito) más créditos, divulgación y símbolo ℗. Ver `03-demian/`
(carpeta de trabajo del autor, no incluida en este paquete) como precedente
de formato ya usado.

## Letra cantada real

Para la descripción, si la plataforma la admite, copiar la letra tal como se
cantó, no el texto de generación: si hubo desviaciones de ejecución
(ritardando, omisión de una sección), documentarlas antes de pegarlas. Ver
`letras/03_Demian_letra_v1_PUBLICADA.txt`, que ya documenta sus dos
desviaciones respecto del prompt de entrada, como precedente de cómo hacerlo.

## Casillas operativas

- Descargas: activadas / desactivadas (nota: la exclusividad de distribución
  suele requerir descargas desactivadas en la plataforma de origen si hay
  distribuidor de por medio)
- Licencia: todos los derechos reservados
- Contiene muestras/samples de terceros: no (verificar higiene con
  `checklist-saneamiento.md`, no incluido en este paquete)

## Verificación final antes de publicar

1. Título idéntico en las cuatro superficies (SoundCloud, envío al
   distribuidor, y lo que Spotify/YouTube Music mostrarán una vez
   propagado).
2. ISRC copiado del tracker, no reintroducido a mano por plataforma.
3. Ordinal de pista resuelto, no en disputa.
4. Checklist de saneamiento completa antes de este documento.
