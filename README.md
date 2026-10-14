# THE DEPUTATION

**Empty Space Videogames · Hypenosys · ABBI research companion**

THE DEPUTATION is about **investigating and accrediting a contradiction** under institutional deadlines, knowledge and permission constraints. The proposed player verb is **acreditar**: locate → read → request → act → verify. The project's objective is not to reproduce an actual public institution or security layout.

> **Repository status (2026-10-14):** mechanic-inventory and research foundation. This repository does **not** yet contain a finished or hardware-certified game. Source execution originally researched in [hypenosys/abbi](https://github.com/hypenosys/abbi/tree/feature/retro3d-performance-v3).

## What's in the repository?

- [45 sourced mechanic observations](data/mechanics/extraction.v1.json), linked to an exact ABBI research commit.
- [Readable mechanics audit](docs/mechanics/INVENTORY.md) with cross-references and evidence boundaries.
- [11 draft behavior contracts](data/mechanics/contracts.v1.json) for the highest-value systems.
- [Canonical fictional three-room world](data/world/vertical_slice.v1.json).
- [Canonical GAME LOOP](docs/GAME_LOOP.md), [ACTION MATRIX](docs/behavior/ACTION_MATRIX.md), [player agency](docs/PLAYER_AGENCY.md), [hybrid narrative engine](docs/NARRATIVE_ENGINE.md).
- [Blind paper-playtest protocol](docs/PLAYTESTING_PROTOCOL.md), [C64 constraints](docs/CONSTRAINTS.md), [design baseline](docs/DESIGN_BASELINE.md) and [future state debugger](docs/STATE_DEBUGGER.md).
- [Six-cycle winning ghost](data/world/simulation_trace.json), [losing counterfactual](data/world/simulation_trace_failure.json), [CI-observed action-by-action walkthrough](docs/behavior/TRACE_WALKTHROUGH.md) and [pure trace runner](tools/simulate_trace.py).
- [Architecture](docs/architecture.md), [development roadmap](docs/roadmap.md) and [contribution requirements](CONTRIBUTING.md).
- [EXP-0042 case arc](docs/design/EXP-0042_case_arc.md), [2–3 minute loop](docs/design/moment_to_moment.md), [denial feedback](docs/design/denial_feedback.md), [trust dynamics](docs/design/social_dynamics.md), [pacing](docs/design/case_pacing.md), [M1 scope (15/45)](docs/design/M1_scope.md).
- Python standard-library checks and CI, **not** a claim of executable 45-mechanic integration.

## First verification

Requires Python 3.11+ (no external dependencies):

```bash
python tools/validate_mechanics.py
python tools/validate_design.py
python -m tools.simulate_trace --trace data/world/simulation_trace.json
python -m tools.simulate_trace --trace data/world/simulation_trace_failure.json
python -m unittest discover -s tests -v
```

Expected evidence totals: 19 C/C64 code-path observations, 2 C helpers not wired to gameplay, 18 isolated host prototypes/fixtures, 6 design goals. These are **source classification labels, not 19 runtime-certified mechanics**.

## Design boundary

One institution state; simulation transitions driven by actions/events, irrespective of PETSCII, isometric or Retro3D visualization. A camera switch is presentation only. The runtime, rendering, Godot implementation and native C64 port are future work in this repository. See [architecture](docs/architecture.md).

## Source, provenance and rights

Mechanics have *descriptions*, IDs, source paths and links; this repository does not import proprietary game assets, ROMs, or another project's binary artifacts. The research refers to ABBI source commit `e876cda71b21712860bf742d6de6689161940fdf` on `feature/retro3d-performance-v3`; inspect that source before promoting a record's implementation status. The repository's existing [CC0 license](LICENSE) has been preserved.

## Hypenosys standards

[Hypenosys development documentation](https://dev.hypenosys.com/documentacion) is the intended authority. It was unreachable during the initial import and **formal compliance remains pending**, documented in [standards adoption](docs/standards/HYPENOSYS_ADOPTION.md). This initial scaffold uses explicit evidence, tests, architectural boundaries and reviewable pull requests; it does not invent unpublished requirements.

## Narrative design and reference-contract boundary

EXP-0042 has a fictional narrative proposal plus **pure Python refusal/permission contract** (`tools/authority_reference.py`). `tests/test_denied_permit_idempotence.py` tests that refusal returns the same frozen authoritative state without charging time or revealing knowledge. The newer **ghost runner** implements a limited, deterministic *host-only* M1 action loop over the three-room JSON world, including movement, explicit waiting and source-matched m10/m15/m27 milestones. It is not a player-facing M1 game: no personnel scheduling, queues, social trust, graphics, Godot or C64 gameplay is integrated. Authoritative actions, including the scripted evidence timing from ABBI, must be ported and verified before claiming a playable slice. All 45 extraction records remain archival observations; only 15 are allocated to M1.

## Intended play experience versus reproducible host ghost

A **case**, not a working day, is the unit of play. The initial expected session is **12–20 real minutes** (unverified), while EXP-0042 spans **30 simulated minutes**. The six-cycle test trace and losing alternative provide **author-selected examples**, not evidence of human player experience. Run the deterministic traces with `python -m tools.simulate_trace`, then consult the blind [paper protocol](docs/PLAYTESTING_PROTOCOL.md) before porting to Godot/C64. A code-driven state debugger is specified for M3 but has not been built.
