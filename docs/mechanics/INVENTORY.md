# THE DEPUTATION — Inventario de mecánicas y capacidades

Repositorio de procedencia: `https://github.com/hypenosys/abbi`
Rama: `feature/retro3d-performance-v3`
Commit observado: `e876cda71b21712860bf742d6de6689161940fdf`

Método: lectura estática de código GitHub y recuperación de decisiones en conversaciones del proyecto. No se han ejecutado pruebas de VICE, C64 Ultimate ni la aplicación durante esta extracción. Importado en Deputation sin cambiar ese estado de evidencia.

**45 entradas de extracción**. Algunas son capacidades de motor y contratos técnicos, no mecánicas jugables autónomas. Ninguna recibe un ID definitivo ABBI-M al extraerse.

## Presente en ruta C/C64 (código, sin certificación de hardware en esta revisión) — 19

| ID | Dominio | Mecánica / capacidad | Estado observable y fuente | Posible relación ABBI |
|---|---|---|---|---|
| DPT-M-001 | Espacio | Navegación por grafo de dependencias espaciales | El jugador cambia de estancia solo si existe un arco en la topología compilada. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/navigation.h) | ABBI-M-000111 |
| DPT-M-002 | Tiempo | Coste temporal del desplazamiento | Cada salida válida tiene un coste en minutos; el reloj avanza atravesando los minutos intermedios. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/navigation.h) | ABBI-M-000005 |
| DPT-M-003 | Espacio | Desvíos y retorno sin bloquear progresión | El jugador puede recorrer salidas A/B, regresar y retomar la secuencia si vuelve al lugar adecuado. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/slice.c) | ABBI-M-000111 |
| DPT-M-004 | Interacción | Interacciones dependientes de estancia | Las acciones de registro y archivo se rechazan si el jugador no está en la estancia requerida. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/slice.c) | ABBI-M-000025 |
| DPT-M-005 | Tiempo | Reloj institucional irreversible | Los avances temporales no pueden retroceder y deben atravesar cada minuto. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/time.h) | ABBI-M-000005 |
| DPT-M-006 | IA | Rutina autónoma del archivero | La posición del archivista cambia al llegar el minuto 5, independientemente de la cámara. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/sim.c) | ABBI-M-000024 |
| DPT-M-007 | Expedientes | Máquina de estados del expediente EXP-0042 | Un caso pasa por registered, archive_review y validated de manera reglada. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/sim.c) | ABBI-M-000032 |
| DPT-M-008 | Expedientes | Traslado institucional del expediente | La estancia del expediente cambia automáticamente durante el flujo de revisión y validación. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/sim.c) | Por normalizar |
| DPT-M-009 | Conocimiento | Conocimiento del jugador en bits | Los hitos temporales 15 y 27 incorporan hechos al bitset de conocimiento del jugador. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/sim.c) | ABBI-M-000080 |
| DPT-M-010 | Social | Valor de relación institucional | La simulación modifica un valor firmado de relación en el minuto 18. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/sim.c) | ABBI-M-000034 |
| DPT-M-011 | Incidentes | Incidente de conexión con apertura y cierre | Una bandera de incidente de Registry se activa en minuto 20 y se desactiva en 24. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/sim.c) | ABBI-M-000031 |
| DPT-M-012 | Expedientes | Validación del caso por conocimiento y fase | La validación exige el hecho READY y la fase ARCHIVE_REVIEW y ocurre por acción explícita. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/sim.c) | ABBI-M-000032 |
| DPT-M-013 | Tiempo | Plazo seguro, urgente y vencido | El estado del plazo se deriva del minuto y de su deadline; urgente si quedan 5 minutos o menos. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/deadline.h) | ABBI-M-000004 |
| DPT-M-016 | Objetivos | Objetivos dinámicos por fase y posición | El objetivo y el indicador de estar en su estancia se derivan del estado del slice. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/objective.h) | ABBI-M-000032 |
| DPT-M-017 | Objetivos | Condición de cierre y victoria del slice | La última validación fija fase DONE y complete y bloquea pasos posteriores. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/slice.c) | ABBI-M-000032 |
| DPT-M-018 | Representación | Cámara independiente del estado institucional | La vista transforma estado sin avanzar minuto, mutar expediente ni mover NPC. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/render.h) | ABBI-M-000001 |
| DPT-M-019 | Representación | Triple vista PETSCII, isométrica y Retro3D | Adaptadores seleccionan raycasting, isométrico y wireframe del motor; no hay una vista cenital 2D general aquí. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/retro3d_adapter.h) | ABBI-M-000001 |
| DPT-M-020 | Representación | Reconocimiento de salas por señales y siluetas | Courtyard, Registry y Archive estampan motivos visuales distintos; son overlays, no geometría interactiva. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/room_landmarks.h) | ABBI-M-000113 |
| DPT-M-021 | Interfaz | HUD de plazo, objetivo, urgencia y localización | La primera fila del VIC-II muestra expediente, cuenta atrás, objetivo y estado seguro/urgente/tarde. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/hud.h) | ABBI-M-000115 |

