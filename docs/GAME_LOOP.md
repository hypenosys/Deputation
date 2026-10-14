# THE DEPUTATION — Gramática ludológica y game loop canónico

**Estado:** baseline de diseño para **EXP-0042**; solo el ghost runner Python es ejecutable. No afirmar que existe UI jugable, C64 port o libre diálogo. [Arco del caso](design/EXP-0042_case_arc.md) · [micro-loop](design/moment_to_moment.md) · [traza reproducible](../data/world/simulation_trace.json).

## Verbo definitorio: ACREDITAR

**El jugador investiga para acreditar una contradicción ante una institución que decide qué puede darse por válido.** No es un gestor omnisciente: transforma *observación* en *prueba admisible* y *prueba admisible* en *validación*, bajo tiempo, autoridad y ubicación. La estructura causal es: **localizar → leer/contrastar → solicitar → actuar → verificar consecuencia → replantear**. «Sabes la verdad» no basta si no demuestras cadena de procedencia; «te creen» no basta para obtener una autorización.

## Unidad y relojes

La **unidad primaria** es **un expediente** con inicio, deadline y cierre verificable, no un día de oficina. Una **microdecisión** es una acción con resultado observable; un **ciclo** contiene un objetivo local, una o varias decisiones, respuesta y reajuste (objetivo: **2–3 minutos reales**, hipótesis a validar con jugadores). El expediente EXP-0042 utiliza **30 minutos simulados**, el reloj solo avanza mediante acciones explícitas válidas (viaje, espera, lectura, tramitación) o hitos de simulación durante ese avance. Las negativas puras cuestan **cero** minutos. Consultar estado y cambiar de cámara no cuestan tiempo.

## Vocabulario del jugador (M1)

| Verbo | Requisito | Coste simulado | Resultado |
| --- | --- | --- | --- |
| Moverse | Arco entre salas, costo de tabla | 2 o 3 min según [mundo](../data/world/vertical_slice.v1.json) | Cambia estancia |
| Leer carátula | Registry, plazo no vencido | 1 min (valor de oráculo propuesto) | Conocer \`CASE_BASIS\` |
| Solicitar permiso | Registry, Secretaría, \`CASE_BASIS\` | 1 min si concede; 0 si niega | \`ARCHIVE_CASE_0042\` |
| Consultar archivo | Archive, permiso y \`archive_review\` | 1 min si procede | \`HISTORY\` con procedencia |
| Esperar | Elección explícita | Minutos declarados | Se disparan hitos en orden |
| Consultar estado | Cualquier sala | 0 | Objetivo/plazo/fase, sin hechos secretos |
| Validar | Archive, revisión y \`HISTORY\` + \`READY\` | 1 min si procede | Caso \`validated\` |
| Cambiar vista | Cualquier estancia | 0 | Solo presentación, sin mutación |

**Hitos heredados como referencia:** m10 mueve el expediente a \`archive_review\` (secuencia de ABBI); m15 aporta \`REVIEW\`; m27 aporta \`READY\`. El oracle M1 no ejecuta aún m18 cambio de relación ni m20–24 incidente de conexión, que pertenecen a otros sistemas.

## Cuatro ciclos completos (ejemplo de partida, no playtest observado)

**1. Apertura (m0→4):** Courtyard → Registry (**m2**); pedir permiso sin carátula → **DENY/MISSING_CASE_BASIS**, reloj aún m2, autoridad explica cómo proceder; leer carátula → m3 y \`CASE_BASIS\`; solicitar de nuevo → permiso específico concedido, m4. **Cierra el ciclo con nueva capacidad**, no con un marcador abstracto.

**2. Fricción institucional (m4→11):** Registry → Archive (m7); consultar antes de la fase habilitada → **DENY/INVALID_CASE_STAGE** sin coste; esperar voluntariamente 3 min → m10, \`archive_review\`; leer documentación autorizada → m11, \`HISTORY\`. **Cierra con prueba**, y el error previo era subsanable.

**3. Una mala decisión comprensible (m11→18):** El jugador regresa a Registry (m14), inspecciona estado sin coste, espera a m15 (hito \`REVIEW\`), vuelve a Archive (m18) y valida demasiado pronto → **DENY/MISSING_READY**. **Cierra con información útil**, aunque ha gastado tiempo real de simulación en dos viajes.

**4. Compresión y desenlace (m18→28):** Se aventura a Registry (m21), intenta leer Archive desde sala errónea → **DENY/WRONG_ROOM**; regresa a Archive (m24); verifica que falta \`READY\`; espera expresamente hasta m27; valida a m28. La presión no surge de cámaras ni escenas guionizadas, sino del **coste de escoger volver, esperar y probar demasiado pronto**.

El [JSON de seis ciclos](../data/world/simulation_trace.json) subdivide los dos últimos ciclos para aportar seis unidades inspeccionables. Su contraparte [perdedora](../data/world/simulation_trace_failure.json) demuestra cierre por tiempo: cuando la espera alcanza m30, la validación se deniega explicando la pérdida. No se manipula retrospectivamente una decisión para imponer un final.

## Victoria, derrota y cierres deliberados

- **Victoria M1:** transición explícita a \`validated\` en Archive, con fase y hechos requeridos, **acción iniciada antes de m30** y terminada dentro del límite. Conocer \`HISTORY\` no es victoria por sí mismo.
- **Derrota M1:** la ventana alcanza m30 sin validación; se registra \`expired\` y se explica qué no se logró. No se borra conocimiento ni se desencadena una muerte ficticia.
- **Resultado moral:** un éxito procesal puede seguir siendo éticamente incompleto; **no** existe todavía cómputo automático de «complicidad» ni finales ramificados implementados. Son propuestas M2 ([agencia](PLAYER_AGENCY.md)).

**Anti-objetivo:** nunca convertir un fallo legible en «no pasa nada». Cada \`DENY\` ha de indicar responsable, causa segura, minutos restantes y una ruta de respuesta. Véase [ACTION_MATRIX](behavior/ACTION_MATRIX.md).
