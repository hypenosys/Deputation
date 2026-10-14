# Contributing to THE DEPUTATION

Review the intended [Hypenosys documentation](https://dev.hypenosys.com/documentacion); see the [adoption gap](docs/standards/HYPENOSYS_ADOPTION.md) until it can be verified. The source of truth for original ABBI mechanics remains the exact linked source commit.

## Workflow

1. Branch from master. Never rewrite the existing extraction IDs.
2. Add or update an observation with a source path, evidence level and a specific behavior.
3. Add a contract when invariants are defined; do not label it implemented until executable tests exist.
4. Run `python tools/validate_mechanics.py` and `python -m unittest discover -s tests -v`.
5. Propose a PR explaining source, behavioral changes, tests, platform evidence and known gaps.

## Review checks

- No confusion between conceptual ABBI IDs and game-specific DPT IDs.
- No attribution of prototypes to the C64 gameplay executable.
- No undocumented permission escalation or omniscient NPC knowledge.
- Never advance game time because a camera changes.
- No claim of measured FPS, emulation or physical hardware without artifacts.
- Preserve CC0 license; verify rights individually before adding new external assets.
