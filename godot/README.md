# THE DEPUTATION · Escritorio institucional (Godot 4.x)

**Runnable source prototype, not a certified build or integrated C64 game.** It reads the exact repository `data/world/vertical_slice.v1.json`, `data/design/visual_palette.v1.json`, `data/design/narrative_content.v1.json` and feedback catalog; it does not duplicate room topology. Native Godot Control hierarchy; no imported artwork, external fonts or audio assets.

From the **repository root**, where `project.godot` resides:

```bash
godot --path . --editor
# Open godot/Desk.tscn and press F6 (or F5 for the configured main scene)
# Optionally after installing a compatible Godot 4.x:
godot --headless --path . --quit-after 3
```

The desk shows three **zero-cost** layouts: expediente abierto, bandeja de tareas, ventanilla. State and last feedback persist while switching. To reproduce a quick win: REGISTRO → LEER CARÁTULA → PEDIR PERMISO → ARCHIVO → ESPERAR AL SIGUIENTE HITO (m10) → LEER ARCHIVO → ESPERAR AL SIGUIENTE HITO (m15) → ESPERAR AL SIGUIENTE HITO (m27) → VALIDAR CASO (m28). To see rejection before solving: press PEDIR PERMISO without a carátula or try LEER ARCHIVO from Registry. No simulation minute is charged for a refusal.

**Source QA vs runtime QA:** Python CI validates palette, story content and reference model fixtures. Godot 4 binary is **not currently provisioned in the existing CI**; therefore we do not claim the scene was launched, that glyphs fit every device or that Godot and Python are bit-identical. Confirm `--headless` syntax and inspect the scene manually before merging for production. A separate port/equivalence project should compare step-by-step state hashes and transitions with the Python oracle before promotion.

**Audio:** `godot/procedural_audio.gd` now synthesizes original low-volume stamp, paper, denial and ticking cues in memory; no sound file or license is imported. The ambient tick is based only on presentation-time and has an independent **SONIDO** toggle. See [audio cues](../docs/design/UI_CONVENTIONS.md). The acoustic result needs listening QA on a real device; headless verifies safe execution, not perceptual quality.

**Target C64:** the 1280×720 Godot layout is not a 40×25 PETSCII screen. Refer to the original [SVG wireframes](../docs/design/wireframes/), [40×25 layout fixtures](../docs/design/PETSCII_LAYOUT.md) and [C64 constraints](../docs/CONSTRAINTS.md); implement and test a dedicated bank/glyph-aware renderer before claiming native portability.
