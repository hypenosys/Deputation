# Design Baseline — THE DEPUTATION / EXP-0042

**Versión:** baseline de preproducción, 2026-10-14. **No atribuir** cifras de intención a resultados de un playtest humano ni al ejecutable C64. Este documento bloquea decisiones de alcance para una vertical slice que se pueda **jugar**, no solo estudiar.

## Qué juego es

**Logline jugable:** eres una investigadora interina que debe acreditar una contradicción institucional en un expediente, obteniendo acceso legítimo a información y eligiendo dónde gastar tiempo antes de un cierre irreversible. La institución no es un enemigo con IA mágica: es una red de reglas, trabajadores con conocimientos limitados y plazos.

- **Verbo:** **acreditar**, mediante investigar → justificar → solicitar → comprobar → validar.
- **Unidad primaria:** **expediente cerrado en una sesión**; no se modela un día laboral entero en M1.
- **Escenario:** Courtyard (1) ↔ Registry (2) ↔ Archive (3), \`EXP0042\` con reloj ficticio de m0–30.
- **Duración esperada:** **12–20 minutos reales por primera sesión de una única misión**, hipótesis a medir. Cada ciclo pretende durar ~2–3 minutos reales y la traza ganadora tiene 6 ciclos; los 30 minutos **son simulados**, no un temporizador de 30 minutos del usuario.
- **Presentación objetivo:** PETSCII, tres cámaras propuestas (isométrica/raycast/wireframe) sobre el mismo estado; no condicionan la progresión.
- **Audiencia:** personas que disfrutan la investigación, los dilemas institucionales y descubrir reglas, sin exigir conocimientos administrativos reales.

## Estado del jugador, ramas y finales

**Variables autoritativas M1 propuestas:** sala (3), minuto entero (0–30 y posible expiración), fase (\`registered\`, \`archive_review\`, \`validated\`), permiso \`ARCHIVE_CASE_0042\` (sí/no), conocimiento \`CASE_BASIS\`, \`HISTORY\`, \`REVIEW\`, \`READY\` (bits), objetivo visible y resultado. Confianza y social memory se reservan para M2: *no sumarlas a la explosión de estados como si ya existieran*.

No declarar «N vidas» ni **un número único de combinaciones**: producto cartesiano sin restricciones no representa estados alcanzables y los tiempos/acciones inválidos producen muchos duplicados. Definir **tres clases macroscópicas de resultado** en el diseño: \`validated\` (implementable en oráculo), \`expired\` (implementable en oráculo) y \`under_review\` (reservado para revisión formal M2, **no** implementado). Dejar separadas victoria administrativa y justicia moral; añadir finales ramificados solo si guardas y hechos reproducibles los sustentan.

## Replay value

**Promesa de rejugabilidad:** probar «¿qué pasaba si esperaba?», «¿qué cambia si pido información antes?», «¿puedo evitar viajes inútiles?» y reconstruir el fracaso leyendo causas. La primera iteración ofrece **contrafactuales de coste y conocimiento** sobre un solo caso, no una historia ilimitada. El [ghost ganador](../data/world/simulation_trace.json) acaba en m28; el [ghost perdedor](../data/world/simulation_trace_failure.json) demuestra que m30 sin validar es pérdida. Son guiones reproducibles de entradas, **no** datos reales de jugadores.

**Motivo para repetir:** aprender una regla y aplicarla mejor, tomar decisiones morales distintas (M2) y comparar un historial verificable. Si la segunda pasada es solo memorizar dónde hacer clic, falta variación de consecuencias e interacción social. En M2 se exigirán tres vías de resolución con precondiciones distintas, sin regalar información ni derechos.

## Reglas de diseño congeladas para M1

1. Los rechazos no mutan el mundo, el reloj, la confianza ni el conocimiento; causan **feedback y orientación**.
2. La consulta de estado y la cámara son observaciones, nunca acciones con coste.
3. El permiso para EXP-0042 no es entrada a todo Archive ni equivale a conocimiento verificado.
4. La victoria solo ocurre mediante una validación **explícita** en la sala correcta y dentro del plazo.
5. \`READY\` solo procede del hito autorizado m27; el director no lo fabrica.
6. Mantener 15 observaciones para M1, 23 para M2 y 7 para M3, preservando todos los IDs del archivo.
7. No aprobar la calidad jugable con pruebas puramente de esquema. Requiere protocolo ciego de papel y luego pruebas del ejecutable.

## Definition of fun / rechazo del tedious simulator

El jugador debe identificar un plan, afrontar un obstáculo comprensible, cambiarlo por información/permiso y sentir **consecuencias legibles**. Una denegación sin causa o sin alternativa es un fallo de UX. La repetición mecánica de colas sin nuevas decisiones se elimina o condensa. La humillación burocrática puede ser tema, pero no interacción vacía. M1 no se considera completo hasta observar una partida humana sin intervención explicativa.

**No hacemos aún:** simulador de día laboral, manipulación política libre, NPC omniscientes, IA generativa on-device, sanción moral automática, Godot finalizado ni hardware certificado. Consultar [GAME_LOOP](GAME_LOOP.md), [PLAYER_AGENCY](PLAYER_AGENCY.md), [NARRATIVE_ENGINE](NARRATIVE_ENGINE.md), [CONSTRAINTS](CONSTRAINTS.md) y [PLAYTESTING_PROTOCOL](PLAYTESTING_PROTOCOL.md).
