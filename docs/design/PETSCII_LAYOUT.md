# PETSCII 40 × 25 — three-screen interaction grammar

**Draft only:** three text fixtures sized exactly **40 columns × 25 rows**. These are **ASCII source mockups**, not a C64-encoded PRG, not Commodore ROM character art and not a VIC-II screenshot. They show how the same case might be paginated instead of cramming the 1280×720 Godot desk into the hardware screen.

- [Case document](petscii/case.txt) — evidence, scope, visible state.
- [Task inbox](petscii/tasks.txt) — progress and time costs.
- [Administrative counter](petscii/counter.txt) — competent actor, refused application, repairable next action.

Every layout explicitly contains **case, simulated clock, room and phase, responsible authority, reason/result and next step**. Denial context lives in the final rows: it must remain accessible without switching to another page. Words `DENIED`, `BY`, `WHY`, `NEXT` make the error causal rather than merely red. ASCII labels are a neutral intermediate representation; a future charset map converts into real PETSCII screen codes. No required gameplay meaning is stored solely in a color value.

## Proposed paging hierarchy

- Rows 00–03: institutional masthead + simulated time + room/phase.
- Rows 04–19: case-specific content or actions; 16 row working viewport.
- Rows 20–23: persistent rejection/confirmation actor, reason and alternative.
- Row 24: screen boundary.

These fixtures deliberately sacrifice illustration to keep the command grammar legible. A stamp can occupy cells only if it **does not obscure the deadline, cause or proposed action**. For a 16-color host preview choose an ink/background pairing from `visual_palette.v1.json`; on C64 verify the native VIC-II palette separately.

## UX conversion gate

1. Assert byte-perfect 40-char lines, 25 lines, ASCII source and permanent feedback fields in CI.
2. Replace placeholder labels with localized strings respecting the 38-column inner width. Do **not** silently truncate critical reasons.
3. Implement PETSCII screen/color cell placement over the C64 engine memory map; keep the state transition contract independent of the view.
4. Verify in VICE and the actual C64 Ultimate: capture readable screenshots and confirm that switching between these three layouts advances **zero** game minutes.
5. If legibility conflicts with fake period typography, **legibility wins**.

The current Godot demo shows a separate high-resolution UI. The mockups are the constraint bridge, **not proof** of a C64 rendering implementation.
