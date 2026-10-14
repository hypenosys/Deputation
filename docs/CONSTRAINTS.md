# THE DEPUTATION — Restricciones de C64 y puertas de rendimiento

**Estado:** presupuesto preliminar, **NO** medida del binario de Deputation. Para hardware real, compilar el mismo artefacto, guardar el mapa de enlazado y medir en VICE y Commodore 64 Ultimate. **Ni este repo ni el runner Python contienen todavía un ejecutable del M1.**

## 1. Memoria y representación

El MOS 6510 dispone de espacio de direcciones de **64 KiB**, pero no son 64 KiB de heap utilizable: ROM, I/O, VIC-II, pila, zero-page, mapeo y programas ocupan o comparten distintas regiones según configuración. Una tabla «45 mecánicas × X» no permite deducir honestamente **20–30 KiB mínimos** sin esquema y linker map. Los **45 registros JSON** son un **archivo de investigación host**, no deben incluirse en el PRG.

**Estimación de trabajo, no dato medido** para M1 con *tres salas / un expediente / cinco relaciones potenciales*:

| Segmento de datos de juego | Diseño de codificación | Presupuesto provisional |
| --- | --- | ---: |
| Reloj, deadline, sala, fase | \`uint16_t\` + bytes | 6–10 B |
| Bits de conocimiento, autorización, objetivos | Máscaras de bits | 6–16 B |
| Actores/agenda mínima (si M1 lo requiere) | IDs compactos, sin strings | 8–32 B |
| Confianza (NO integrada en M1) | 5 bytes solo reserva futura | 0 B M1 |
| Cola de eventos, causas de rechazo | Tabla circular de códigos, sin frases | 32–64 B |
| Estado del expediente, flags y margen | IDs + buffers de guardas | 32–64 B |
| **Objetivo de simulación M1** | A confirmar por compilación | **≤256 B** |

Los valores superiores no son suma de bloques certificados; son límites orientativos y *headroom* para un **solo caso**. Nunca asignar RAM en el target según estimaciones de Python. Strings narrativos y secuencias escénicas tienen su propio coste y deben comprimirse en IDs/glyphs o usar contenido en disco según diseño posterior.

| Representación VIC-II | Tamaño nominal | Implicación |
| --- | ---: | --- |
| Pantalla de caracteres estándar | 40 × 25 = 1000 celdas | HUD + mundo compiten por ancho y altura |
| Caracteres normales | 8 × 8 píxeles por celda | 320 × 200 de cuadrícula visual teórica |
| Screen RAM | 1000 B | Página/alineación de VIC-II; base según modo |
| Color RAM | 1000 posiciones × nibble efectivo | Una elección de color por celda en modo texto estándar |
| Charset personalizado | 256 glifos × 8 B = 2048 B | Glyphs de interfaz y escenografía deben compartir presupuesto |
| Paleta del C64 | 16 colores | Contraste antes que gradientes; revisar legibilidad real |

**Cuidado:** pantalla, color y charset son **requisitos de visualización**, no una estimación de «estado social». El color RAM reside en la región I/O \`$D800–$DBE7\`; no contarlo simplemente como un segundo buffer de CPU RAM sin justificar copias. Si se mantiene framebuffer oculto o doble buffer, medir y sumar por separado. Cambios entre raycast/wireframe/isométrico no deben tocar bits de conocimiento.

## 2. Presupuesto de ciclos por cuadro

El vídeo PAL suele refrescar aproximadamente a **50 Hz** (aprox. **19.656 ciclos de CPU por frame** nominal), NTSC a **60 Hz** (aprox. **17.095 ciclos/frame**). Son **cifras de planificación**, no presupuesto libre garantizado: accesos VIC-II, badlines, interrupciones, SID, copia a pantalla y raster pueden consumir tiempo. La cadencia de vídeo **NO** prueba 25/50/60 FPS de juego.

Objetivo propuesto: el control de una opción/denegación debe obtener respuesta lógica en **≤1 tick de simulación** y mostrar feedback **antes de 2 refrescos de vídeo** cuando el render lo permita. No se afirma que pueda cumplirse todavía: la lógica temporal del expediente usa minutos ficticios, no un minuto por frame.

La lógica del M1 debe ser enteros/bits, tiempo monotónico, grafos estáticos; ningún parseo JSON, LLM, allocations sin control o strings largos en el bucle principal C64. Precalcular tablas legibles y documentar su ABI C. Investigar scrolling y paginación de texto: un mensaje de denegación puede necesitar **varias pantallas** o un cuadro de diálogo sin perder los campos esenciales.

## 3. Gate obligatorio de certificación

1. Compilar C99 de la lógica y correr tests host con warnings estrictos.
2. Compilar cc65 PRG con **mapa de memoria exacto**, tamaños CODE/RODATA/DATA/BSS/ZP; comprobar solapes con pantalla, charset y memoria del programa, y la configuración de VIC bank.
3. Registrar SHA del PRG, versiones de toolchain, PAL/NTSC, linker map y evidencia RAM.
4. En VICE, registrar tiempo de cada acción (incluyendo DENY) con medición de ciclos, comprobar primer frame, retroalimentación en pantalla y estabilidad de estado por dump.
5. Capturar vídeo/pantalla y comparar contra referencia solo con crop, paleta y modo declarados.
6. Ejecutar **el mismo hash** en C64 Ultimate, recopilar evidencia y separar aprobación de lógica, presentación y rendimiento.

**Bloqueo actual:** no hay mapa ni ciclos del M1 compilado; los **≤256 B** y **2 frames** son **objetivos de ingeniería**, no resultados. [Diseño 15/45](design/M1_scope.md) · [trazas](../data/world/simulation_trace.json) · [gate anterior](../docs/roadmap.md).
