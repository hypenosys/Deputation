# EXP-0042 — Feedback de denegación

**Estado:** catálogo de diseño + microcontrato Python probado por tests; **no** es una UI existente en C64/Godot. Fuente de datos: [feedback_catalog.json](../../data/design/feedback_catalog.json). Los motivos no son texto generado libremente: el motor devuelve un código y la presentación lo traduce.

Toda respuesta a una acción denegada presenta: **quién** denegó o qué subsistema impidió la acción, **motivo** comprensible sin divulgar información secreta, **tiempo simulado restante** (`max(0, 30-minute)`) y **siguiente acción concreta**. Una denegación no modifica permisos, ubicación, fase, reloj, confianza, conocimiento ni colas de eventos. Consultar feedback es lectura pura. No se emiten estados especiales de «game over silencioso».

| Acción denegada | Motivo visible / responsable | Siguiente posibilidad | Estado |
| --- | --- | --- | --- |
| Solicitar permiso | Falta justificación del caso / Secretaría | Leer carátula en Registry | Referencia |
| Solicitar permiso | Permiso específico ya concedido / Secretaría | Consultar Archive | Referencia |
| Leer archivo | Falta `ARCHIVE_CASE_0042` / Archivero | Solicitar permiso en Registry | Referencia |
| Leer archivo | Fase inapropiada / Archivero | Consultar fase del caso | Referencia |
| Validar caso | No está en `archive_review` / Oficina | Completar revisión | Referencia |
| Validar caso | No consta `HISTORY` / Oficina | Consultar Archive | Referencia |
| Validar caso | Falta `READY` / Oficina | Esperar hito verificable | Referencia |
| Cualquier interacción | Estás en la sala equivocada / Sistema | Viajar a sala exigida | Referencia |
| Cualquier interacción | Venció la ventana de m30 / Sistema | Revisar resultado y consecuencias | Referencia |
| Cualquier interacción | Interlocutor sin competencia / Sistema | Localizar responsable | Referencia |
| Solicitud / consulta | Funcionario no disponible / Sistema | Revisar agenda | Referencia |
| Movimiento | No hay salida a la sala elegida / Sistema | Elegir salida válida | M1 pendiente |
| Solicitud | Servicio de Registry ocupado / Registro | Consultar cola | M2 pendiente |
| Consulta opcional | Confianza insuficiente / Archivero | Presentar evidencia válida | M2 pendiente |
| Archivo | Incidente bloquea índice / Registro | Consultar incidencia | M2 pendiente |

## Proyección de feedback (ejemplo ilustrativo)

```text
SECRETARÍA — SOLICITUD DENEGADA
Motivo: falta una justificación registrada para EXP-0042.
Plazo de revisión: 11 minutos simulados restantes.
Siguiente paso: leer la carátula del expediente en Registry.
Estado del caso: SIN CAMBIOS.
```

**Importante:** el rechazo de una orden y una acción válida que consuma tiempo para esperar, subsanar o desplazarse son cosas distintas. Una solicitud denegada cuesta **0 minutos**; decidir esperar explícitamente sí puede consumirlos. El ajuste futuro de agendas o confianza no puede usar el feedback para producir efectos secundarios. Fuente normativa local: [contrato de referencia](../../tools/authority_reference.py); [test de idempotencia](../../tests/test_denied_permit_idempotence.py).
