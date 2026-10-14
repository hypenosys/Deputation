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

## EXP-0042 playable specification, separate from runtime

The [authored case](design/EXP-0042_case_arc.md) supplies motive, stakeholders and a 30-minute diegetic window. The [moment-to-moment loop](design/moment_to_moment.md) defines a 2–3 **real-minute** repeated player cycle. The [15-mechanic M1 selection](design/M1_scope.md) limits the production target. [Denial feedback](design/denial_feedback.md) is a pure view of rejection codes; [trust scheduling](design/social_dynamics.md) is an M2-only proposal and **cannot** grant legal authority. The [reference evaluator](../tools/authority_reference.py) and [negative tests](../tests/test_denied_permit_idempotence.py) make denied-permission idempotence executable in Python only. The full game remains unimplemented here.

## Ludological reference oracle and causal design

The player verb is **acreditar** (investigate and prove), the unit is a case, and [GAME LOOP](GAME_LOOP.md) is the canonical M1 gameplay grammar. [ACTION MATRIX](behavior/ACTION_MATRIX.md) maps player actions to guards, transition and readable feedback. [NARRATIVE ENGINE](NARRATIVE_ENGINE.md) specifies a hybrid: a deterministic kernel emits facts while an authored director selects permissible beats without inventing outcomes. The host-only [trace runner](../tools/simulate_trace.py) can replay six cycles to validation and an alternative expiry, applying the M1-relevant m10/m15/m27 milestones. It **does not** implement M2 trust/incident or C64 render. [C64 resource constraints](CONSTRAINTS.md) remain engineering targets pending linker and cycle evidence.
