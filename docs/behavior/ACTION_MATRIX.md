# ACTION MATRIX — acción → precondición → transición → respuesta

**Estado:** especificación verificable de EXP-0042. Los códigos de autorización se prueban mediante [reference evaluator](../../tools/authority_reference.py) y [ghost runner](../../tools/simulate_trace.py); el juego C/Godot aún **no** presenta estas pantallas. Catálogo de motivos: [feedback_catalog.json](../../data/design/feedback_catalog.json). \`S\` significa **estado institucional inmutable** (reloj, posición, fase, permisos, conocimiento, confianza); \`S'\` es nuevo estado tras aceptar.

| Acción | Estado observable / guard | Transición institucional | Feedback PETSCII propuesto |
| --- | --- | --- | --- |
| Ir Registry desde Courtyard | Sala=Courtyard, existe salida; m0 | \`S→S'\` sala Registry, m2 | \`REGISTRY / 28 MIN / CASE\` |
| Ir Archive desde Courtyard | Sin salida directa | \`S→S\`, \`INVALID_EXIT\` | \`NO EXIT / GO VIA REGISTRY\` |
| Leer carátula | Registry; m2 | \`CASE_BASIS\` adquirido, m3 | \`CASE BASIS RECORDED\` |
| Leer carátula desde Courtyard | Sala equivocada | \`S→S\`, \`WRONG_ROOM\` | \`REGISTRY REQUIRED / 28 MIN\` |
| Pedir permiso sin justificación | Registry; sin \`CASE_BASIS\`; m2 | \`S→S\`, \`MISSING_CASE_BASIS\` | \`SECRETARY: BASIS REQUIRED\` |
| Pedir permiso con justificación | Registry; \`CASE_BASIS\`; m3 | \`ARCHIVE_CASE_0042\` solo, m4 | \`CASE PERMIT GRANTED\` |
| Pedir permiso duplicado | Ya concedido | \`S→S\`, \`PERMISSION_ALREADY_GRANTED\` | \`ALREADY APPROVED / VISIT ARCHIVE\` |
| Pedir a interlocutor incompetente | Actor != Secretaría | \`S→S\`, \`ACTOR_NOT_AUTHORIZED\` | \`FIND SECRETARY\` |
| Solicitud sin Secretaría disponible | Secretaría fuera de atención | \`S→S\`, \`ACTOR_UNAVAILABLE\` | \`NOT AVAILABLE / CHECK SCHEDULE\` |
| Leer Archive sin permiso | Archive, no \`ARCHIVE_CASE_0042\` | \`S→S\`, \`MISSING_CASE_PERMISSION\` | \`CASE PERMIT REQUIRED\` |
| Leer Archive antes de m10 | Permiso sí, fase \`registered\` | \`S→S\`, \`INVALID_CASE_STAGE\` | \`REVIEW NOT OPEN\` |
| Esperar 3 min desde m7 | Espera deliberada | \`S→S'\` m10, fase \`archive_review\` | \`ARCHIVE REVIEW OPEN\` |
| Leer Archive en revisión | Permiso, Archive, fase revisión | \`S→S'\` agrega \`HISTORY\`, +1 min | \`HISTORY VERIFIED\` |
| Validar sin \`HISTORY\` | Archive, fase revisión | \`S→S\`, \`MISSING_HISTORY\` | \`EVIDENCE MISSING\` |
| Validar sin \`READY\` | Archive, revisión, HISTORY | \`S→S\`, \`MISSING_READY\` | \`NOT READY / CHECK STATUS\` |
| Validar con ambos hechos | Archive, revisión, HISTORY + READY, m27 | \`S→S'\` \`validated\`, m28 | \`EXP-0042 VALIDATED\` |
| Validar fuera de Archive | Sala no autorizada para acción | \`S→S\`, \`WRONG_ROOM\` | \`ARCHIVE REQUIRED\` |
| Validar desde m30 | Plazo vencido | \`S→S\`, \`DEADLINE_EXPIRED\` | \`EXPIRED / REVIEW OUTCOME\` |
| Consultar el estado | Cualquier sala | \`S→S\` (read-only) | \`ROOM / CASE / DEADLINE / NEXT\` |
| Cambiar cámara | Cualquier sala | \`S→S\` (presentación pura) | Misma información, nueva composición |

## Contrato de UX, no «permiso = game over»

Todo rechazo debe adjuntar: \`reason_code\`, actor o subsistema responsable, razón visible sin datos confidenciales, **minutos restantes**, y al menos un \`next_action\` viable o la orientación de revisión si el plazo venció. Los textos PETSCII de arriba son **mockups**, sujetos a longitud final, codificación de caracteres y pruebas visuales. El sistema no puede cargarle minutos ni bajar la confianza *simplemente por pulsar* una petición rechazada.

**Las excepciones con coste son actos nuevos del jugador:** esperar explícitamente, viajar por otra ruta, tramitar documentación o divulgar una afirmación que un actor compruebe como falsa (esto último queda en M2). Una autoridad negando una consulta no es un castigo moral.

## Separación de responsabilidades

- **Kernel (M1):** decide guardas y transiciones; conoce datos canónicos.
- **Knowledge projection (M1):** filtra lo que el jugador puede saber; el HUD no muestra motivaciones ocultas de NPC.
- **Feedback adapter (M1 pendiente):** mapea códigos estables a respuestas legibles; no escribe en el kernel.
- **Narrative Director (M2):** elige orden/presentación de consecuencias ya generadas, sin crear hechos.
- **Camera (M3):** encuadra; no dispara tiempo, autorización o cambio de fase.

La tabla representa contratos **propuestos y algunos ejecutables en host**; no equivale a 19 mecánicas C64 certificadas.