## Helper C implementado, sin integración con bucle principal — 2

| ID | Dominio | Mecánica / capacidad | Estado observable y fuente | Posible relación ABBI |
|---|---|---|---|---|
| DPT-M-014 | Consecuencias | Generación de consecuencia por vencimiento | Se deriva una late review y una penalización potencial; falta integración en el bucle jugable principal. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/consequence.h) | ABBI-M-000079 |
| DPT-M-015 | Consecuencias | Revisión manual tras retraso | La revisión obligatoria se puede resolver y reduce relación una sola vez según el estado local de review. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/src/c/deputation/review.h) | ABBI-M-000079 |

## Prototipo o fixture host Python, no integrado en PRG — 18

| ID | Dominio | Mecánica / capacidad | Estado observable y fuente | Posible relación ABBI |
|---|---|---|---|---|
| DPT-M-022 | Acceso | Control de acceso por rol y zona | Un visitante sin permiso ARCHIVE recibe DENY en la demostración host. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day2.py) | ABBI-M-000073 |
| DPT-M-023 | Acceso | Competencias para transiciones de expediente | Una fase requiere rol de archivero; es un contrato de fixture y no está aplicado por el slice nativo. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/data/deputation/day2.json) | Por normalizar |
| DPT-M-024 | Percepción | Conocimiento local de acontecimientos | Solo los testigos definidos reciben noticias de eventos; no hay conocimiento omnisciente. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day2.py) | ABBI-M-000080 |
| DPT-M-025 | Acceso | Solicitud y autorización de acceso específico | El secretario puede conceder ARCHIVE_CASE_0042 sin conceder acceso general al Archivo. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day4.py) | Por normalizar |
| DPT-M-026 | Conocimiento | Divulgación autorizada de información | El jugador aprende HISTORIA únicamente tras autorización y acceso al archivero. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day4.py) | ABBI-M-000080 |
| DPT-M-027 | Tiempo | Agendas, reuniones y ventanas de atención | El secretario no está disponible durante una reunión; la solicitud debe esperar y puede llegar tarde. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day5.py) | ABBI-M-000024 |
| DPT-M-028 | Incidentes | Dependencia funcional entre servicios y trámites | Un terminal fuera de servicio bloquea el avance administrativo hasta su restauración. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day3.py) | ABBI-M-000031 |
| DPT-M-029 | IA | Respuesta de técnico ante incidencias | El técnico se desplaza para reparar el servicio sin intervención del jugador. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day3.py) | ABBI-M-000024 |
| DPT-M-030 | Tiempo | Duración del procesamiento de solicitudes | Aceptar una solicitud no implica completarla al instante; se consumen minutos y se evalúa el plazo. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day5.py) | ABBI-M-000005 |
| DPT-M-031 | Incidentes | Presión institucional acumulativa | Varias señales independientes suman severidad y superan umbrales de coordinación. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day9.py) | ABBI-M-000004 |
| DPT-M-032 | Incidentes | Coordinación interdepartamental reactiva | El umbral de presión activa una respuesta compartida que reduce presión sin borrar los hechos. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day9.py) | ABBI-M-000031 |
| DPT-M-033 | Recursos | Capacidad limitada de departamentos y colas | Cada recurso humano procesa una única tarea a la vez, generando tiempos de espera. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day10.py) | Por normalizar |
| DPT-M-034 | Recursos | Despacho con prioridades y desempate estable | Entre tareas disponibles gana mayor prioridad; empate por llegada y luego ID. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day10.py) | Por normalizar |
| DPT-M-035 | Social | Memoria social de ayuda y conducta intrusiva | Help incrementa confianza, unauthorized_probe la reduce y ambos dejan memoria social. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day11.py) | ABBI-M-000034 |
| DPT-M-036 | Social | Revelación de hechos condicionada por confianza | El funcionario concede o niega información según un umbral de confianza. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_day11.py) | ABBI-M-000077 |
| DPT-M-037 | Eventos | Cola de eventos por tiempo, prioridad e identidad | Se ordenan eventos por minuto, prioridad, tipo y sujeto para reproducibilidad. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/day6_events.py) | ABBI-M-000031 |
| DPT-M-038 | Narrativa | Director que selecciona hechos sin fabricarlos | El selector narrativo filtra eventos relevantes; no inventa cambios en el mundo. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/day6_director.py) | ABBI-M-000078 |
| DPT-M-039 | Verificación | Hash y reproducibilidad de simulación | Serialización canónica y SHA256 detectan divergencias entre ejecuciones host. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/tools/deputation/sim_core.py) | ABBI-M-000106 |

