# THE DEPUTATION

**Empty Space Videogames · Hypenosys · ABBI research companion**

THE DEPUTATION explores a fictional institution as a systemic game: deadlines, knowledge, permissions, civil servants, case files, incidents and social consequences interact under one authoritative simulation. The project's objective is not to reproduce an actual public institution or security layout.

> **Repository status (2026-10-14):** mechanic-inventory and research foundation. This repository does **not** yet contain a finished or hardware-certified game. Source execution originally researched in [hypenosys/abbi](https://github.com/hypenosys/abbi/tree/feature/retro3d-performance-v3).

## What's in the repository?

- [45 sourced mechanic observations](data/mechanics/extraction.v1.json), linked to an exact ABBI research commit.
- [Readable mechanics audit](docs/mechanics/INVENTORY.md) with cross-references and evidence boundaries.
- [11 draft behavior contracts](data/mechanics/contracts.v1.json) for the highest-value systems.
- [Canonical fictional three-room world](data/world/vertical_slice.v1.json).
- [Architecture](docs/architecture.md), [development roadmap](docs/roadmap.md) and [contribution requirements](CONTRIBUTING.md).
- Python standard-library checks and CI, **not** a claim of executable 45-mechanic integration.

## First verification

Requires Python 3.11+ (no external dependencies):

```bash
python tools/validate_mechanics.py
python -m unittest discover -s tests -v
```

Expected evidence totals: 19 C/C64 code-path observations, 2 C helpers not wired to gameplay, 18 isolated host prototypes/fixtures, 6 design goals. These are **source classification labels, not 19 runtime-certified mechanics**.

## Design boundary

One institution state; simulation transitions driven by actions/events, irrespective of PETSCII, isometric or Retro3D visualization. A camera switch is presentation only. The runtime, rendering, Godot implementation and native C64 port are future work in this repository. See [architecture](docs/architecture.md).

## Source, provenance and rights

Mechanics have *descriptions*, IDs, source paths and links; this repository does not import proprietary game assets, ROMs, or another project's binary artifacts. The research refers to ABBI source commit `e876cda71b21712860bf742d6de6689161940fdf` on `feature/retro3d-performance-v3`; inspect that source before promoting a record's implementation status. The repository's existing [CC0 license](LICENSE) has been preserved.

## Hypenosys standards

[Hypenosys development documentation](https://dev.hypenosys.com/documentacion) is the intended authority. It was unreachable during the initial import and **formal compliance remains pending**, documented in [standards adoption](docs/standards/HYPENOSYS_ADOPTION.md). This initial scaffold uses explicit evidence, tests, architectural boundaries and reviewable pull requests; it does not invent unpublished requirements.
