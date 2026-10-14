# Roadmap — mechanics to executable game

## M0 — Research foundation (this PR)

- Preserve all 45 records and their actual source evidence; never renumber.
- Record an authored, non-verified contract subset.
- Validate unique IDs, provenance, links, scenario topology and the status ledger.
- Publish an initial CI gate and documentation.

## M1 — Canonical game runtime

Implement a deterministic institution kernel independent of renderer; port essential navigation/time/EXP-0042 logic from ABBI with tests rather than copying assumptions. Tests for a denied action changing no world state, monotonic time, permission checks and knowledge provenance.

## M2 — Causal institutional systems

Integrate queues, capacity, autonomous schedules, incidents, authorization scopes and social trust into *one* runtime. At least three outcomes must emerge from the rules, not from scripted camera triggers.

## M3 — Godot interactive vertical slice

Create Courtyard, Registry and Archive environments with navigation and interactions. Switch between first-person retro 3D, isometric and 2D views over the **same** game state. Godot headless integration tests and observable time/knowledge invariance.

## M4 — Native C64 adapter and hardware gates

Derive static tables and fixed-point representation. Compile for cc65, inspect linker map, measure cycle budgets and validate in VICE. Repeat the exact binary on C64 Ultimate. Keep performance, visual quality and evidence dimensions separate.

## Definition of done

Every completed mechanic must have provenance, a reproducible behavioral contract, source implementation, negative and positive tests, visible effects and explicit per-platform verification. A planning document or source import alone does not satisfy implementation.
