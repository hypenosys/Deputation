# Roadmap — mechanics to executable game

## M0 — Research foundation (this PR)

- Preserve all 45 records and their actual source evidence; never renumber.
- Record an authored, non-verified contract subset.
- Validate unique IDs, provenance, links, scenario topology and the status ledger.
- Publish an initial CI gate and documentation.

## M0.5 — EXP-0042 narrative and negative-action specification (design stage)

- Author [case arc](design/EXP-0042_case_arc.md), [moment-to-moment loop](design/moment_to_moment.md), [denial feedback matrix](design/denial_feedback.md), [social dynamics matrix](design/social_dynamics.md), and [winning/losing pacing curves](design/case_pacing.md).
- Require `python tools/validate_design.py` and negative tests against a [pure reference evaluator](../tools/authority_reference.py); these checks do **not** certify a playable M1 or a native port.
- Partition **45 research records** as [M1=15, M2=23, M3=7](../data/design/m1_scope.json), preserving IDs and existing source-evidence labels.

## M0.6 — Ludological grammar and executable paper ghost

- Canonical [GAME LOOP](GAME_LOOP.md), [ACTION MATRIX](behavior/ACTION_MATRIX.md), [PLAYER AGENCY](PLAYER_AGENCY.md), [NARRATIVE ENGINE](NARRATIVE_ENGINE.md), [DESIGN BASELINE](DESIGN_BASELINE.md).
- Run six-cycle [winning](../data/world/simulation_trace.json) and [losing](../data/world/simulation_trace_failure.json) ghost traces through [Python reference simulation](../tools/simulate_trace.py) and negative replay tests in CI.
- Apply [blind playtest protocol](PLAYTESTING_PROTOCOL.md) with actual participants separately; automated traces **do not** demonstrate a fun or usable UI.
- Document [target C64 limits](CONSTRAINTS.md) as provisional budgets requiring cc65 map and cycle evidence.

## M1 — Canonical game runtime (15 essential mechanics)

Implement [the exact 15-mechanic subset](design/M1_scope.md): navigation, action/travel time, EXP-0042 phase/knowledge/deadline/validation, objectives, HUD, view invariance, case-scoped permissions, and authorized disclosures. The last three have only host-prototype evidence in the archive; integration is new work. Port deterministic institution transitions independently of the renderer. Test **rejected action leaves identical authoritative state** (including minute, trust, and knowledge), monotonic time on accepted moves, permission scopes, deadline behavior, visible denial reasons and positive/negative playthroughs. Do not conflate game minutes with the player's 2–3 minute real-time interaction cycle.

## M2 — Causal institutional systems (23 deferred observations)

Integrate queues, capacity, autonomous schedules, incidents, authorization scopes and social trust into *one* runtime. At least three outcomes must emerge from the rules, not from scripted camera triggers.

## M3 — Godot interactive vertical slice (7 deferred observations)

Create Courtyard, Registry and Archive environments with navigation and interactions. Build a [state debugger](STATE_DEBUGGER.md) that shows the canonical state, denial reasons and step hashes during development. Switch between first-person retro 3D, isometric and 2D views over the **same** game state. Godot headless integration tests and observable time/knowledge invariance.

## M4 — Native C64 adapter and hardware gates

Derive static tables and fixed-point representation. Compile for cc65, inspect linker map, measure cycle budgets and validate in VICE. Repeat the exact binary on C64 Ultimate. Keep performance, visual quality and evidence dimensions separate.

## Definition of done

Every completed mechanic must have provenance, a reproducible behavioral contract, source implementation, negative and positive tests, visible effects and explicit per-platform verification. A planning document or source import alone does not satisfy implementation.
