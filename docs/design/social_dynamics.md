# EXP-0042 — Dinámica social 5 × 5

**Estado:** diseño de balance M2; no existe en el ejecutable jugable. Fuente estructurada: [social_dynamics.json](../../data/mechanics/social_dynamics.json). Se distinguen cinco tipos de interlocutores y cinco **cambios observables** de confianza en una relación concreta observador→jugador.

El valor muestra ajuste en **minutos simulados de espera de la próxima atención elegible**, nunca una modificación del deadline ni un pase de seguridad. El tiempo de espera efectivo se limita inferiormente a cero. Por ejemplo, si la cola base son 4 minutos, una bonificación `−2` la reduce a 2, no a −2. Un agente desconfiado puede exigir revisión formal; no puede falsear qué hechos existen.

| Tipo de actor | Caída grave (−2) | Caída leve (−1) | Sin cambio (0) | Mejora leve (+1) | Mejora alta (+2) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Empleado Registro | +6 min | +3 | 0 | −1 | −2 |
| Secretaría | +8 min | +4 | 0 | −1 | −2 |
| Archivero | +6 min | +3 | 0 | −1 | −1 |
| Supervisor del caso | +10 min | +5 | 0 | −2 | −3 |
| Enlace con testigos | +4 min | +2 | 0 | −1 | −2 |

**Acción → memoria social → efecto sobre la siguiente disponibilidad:**

- Aportar información **demostrablemente falsa** o explorar sin permiso: caída grave; solicitud futura puede necesitar acompañamiento, cita o documentación reforzada.
- Incumplir un compromiso previo: caída leve; menor prioridad de atención.
- Presentar una solicitud formal válida: neutro; cola normal.
- Colaborar de manera verificable: mejora leve; mayor predisposición a atender.
- Cumplir un trámite previo documentado: mejora alta; prioridad limitada en la siguiente interacción.

**Cortafuegos de autoridad:** confianza jamás otorga `ARCHIVE_CASE_0042`, ni divulga `HISTORY`, ni convierte un funcionario en competente, ni produce automáticamente una extensión de **12 horas**. Cualquier ampliación del plazo de otro expediente requerirá una norma explícita, un actor competente y una transición autorizada (M2); el slice EXP-0042 mantiene **30 minutos**. La memoria pertenece al observador, no a una reputación omnisciente compartida. Véanse [permiso negativo](../../tests/test_denied_permit_idempotence.py) y [alcance M1](M1_scope.md).
