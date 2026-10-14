# Narrative Engine — híbrido, causal y auditable

**Decisión:** arquitectura **híbrida** de **simulación autoritativa determinista** + **puesta en escena escrita**. El motor de reglas genera qué ocurrió; el Narrative Director decide qué hecho ya ocurrido merece mostrarse, a quién, cuándo y desde qué punto de vista. Los checkpoints aseguran ritmo legible, pero nunca cambian retrospectivamente un hecho ni conceden permisos.

## 1. Estratos

\`\`\`text
PLAYER INPUT
    ↓
INSTITUTION KERNEL (rules/state, pure transitions, timers, actors)
    ├── World truth: exact room, minute, phase, incident, permissions
    ├── Provenance: who witnessed what; which case can disclose it
    └── Events: ordered, timestamped, source-linked
    ↓
KNOWLEDGE PROJECTION (what this observer is entitled to know)
    ↓
NARRATIVE DIRECTOR (selection and pacing; no state mutation)
    ├── Beat templates: authored prose, sounds, cinematic shot hints
    ├── Conditions: only visible event/state, never guessed secrets
    └── Priorities: urgent deadline > action rejection > new evidence > ambiance
    ↓
UI / PETSCII / GODOT (presentation only)
\`\`\`

No LLM en runtime C64. Si en herramientas de autoría se usa un LLM, sus propuestas se serializan, se revisan y se validan como contenido **offline**, jamás como sentencia del estado institucional. El registro de eventos y la procedencia son verificables con replay y hashes de estado.

## 2. Fuentes de verdad: lo que es script y lo que emerge

| Elemento | Procedencia | ¿Puede cambiar estado? | Ejemplo |
| --- | --- | --- | --- |
| Topología y costes | Datos canónicos del mundo | Sí, si el jugador se mueve válidamente | Courtyard→Registry +2 |
| m10 \`archive_review\` | Hito programado heredado de ABBI | Sí, mediante avance de minutos | El caso llega al Archivo |
| m15 \`REVIEW\`; m27 \`READY\` | Eventos programados en prototipo | Sí, a su minuto exacto | READY no se anticipa |
| Permiso específico | Elección + guardas | Sí, si concede autoridad competente | \`ARCHIVE_CASE_0042\` |
| Denegación | Resultado del kernel | **No** | \`MISSING_CASE_BASIS\` |
| Plantilla de texto | Contenido de autoría | **No** | «Secretaría necesita el motivo» |
| Confianza, rumores y colas | Futuro M2 causal | Solo tras acción comprobada | Mentir al archivero deja rastro |
| Plano y música | Adaptador escénico | **No** | Contrapicado al revelar sala |

**M1** usa una combinación de hitos temporales fijos y resultados contingentes por acciones. Esto es híbrido, pero no equivale todavía a un mundo social emergente completo. El catálogo ABBI observa \`DPT-M-038\` como selector narrativo host, no como compositor en C64; no elevar evidencia hasta probar el port.

## 3. Contrato de selección de beats

Propuesta de interfaz futura, sin código ejecutable aún:

\`\`\`json
{
  "event_id": "EVT-0042-0017",
  "minute": 7,
  "kind": "request_denied",
  "source_actor": "SECRETARY",
  "case_id": "EXP-0042",
  "reason_code": "MISSING_CASE_BASIS",
  "observer": "PLAYER",
  "visible": true,
  "beat": "permit_denied_missing_basis",
  "camera_hint": "close_up",
  "world_mutation": false
}
\`\`\`

Reglas: (1) solo se puede emitir un beat cuyo \`event_id\` existe y pertenece al conocimiento/autorización del observador; (2) determinación por prioridad y orden estable \`(minute, priority, event_id)\`; (3) no emitir dos revelaciones de un secreto por un mismo evento salvo intención explícita; (4) el silencio nunca equivale a aceptar una acción; (5) derivar la urgencia del minuto simulado, no del tiempo real de visualización; (6) presentar una negación no cambia el hash institucional. Los planos, subtextos y *foreshadowing* pueden añadir tono, no hechos no autorizados.

## 4. Ejemplo de emergente legible

El jugador llega a Archive en m7 y pide \`HISTORY\` (permiso concedido, pero caso aún \`registered\`). El kernel responde \`INVALID_CASE_STAGE\`; el director selecciona un beat corto que expresa **falta de fase**, con reloj aún en m7 y siguiente paso de consulta/espera. El jugador elige esperar hasta m10, el hito cambia la fase, y ahora se obtiene \`HISTORY\` por acción explícita. Los hechos son los mismos en cualquier cámara; el orden y frustración proceden de decisiones. Una ruta que espera hasta m30 produce un cierre sin validación, no un *plot twist* escrito para el jugador.

## 5. Contrato de aceptación antes de M2/M3

Se requieren tests para dos rutas con distinto estado terminal, denies idempotentes, ausencia de divulgación no autorizada, replay bit a bit estable, prioridad de eventos determinista y vista neutral. Los [traces del ghost](../data/world/simulation_trace.json) verifican **solo un oráculo M1 de referencia**. No prueban autoría audiovisual, NPC sociales, motores 3D ni escenas. Las consecuencias éticas deberán tener fuentes y destinatarios observables, no un contador de moralidad oculto.

El jugador puede sospechar que el mundo miente. **El kernel no debe mentir sobre sus propias reglas.**
