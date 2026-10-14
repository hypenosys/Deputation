# Architecture — institution before camera

**Status:** research/architecture foundation. The canonical runtime discussed below exists as implementations and experiments in ABBI; the new Deputation repository has imported descriptions and fixtures, **not those runtime binaries**.

## Separation of concerns

```text
external original source / game-design conversations
   -> immutable extraction records (DPT-M-001..045)
   -> curated behavior contracts (DPT-C-...)
   -> future authoritative institution state
      [time, rooms, actors, permissions, cases, knowledge, trust, incidents, queues]
   -> transitions / bounded event processing / reproducible evidence
   -> immutable frame-state projection
      -> 2D/PETSCII
      -> 2.5D isometric
      -> retro 3D first person
```

Do not use a rendered sprite or HUD state as the source of truth for gameplay decisions.

## Data model and evidence

The [extraction](../data/mechanics/extraction.v1.json) conserves names, evidence classifications, source paths and ABBI candidate cross-references. A `DPT-M` observation is **not** a new canonical `ABBI-M` identity. Proposed contracts are stored separately in [contracts](../data/mechanics/contracts.v1.json). IDs are stable and not recycled.

A contract describes inputs, outputs and invariants, but is not marked as implemented merely because it can be described. Validation source code is in [tools](../tools/validate_mechanics.py).

## Rule examples

- **Spatial:** a room exit must exist; movements have travel costs; interaction takes place in the actor's actual room.
- **Institutional:** EXP-0042 requires stage transitions and explicit validation; clock-based deadlines can generate review consequences.
- **Epistemic:** facts have observers and authorization. A global world fact is not magically known by every character.
- **Social:** trust is actor-scoped and affects disclosure; denied disclosure must not transfer the fact.
- **Operational:** a worker or terminal is capacity-constrained; events are causal and deterministic.
- **Presentation:** the camera must not advance a tick or mutate the authoritative case.

## World fixture

The canonical vertical slice is Courtyard (1) ↔ Registry (2) ↔ Archive (3), with integer room IDs, travel times, camera anchors and case EXP-0042. It is a fictional topology. The full game design remains broader than this baseline.

## Platform work

A future Godot front end may use GDScript nodes to display the world; a separate C99/cc65 module may implement a fixed memory layout for C64. Neither changes the contracts silently. Hardware validation needs exact binary SHA, memory-map evidence, VICE, then real C64 Ultimate observations.

## Acceptance before promoting implementation status

1. Data/contracts validate; duplicates and illegal cross-references are rejected.
2. Deterministic host-level transition tests cover real action choices.
3. Three camera modes do not modify authoritative simulation state.
4. Runtime platform claims are backed by the *exact artifact* and reproducible logs.
5. Only then may "implemented" or "validated" replace the research statuses.
