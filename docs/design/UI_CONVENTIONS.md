# THE DEPUTATION — UI conventions / interaction contract

The interface **is** the institution: folders, numbered forms, stamps and explicit status. It must deliberately look rigid while remaining mechanically honest. [Visual identity](VISUAL_IDENTITY.md) · [voice](NARRATIVE_VOICE.md) · [action matrix](../behavior/ACTION_MATRIX.md).

## Persistent information (all three layouts)

**Always visible:** `EXP-0042`; active room; case stage; `CLOCK mm/30` and remaining minutes; known permission scope; last actionable response; current next step. Show the clock **before committing a costly move**. Keep a single persistent last-result panel rather than a temporary toast. Ending controls do not change world state after `validated` or `expired`.

**Layouts:** 
1. **Abierto** — case document, recorded facts, visible conflicting dates, actionable file review.
2. **Bandeja** — pending duties and derived blockers, sorted by viability, not arbitrary quest rarity.
3. **Ventanilla** — interlocutor, permitted action, rejection reason + authorized next step.

User navigates layouts for **zero** simulated time. The prototype must retain the same state across all screens. On screen `DENIED` is a **response**, not a penalty, and must not consume a minute.

## Administrative vocabulary

| Machine code | Visual label | Audio placeholder | Guidance |
| --- | --- | --- | --- |
| `MISSING_CASE_BASIS` | `DENEGADO — FALTA MOTIVO` | paper thud | Abrir carátula en Registro |
| `PERMIT_GRANTED` | `AUTORIZADO PARA EXP-0042` | single stamp | Ir a Archivo; no acceso general |
| `INVALID_CASE_STAGE` | `NO DISPONIBLE — FASE` | muted click | Esperar m10; consultar fase |
| `MISSING_CASE_PERMISSION` | `DENEGADO — FALTA PERMISO` | muted click | Solicitar en Registro |
| `MISSING_READY` | `NO LISTO PARA VALIDACIÓN` | paper rustle | Comprobar indicación de preparación |
| `CASE_VALIDATED` | `DISCREPANCIA ACREDITADA` | firm double stamp | Consultar consecuencias |
| `DEADLINE_EXPIRED` | `PLAZO VENCIDO` | dry final tick | Consultar resultado; no reinicia |
| `WRONG_ROOM` | `VENTANILLA INCORRECTA` | paper thud | Ir a sala adecuada |

Audio is **an event cue, not another authoritative state**; sound muted must not reduce knowledge.

## Input and readability

- Keyboard and mouse controls; focus ring visible; buttons use verbs rather than vague “Aceptar”.
- The feedback panel shows **responsible actor, stable code, explanation and next action**. Never clear it on layout change.
- Always label clock as **SIMULADO**. The 2–3 minutes of play are *real time*, not the m30 deadline.
- Separate paper color role from stamp ink; urgent/danger are words + icons, never hue alone.
- Host Godot baseline 1280×720; min body text size **16 px**, headlines 20–28; hardware 40×25 renders full 8×8 glyphs, no promise of WCAG pixel equivalence.
- Declared pairings must pass **WCAG AA 4.5:1** as a host-web accessibility target. Godot/C64 still need human/screenshot verification; raster ghost does not equal compliance.
- No `await Timer`, frame-counting or camera switch may advance simulated time. A typed rejection is immediate and idempotent.
- No inaccessible automatic pagination. Reading the second page of evidence is visual only, not a second mechanical cost.

## Prototype acceptance

Must display three layouts, work from the canonical three-room map, allow case reading, permission request, archive disclosure, explicit waiting and validation. It must show a **denied action** with a reason and next step, preserve state across tabs and freeze mutating actions after closing. It does **not** implement M2 social trust, capacity, real NPC walking, 3D or C64 native rendering; do not label it the complete game.

## Sound staging (original procedural placeholders)

Action `read_case_file`: short soft paper flutter (0.12 s); permission success: single stamp low knock (0.07 s); denial: muted double-key tick (0.1 s); `m27` readiness: one restrained chime (0.2 s); expiry: dry clock stop (0.3 s). **No continuously looping noise** that masks the feedback or becomes fatigue; ambient clock loops should be user-mutable and independent of authoritative simulation time. No third-party audio files or rights assumptions. The Godot prototype synthesizes brief original event cues and an optional ambient ticking clock via `godot/procedural_audio.gd`; its mute toggle is independent of the authoritative case. Auditory quality and loudness have not been user-tested.
