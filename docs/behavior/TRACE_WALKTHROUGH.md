# EXP-0042 — Walkthrough observado del replay host (NO playtest humano)

**Evidencia:** [GitHub Actions #38589387641](https://github.com/hypenosys/Deputation/actions/runs/38589387641), ejecución Quality concluida con **success** para el código de la rama \`feature/gameplay-grammar-simulation-traces\` a fecha **2026-10-14**. Este resumen refleja lo que produjo **el oráculo Python**. No son sensaciones de un jugador, vídeo de Godot ni pantalla del C64.

## Ruta ganadora — 6 ciclos, 20 acciones

| # | Acción | Min. tras acción | Sala | Resultado |
| ---: | --- | ---: | --- | --- |
| C01.1 | Ir a Registry | 2 | Registry | MOVED, coste +2 |
| C01.2 | Pedir permiso sin carátula | 2 | Registry | **MISSING_CASE_BASIS**, estado sin cambio |
| C01.3 | Leer carátula | 3 | Registry | CASE_FILE_READ; aprende CASE_BASIS |
| C01.4 | Solicitar permiso nuevamente | 4 | Registry | PERMIT_GRANTED; permiso específico |
| C02.1 | Ir a Archive | 7 | Archive | MOVED, coste +3 |
| C02.2 | Leer antes de la revisión | 7 | Archive | **INVALID_CASE_STAGE**, estado sin cambio |
| C02.3 | Esperar 3 | 10 | Archive | WAITED; expediente entra en archive_review |
| C02.4 | Leer historial autorizado | 11 | Archive | ARCHIVE_READ; aprende HISTORY |
| C03.1 | Volver a Registry | 14 | Registry | MOVED, coste +3 |
| C03.2 | Consultar estado | 14 | Registry | STATUS_VIEWED, sin coste |
| C03.3 | Esperar 1 | 15 | Registry | WAITED; aprende REVIEW |
| C03.4 | Volver a Archive | 18 | Archive | MOVED, coste +3 |
| C03.5 | Intentar validar temprano | 18 | Archive | **MISSING_READY**, estado sin cambio |
| C04.1 | Volver a Registry | 21 | Registry | MOVED, coste +3 |
| C04.2 | Intentar leer Archive desde Registry | 21 | Registry | **WRONG_ROOM**, estado sin cambio |
| C04.3 | Regresar a Archive | 24 | Archive | MOVED, coste +3 |
| C05.1 | Validar sin READY | 24 | Archive | **MISSING_READY**, estado sin cambio |
| C05.2 | Esperar 3 | 27 | Archive | WAITED; obtiene READY |
| C05.3 | Consultar estado | 27 | Archive | STATUS_VIEWED, sin coste |
| C06.1 | Validar expediente | 28 | Archive | **CASE_VALIDATED** |

**Terminal comprobado:** \`validated\` en m28. Hash canónico SHA-256 del último estado: \`3f2cffcf3f93ad93f052c5744052745c1c9fabf83d8be8a0aaa2efd4056b42b0\`.

## Ruta perdedora — 3 ciclos, 9 acciones

| # | Acción | Min. tras acción | Sala | Resultado |
| ---: | --- | ---: | --- | --- |
| L01.1 | Ir a Registry | 2 | Registry | MOVED |
| L01.2 | Leer carátula | 3 | Registry | CASE_FILE_READ |
| L01.3 | Solicitar permiso legítimo | 4 | Registry | PERMIT_GRANTED |
| L01.4 | Ir a Archive | 7 | Archive | MOVED |
| L02.1 | Esperar 3 | 10 | Archive | WAITED; abre la revisión |
| L02.2 | Leer Archive | 11 | Archive | ARCHIVE_READ |
| L02.3 | Esperar 13 | 24 | Archive | WAITED |
| L03.1 | Esperar 6 | 30 | Archive | WAITED; vence plazo |
| L03.2 | Validar fuera del plazo | 30 | Archive | **DEADLINE_EXPIRED**, sin mutación |

**Terminal comprobado:** \`expired\` en m30. Hash canónico SHA-256 del último estado: \`1695277900bbd9ee212cd0d5ba70d4e14ef85ec9088f1939a06092529b1eb521\`. El mensaje final corresponde a un código verificable y propone revisar el resultado; **no** concede un permiso ni reabre el expediente.

## Lectura de diseño

La diferencia que importa **no** es un final animado: la primera partida convierte una justificación en permiso y una lectura en prueba **a tiempo**; la segunda reúne pruebas, pero elige esperar hasta que ya no puede validarlas. Las negativas no son castigo de reloj; **moverse y esperar sí**. El caso conserva el plazo m30 en ambas rutas.

**Gaps reconocidos:** el oráculo no mide tiempo real de 2–3 minutos por ciclo, no observa respuestas humanas y no simula m18 relación social ni la incidencia m20–24. Tampoco certifica FPS, memoria, coste por frame o PETSCII en hardware. Los informes detallados y hashes por paso se regeneran con:

\`\`\`bash
python -m tools.simulate_trace --trace data/world/simulation_trace.json --format json
python -m tools.simulate_trace --trace data/world/simulation_trace_failure.json --format json
\`\`\`
