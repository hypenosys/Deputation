# Player agency — libertad, complicidad y vulnerabilidad

**Declaración central:** THE DEPUTATION no debe ser un simulador de obedecer pantallas. Debe permitir al jugador **usar las reglas para disputar una versión oficial**, asumiendo que no todo puede resolverse simplemente con buena voluntad. Esta es una propuesta de diseño, no un sistema social C64 existente.

## Tres relaciones del jugador con el poder

| Acto | Libre (decisión con efecto) | Cómplice (acepta coste moral) | Víctima (frontera externa) | Evidencia M1 |
| --- | --- | --- | --- | --- |
| Leer la carátula | Elegir qué prueba investigar y cuándo | Convertir una duda en mero trámite sin contrastar | No acceder sin visitar Registry | Lectura/coste probado en ghost runner |
| Solicitar permiso | Preparar \`CASE_BASIS\` antes de pedirlo | Presentar solo la versión administrativa más favorable | Secretaría puede negar por reglas objetivas | Permit/denial host probado |
| Moverse | Elegir ruta y pagar tiempo | Abandonar una línea de prueba por rapidez | La topología solo permite Courtyard ↔ Registry ↔ Archive | Grafo y costes en ghost runner |
| Leer Archive | Confrontar una afirmación con fuente | Ocultar una contradicción conocida (**M2**) | Sin \`ARCHIVE_CASE_0042\` no hay divulgación | \`HISTORY\` host con guardas |
| Esperar | Decidir si sacrifica minutos a cambio de otro hito | Elegir comodidad mientras terceros esperan (**M2**) | m27 \`READY\` no se adelanta por voluntad | Espera y milestone host |
| Validar | Actuar al contar con hechos suficientes | Dar por válida una omisión cuando existe otra vía (**M2**) | Sin fase/READY/plazo no puede forzar un sí | Guardas probadas en host |
| Recurrir tras derrota | Investigar por qué perdió y repetir | Aceptar cierre administrativo injusto (**M2**) | Plazo de m30 irreversible en este expediente | Rechazo de deadline host |

**Agencia auténtica:** dos órdenes distintos de acciones deben poder producir costes y conocimiento distintos, sin una transición guionizada que borre esa diferencia. El ejemplo ganador llega a validación en m28, mientras que el alternativo acaba en m30 con expediente sin validar. El primer desenlace no es un premio cinematográfico arbitrario: el estado sustenta la consecuencia.

**Agencia ilusoria (evitar):** opciones diferentes con idéntico coste, texto y destino sin razón narrativamente justificable; un rechazo que muta el caso aunque UI diga que no; pistas que aparecen por arte del director; minutos que pasan al cambiar la cámara. Si se necesita un acto inevitable, se declara como frontera institucional con causa perceptible.

## Escalada de complicidad moral (hipótesis M2)

- **Acto I — Curiosidad y capacidad (0–5 min reales):** el jugador entiende qué puede hacer y consigue una primera mejora legítima. El sistema no penaliza experimentar con acciones sin coste.
- **Acto II — Fricción (5–12):** la institución impone la diferencia entre *información verdadera* y *información admisible*. Aparecen tentaciones de simplificar el expediente o de presionar a un funcionario; **ninguna trampa moral automática** mientras no exista elección con alternativas reales.
- **Acto III — Responsabilidad (12–18+):** entregar la prueba puede perjudicar a un trabajador o dejar fuera a afectados si solo se acredita la parte conveniente. La moralidad no se reduce a confianza numérica; el juego debería reconocer *qué información se presentó/omitió*, *quién recibió consecuencias* y *qué sabía el jugador al decidirlo*.

**No prometer lo que aún no se puede jugar:** en M1 hay agencia procesal, pero la complicidad moral es en gran parte **representación escrita**, sin rama funcional implementada. El paso a M2 deberá añadir una decisión de coste moral auditable (beneficia a alguien y perjudica a otro), otra ruta viable, memoria por observador y dos resultados distintos medidos en tests. La confianza afecta disponibilidad, **nunca concede competencia legal** ([matriz social](../data/mechanics/social_dynamics.json)).

## Diseño contra la impotencia tediosa

El jugador merece un rechazo comprensible, una pista no falsa para reconstruir la causa, decisiones que importen y momentos de alivio **ganados**. El expediente puede fracasar sin hacer fracasar a la persona; la pantalla final explica qué hizo, qué no pudo probar y qué quedó pendiente. La incomodidad institucional es una temática, **no una excusa para UI opaca**. Debe playtestearse la distinción entre ansiedad dramática y frustración por falta de feedback.