## Diseño objetivo, sin implementación demostrada — 6

| ID | Dominio | Mecánica / capacidad | Estado observable y fuente | Posible relación ABBI |
|---|---|---|---|---|
| DPT-M-040 | Diseño | Tres soluciones sistémicas al mismo problema | Meta de diseño M2: tres rutas de resolución demostradas; no hay soporte probado en el slice nativo. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/docs/production/THE_DEPUTATION_PRODUCTION_PIPELINE.md) | ABBI-M-000083 |
| DPT-M-041 | Diseño | Mundo espacial navegable con geometría por estancia | Definir colisiones, muebles, puertas, portales y oclusiones propios de cada sala, no solo overlays. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/docs/production/DEPUTATION_VISUAL_ARCHITECTURE_V1.md) | ABBI-M-000113 |
| DPT-M-042 | Diseño | Población institucional general y simulación fuera de cámara | Ampliación de NPC con comportamientos y horarios más allá de eventos de reloj fijos. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/docs/production/THE_DEPUTATION_PRODUCTION_PIPELINE.md) | ABBI-M-000024 |
| DPT-M-043 | Diseño | Rutas secretas e investigación opcional | Añadir secretos y trayectos alternativos con efectos verificables sobre el trámite. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/docs/production/THE_DEPUTATION_PRODUCTION_PIPELINE.md) | ABBI-M-000080 |
| DPT-M-044 | Diseño | Guardar partida y replay reproducible de entradas | Persistencia y replays reales del juego integrado, diferenciados de hashes de fixtures. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/docs/production/THE_DEPUTATION_PRODUCTION_PIPELINE.md) | ABBI-M-000044 |
| DPT-M-045 | Diseño | Diálogo y decisiones sociales libres | Contenido conversacional interactivo para consultar, convencer o intercambiar información con funcionarios. [Código](https://github.com/hypenosys/abbi/blob/feature/retro3d-performance-v3/docs/production/THE_DEPUTATION_PRODUCTION_PIPELINE.md) | ABBI-M-000033 |

## Límites comprobados

- El ejecutable C64 implementa una progresión principalmente guionizada por fases y minutos mínimos; no hay una simulación autónoma de tiempo real mientras espera entrada.
- Los fixtures `day1`–`day11` son experimentos separados. Sus subsistemas no constituyen automáticamente una única experiencia jugable integrada.
- El acceso por permisos, competencia administrativa, colas, confianza y divulgación social están en prototipos Python, no en la ruta jugable C actual.
- Los tres modos nativos son variantes de raycasting/retro3d/isométrico; no equivalen a una cámara 2D cenital completamente implementada.
- Los indicadores de sala se añaden como siluetas y overlays de render, sin topologías de colisión específicas y plenamente interactivas.
- Las mecánicas de un prototipo solo deben promoverse a validadas con pruebas de comportamiento y evidencia ligada al artefacto.