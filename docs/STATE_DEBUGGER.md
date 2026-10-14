# State Debugger (M3) — diseño para Godot, no escena implementada

El inspector deberá mostrar en tiempo real **el estado autoritativo del kernel**, no valores deducidos de la cámara ni propiedades inventadas por la UI. En la primera entrega bastará un panel read-only conectado por un adaptador, sin editor que pueda «arreglar» partidas alterando permisos manualmente.

## Panel propuesto

- **Timeline:** minuto simulado, plazo, eventos de transición (origen, reloj, prioridad e ID).
- **Caso:** ID, sala del expediente, fase, requisitos para la siguiente transición, y fuente de cada cambio.
- **Jugador:** sala, verbos disponibles, permisos acotados, conocimiento por procedencia y estado final.
- **Actores (M2):** sala/agenda, hechos observados, confianza por observador y próximas ventanas de atención.
- **Guardas:** motivo de la última aceptación/rechazo, decisión, reloj antes/después, diferencias de estado. Denegación exige `pre_sha256 == post_sha256`.
- **Presentación:** modo de cámara actual y hash institucional: cambiarla jamás varía el hash.
- **Reproducción:** importar acciones de `data/world/simulation_trace.json` y ver el mismo hash paso a paso en un entorno host/Godot, sin cambiar la verdad para obtener una imagen deseada.

## Contrato técnico

Propuesta de snapshot de depuración (no es protocolo productivo implementado):

```json
{
  "minute": 18,
  "case_id": "EXP-0042",
  "case_stage": "archive_review",
  "player_room": "ARCHIVE",
  "known_facts": ["CASE_BASIS", "HISTORY", "REVIEW"],
  "permissions": ["ARCHIVE_CASE_0042"],
  "last_action": "validate_case",
  "last_reason_code": "MISSING_READY",
  "unchanged": true,
  "state_sha256": "<sha256 de estado canónico real>"
}
```

El campo de hash se calcula del estado real; el literal es solo una plantilla de diseño. No expone secretos que el jugador no conoce en un build comercial: el modo developer permite inspeccionar, pero logs accesibles al usuario siguen políticas epistemológicas. Exportar la secuencia como JSON legible, con inputs y hashes, para diagnóstico de errores. Sin incorporar trazas con datos personales reales.

## Gate de aceptación

Inyectar una misma serie de acciones en el oráculo host y en el adaptador Godot, comparar campos canónicos y todos los códigos. Reproducir los 10 fixtures denegados, ambos endings y cambios de cámara; comprobar hash invariante ante render y negativo idéntico. Los hashes entre dos implementaciones solo se equiparan tras normalizar tipos, orden, versión de esquema y serialización de bytes. Ninguna discrepancia se oculta mediante un hotfix visual.
