# Voice Profile — creación y uso del perfil vocal propio

Complementa §0.B y §5 del `SKILL.md`. Cubre el flujo operativo para construir
y mantener un perfil vocal reutilizable en Suno, calibrado al perfil sonoro
del autor (countertenor masculino en head voice, §1 del `SKILL.md`). Los
nombres de función exactos («Voice Profile», «Persona» u otro) cambian entre
versiones de la interfaz de Suno; verificar la denominación vigente antes de
seguir estos pasos al pie de la letra.

## 1. Qué es y para qué sirve

Un perfil vocal es un condicionamiento adicional que el modelo usa junto al
texto del style, entrenado o derivado a partir de generaciones previas (o de
audio propio, según la función disponible en el plan de suscripción). Sirve
para dos cosas distintas que conviene no confundir:

- **Consistencia entre tracks:** que la voz de un álbum completo se
  reconozca como «la misma» sin repetir la descripción vocal completa en
  cada style.
- **Anclaje contra deriva:** reduce, pero no elimina, la tendencia del
  modelo a derivar hacia timbres distintos en generaciones largas o en
  secciones de alta intensidad (§0.B del `SKILL.md`).

No sustituye al perfil vocal descrito en texto (§1, §2.4). Los dos actúan
juntos: el texto fija la intención, el perfil vocal fija la identidad
sonora entre generaciones.

## 2. Construcción del perfil

1. Generar varias tomas (mínimo cuatro o cinco) con el template base de §2.3
   del `SKILL.md`, variando ligeramente tempo y sección, hasta obtener al
   menos dos o tres que cumplan la checklist de §9 sin fry ni breaks a pecho.
2. Seleccionar las tomas más limpias como semilla del perfil. Descartar
   cualquiera con artefactos audibles: un perfil entrenado sobre una toma
   con fry hereda el fry.
3. Crear el perfil desde la interfaz de Suno vigente, con esas tomas como
   fuente. Nombrar el perfil de forma reconocible (por ejemplo, por el
   proyecto: «El Viaje — voz principal»).
4. Probar el perfil sobre una sección corta y nueva antes de usarlo en un
   track completo. Verificar contra la misma checklist de §9.

## 3. Uso en generación

- Audio influence / reconocimiento de voz: 55–75 % como punto de partida
  (tabla de §4 del `SKILL.md`); subir si la voz generada no se reconoce
  como la del perfil, bajar si arrastra artefactos de las tomas de origen.
- El perfil vocal no reemplaza las reglas de §2.4: seguir evitando
  `whispered`, `breathy` sin matizar, y `gothic romance` aunque el perfil
  esté activo, porque esos disparadores actúan sobre el texto, no sobre el
  perfil.
- Cambiar un solo parámetro a la vez al ajustar (regla operativa de §4) y
  anotar el resultado en el registro de §8, indicando qué perfil se usó.

## 4. Mantenimiento

- Revisar el perfil cada cierto número de tracks: si empieza a arrastrar
  artefactos que no tenían las tomas originales, puede requerir
  reentrenarse con tomas más recientes y más limpias.
- No mezclar tomas de perfiles distintos (por ejemplo, del álbum y de piezas
  sueltas) si sus perfiles de producción son distintos (§0 del `SKILL.md`
  distingue explícitamente ambos): la mezcla puede producir un perfil vocal
  que no corresponde a ninguno de los dos.
- Documentar la fecha de creación y de cada actualización del perfil; es
  relevante para el aporte humano declarado en `legal-distribucion.md` §1.

## 5. Límites conocidos

- El perfil vocal no fija tonalidad ni tempo (§6 del `SKILL.md` sigue
  aplicando sin cambios).
- Un perfil entrenado sobre pocas tomas (menos de cuatro) tiende a ser
  inestable entre generaciones distintas.
- No hay garantía de reconocimiento perfecto en secciones de alta densidad
  instrumental; si el audio influence alto no basta, reducir la
  instrumentación (§0.B del `SKILL.md`, mitigaciones operativas) antes de
  seguir subiendo el parámetro.
