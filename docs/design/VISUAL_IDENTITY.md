# THE DEPUTATION — Visual Identity / Internal Style Bible v0.1

**Direction:** *institutional realism, fraudulent order*. Fictional anonymous civil service circa 1978–1985, not a facsimile of a particular public building. **Genre:** restrained administrative dread; a paper trail is both weapon and prison. The image should be deliberately unglamorous, **not** unreadable. A stamped document must feel like a state change.

## Material and spatial identity

The player sees a **desk**, not a floating quest HUD: folders, typed forms, registry cards, numbered shelves, rubber stamps, carbon copy paper, punched holes, aging terminal glass, counter windows and a clock. Repetition is visual bureaucracy; **interruptions in the grid** signal important exceptions. Never use unreadable text, intentional mouse failure, or compulsory fake delays to suggest institutional incompetence. Ordinary actions remain responsive.

Three visual layers: (1) paper: cream/ink/typewriter grid; (2) institution: charcoal/metal/blueprint panels; (3) administrative agency: green authorized, amber needs procedure, red rejected, each with **explicit words**. Camera views may show the rooms, but the same authoritative case state drives the desk and all reports.

## Palette: one authored 16-color host set

The machine-readable source is [visual_palette.v1.json](../../data/design/visual_palette.v1.json). The 16 named hexes are **design RGB values for the Godot host prototype**, not a calibrated VIC-II 16-color mapping. Real C64 implementation must remap to its actual palette and prove readable contrast on the target display. No extra colors for alarms, overlays or disabled states; opacity can change but text must retain contrast.

| Role | Foreground / background | Contrast ratio (computed target) |
| --- | --- | ---: |
| Legal text | `ink #172527` / `paper #EEE5CE` | 12.58:1 |
| Secondary annotation | `muted #55615A` / `paper #EEE5CE` | 5.16:1 |
| Granted stamp | `green #1D6C58` / `paper #EEE5CE` | 5.01:1 |
| Refused stamp | `red #8B2734` / `paper #EEE5CE` | 6.87:1 |
| Urgent stamp | `amber #775211` / `paper #EEE5CE` | 5.58:1 |
| Terminal text | `pearl #F8F2E2` / `carbon #151B1C` | 15.59:1 |
| Secondary dark text | `paper_aged #D8CAA9` / `coal #222C2C` | 8.84:1 |

Official WCAG 2.2 AA text baseline: **4.5:1** regular, **3:1** large text; ratios verified in CI for declared semantic pairings using the official luminance formula (not a substitute for human readability testing). [W3C source](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Iconography must never encode a decision by color alone.

## Typography and iconography

- **Host desktop:** built-in engine font (no bundled fonts), force **fixed-width layout cells**, uppercase machine headings, sentence-case readable descriptions. Do not claim font is monospace until a licensed open monospace is added and tested; explicit cell alignment in this prototype is visual only.
- **Target C64:** use 8×8 glyphs and the exact 40×25 text screen; 256 glyphs/2048-byte charset if custom. Minimum capital text should occupy one full 8×8 cell. Avoid 6px miniature labels.
- **Status:** `[X]` DENIED, `[+]` APPROVED, `[!]` URGENT, `[?]` EVIDENCE, `[i]` STATUS. ASCII-first icons preserve portability between fonts and PETSCII, with a mapping table for C64 later.
- **Form fields:** left aligned, indexed `A01/A02`, dates written absolutely. Case code in machine-readable form `EXP-0042`; colon separators, dotted leaders, dashed rules.
- **Stamps:** never simply draw a decorative stamp and pretend a permission changed; appear only when the authoritative action succeeds.

## Reference design vs copying

Use **generic** office technology, mimeograph copies, analogue index cards and archival file systems as mood references. No copyrighted textures or borrowed government seals; all in-repo SVG wireframes must be original. Distinguish procedural friction from malicious UX. The desk should tell the player what is missing while the institution still may refuse the request.

## Three compositions

- [**Expediente abierto**](wireframes/case_open.svg): paper dominates, evidence and permission labels, two-step action.
- [**Bandeja de trabajo**](wireframes/task_list.svg): deadlines and order of work; no arbitrary quest markers.
- [**Ventanilla administrativa**](wireframes/administrative_view.svg): person/competence, denial with reason and next action.

The original [office concept art](concepts/institutional_desk.svg) (editable SVG), [three host UI sketches](wireframes/case_open.svg) and [three constrained PETSCII screens](PETSCII_LAYOUT.md) form one set of art direction sources. The Godot [institutional desk](../../godot/README.md) reads the same authored palette and voice JSON, rather than shipping unrelated colors.

**Visual gate:** before claiming a usable C64 UI, photograph/record on target palette and check truncation of cause/remaining time/next action at 40 columns; no color-only semantic distinctions.
