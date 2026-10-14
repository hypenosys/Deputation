# Playtesting Protocol — EXP-0042 paper ghost / jugador sin instrucciones

**Estado:** protocolo propuesto. **No se ha realizado un playtest humano** ni se ha observado una UI ejecutable en C64 o Godot. El único «ghost» disponible es un **replay de datos** validado por Python. No presentar sus decisiones como comportamiento de una persona real.

## 1. Dos modalidades

**Ghost determinista (automático):** ejecutar desde la raíz:

\`\`\`bash
python -m tools.simulate_trace --trace data/world/simulation_trace.json
python -m tools.simulate_trace --trace data/world/simulation_trace_failure.json
python -m tools.simulate_trace --trace data/world/simulation_trace.json --format json > /tmp/deputation-trace.json
python -m unittest discover -s tests -v
\`\`\`

La terminal imprime cada acción, minuto simulado, estancia, resultado, denegación/alternativa y estado terminal. El archivo JSON de informe registra hashes por paso. Los hitos m10/m15/m27 se aplican exactamente al cruzarlos. **No** aparecen colas, relaciones sociales, incidentes de red, NPC autónomos ni cámaras: siguen sin integrar.

**Playtest humano en papel (posterior):** preparar una hoja con mapa **Courtyard–Registry–Archive** sin mostrar de entrada las condiciones de victoria; mostrar objetivos, 30 minutos del expediente y una línea de estado legible. El moderador aplica manualmente la [ACTION MATRIX](behavior/ACTION_MATRIX.md), anota decisiones y sirve feedback; evita explicar la solución. El participante no lee [GAME_LOOP](GAME_LOOP.md), el arco narrativo completo, JSON de fixtures ni reglas ocultas hasta terminar.

## 2. Onboarding sin instrucciones

**Texto inicial mostrado:** «EXP-0042. Revisión extraordinaria. El cierre del expediente está previsto en 30 minutos institucionales. Registro conserva la carátula; Archivo custodia la documentación. Puedes consultar el estado o desplazarte. Tu objetivo es acreditar una contradicción antes del cierre.»

**Instrumentación:** observador registra antes de cada paso \`room\`, \`minute\`, \`stage\`, \`known_facts\`, \`permissions\`, acción, código de denegación, feedback que se entregó, siguiente acción elegida, tiempo real y una nota de sorpresa/frustración. Un observador **no puede cambiar el estado** para facilitar el guion.

Preguntas de observación (sin interrumpir la partida): ¿El jugador identifica qué significa acreditar? ¿Comprende si leer el caso cambia su posibilidad legal? ¿Interpreta «no» como instrucción o como castigo? ¿Distingue minuto simulado y tiempo real? ¿Percibe que volver sobre sus pasos cuesta minutos? ¿Entiende por qué \`READY\` no está aún disponible? ¿Reconoce qué hizo posible validar? ¿Puede explicar la derrota?

## 3. Tabla de expectativas vs evidencia hoy

| Situación | Lo que esperaríamos que vea el jugador | Lo que existe actualmente en Deputation |
| --- | --- | --- |
| Inicio sin tutorial | Objetivo y reloj, navegación clara | Fixture JSON y documentación; **no pantalla jugable** |
| Petición sin legitimación | «Secretaría: falta motivo; lee carátula» | Código \`MISSING_CASE_BASIS\` y feedback JSON; **no UI** |
| Desplazamiento | Estancia nueva y minutos consumidos | Runner Python con sala/minuto; **no escena** |
| Llegar antes de revisión | «No abierta todavía» y condición verificable | Código \`INVALID_CASE_STAGE\`; **no personaje animado** |
| Tramo m20–24 | Incidente comprensible y evitable | **No ejecutado en ghost**: mecánica ABBI observada pero fuera de M1 |
| Victoria | Validación visible + consecuencias | \`validated\` en replay; **no final visual** |
| Derrota | Plazo agotado + causa/alternativa | \`expired\` y rechazo; **no pantalla final** |
| Cambio de cámara | Misma situación institucional | Sin interfaz de cámara en este repo |

## 4. Ghost de seis ciclos: auditoría de legibilidad

| Ciclo | Riesgo de incomprensión | Señal que debe entregar la UI | Criterio de prueba |
| --- | --- | --- | --- |
| C01 m0→4 | ¿Por qué me niega Secretaría? | \`MISSING_CASE_BASIS\`, minutos 28, carátula en Registry | El usuario intenta subsanar, no reiniciar |
| C02 m4→11 | Permiso vs expediente listo | Explicar que falta fase, no otra credencial | Comprende que debe esperar/consultar |
| C03 m11→18 | Confundir \`REVIEW\` con \`READY\` | Separar hechos y estado legal | Predice por qué falla validar |
| C04 m18→24 | Viajar de más y equivocarse de sala | Marca de coste antes de moverse; causa \`WRONG_ROOM\` | Sabe explicar la pérdida de tiempo |
| C05 m24→27 | Espera artificial | Indicador causal de \`READY\` y reloj | Sabe qué gana/pierde esperando |
| C06 m27→28 | Victoria sin catarsis | «Prueba admitida», consecuencias, posibilidad de revisar cronología | Verbaliza qué acreditó |

El [replay de pérdida](../data/world/simulation_trace_failure.json) ofrece un contraejemplo: el jugador conserva permiso, pero espera hasta m30. Una negativa final **no** resta memoria ni confianza. El moderador pregunta: «¿Qué decisión habrías modificado y por qué?»

## 5. Plantilla de registro y umbrales de aceptación propuestos

- Sesiones: primero **5 pruebas exploratorias** sin tutorial, después una segunda ronda tras corregir fallos; la cantidad es una propuesta de diseño, no participantes reclutados.
- Registrar: tiempo para primera decisión útil, porcentaje de rechazos cuya causa se comprende, errores de reloj, tasa de avance sin intervención del moderador, duración por ciclo y sentido declarado de agencia.
- Umbral previo a Godot (propuesta): **4/5** participantes describen el objetivo en sus palabras, **4/5** distinguen tiempo real/simulado y **4/5** identifican una corrección tras el primer rechazo; los cinco deben poder explicar por qué terminó su partida. No es un criterio estadístico de producto final.
- Parada inmediata si el facilitador necesita inventar un permiso, saltar un plazo o divulgar una pista que el kernel no permite. Se anota como **defecto del diseño**, no como error del jugador.
- Prioridad de reparación: **sin alternativa tras DENY > estados ilegibles > coste sorpresivo > fatiga por repetición > preferencias de texto/cámara**.

El artefacto reproducible y la sesión humana son tipos de evidencia distintos. No prometer satisfacción, agencia percibida ni duración hasta observar personas.
