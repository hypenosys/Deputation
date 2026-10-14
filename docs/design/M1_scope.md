# M1 — Selección estricta de mecánicas (diseño, no implementación certificada)

**Fuente:** [inventario de 45 observaciones](../mechanics/INVENTORY.md). M1 no porta el archivo completo. Los códigos `DPT-M-XXX` conservan identidad y evidencia originales: `c64_source` es presencia en ruta fuente, **no** ejecución validada; `host_prototype` tampoco prueba integración en PRG.

## M1 — 15 de 45 (mínimo núcleo del EXP-0042)

| IDs | Por qué se incluyen | Aceptación exigida |
| --- | --- | --- |
| 001, 002, 004 | Movimiento, minutos y acciones condicionadas por sala | Salidas ilegales sin cambios; ruta 1→2→3 con costes 2 y 3 |
| 005, 013 | Reloj y deadline | Tiempo monótono; advertencia a 5 minutos; no validación después de m30 |
| 007, 009, 012 | Fase, conocimiento y validación | Transiciones solo por acción y precondiciones; no conocimiento omnisciente |
| 016, 017, 021 | Objetivo, conclusión y feedback visual | Objetivo legible, victoria condicionada, cuenta atrás visible |
| 018 | Separación de cámara y estado | Mismo hash autoritativo antes/después de cambiar la vista |
| 022, 025, 026 | Acceso, permiso específico y divulgación | `ARCHIVE_CASE_0042` no es un permiso general; negación sin pérdida de tiempo, divulgación sin fuga |

Estos **tres últimos** existen solo como prototipos host en el catálogo de referencia. Integrarlos en M1 requiere código y tests nuevos; sus contratos no se consideran ejecutados por este documento. La [prueba de denegación](../../tests/test_denied_permit_idempotence.py) cubre un **microcontrato Python puro**, no el juego completo ni C64.

## M2 — 23 observaciones, fuera de M1

`003, 006, 008, 010, 011, 014, 015, 023, 024, 027, 028, 029, 030, 031, 032, 033, 034, 035, 036, 037, 038, 039, 040`.

Automatismos, memoria social, agendas, colas, incidentes, tres rutas de resolución y direcciones narrativas emergentes. La [matriz social 5×5](../../data/mechanics/social_dynamics.json) es tuning propuesto **M2**; ningún bono cambia una competencia jurídica ni amplía automáticamente el deadline. La matriz de feedback separa las entradas ya cubiertas por la prueba de referencia de las previstas.

## M3 — 7 observaciones, fuera de M1

`019, 020, 041, 042, 043, 044, 045`.

Las cámaras y landmarks se activan sobre el mismo estado, con espacios reales, diálogos y replay. La base del director narrativo sigue siendo un selector de eventos verificables; las cinemáticas no escriben la simulación.

## C64 — presupuesto sujeto a evidencia

La máquina tiene un espacio de direcciones de **64 KiB**, no 64 KiB libres para tablas. **No afirmar** que navegación, permisos, hechos y confianza precisan ya 20–30 KiB: no existe medida reproducible para esa cifra en Deputation. Compilar las 15 reglas, generar mapa real de `cc65` (CODE/RODATA/DATA/BSS/ZP, pantalla, charset y runtime) y medir tamaño y ciclos antes de decidir bancos, compresión o eliminación. Datos de archivo y documentos de autoría **no** forman parte del ejecutable.

## Puertas de calidad

M1 solo se considerará jugable con un recorrido positivo, denegación idempotente (estado, reloj, conocimiento, confianza), razones visibles, deadline probado, cámara neutra y fixtures de derrota. M2 requiere causación social probada y salidas alternativas; M3 exige interacción real de las tres presentaciones. Ninguna fase se valida por cantidad de registros.
