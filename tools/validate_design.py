#!/usr/bin/env python3
"""Validate authored EXP-0042 narrative artifacts without promoting runtime claims."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_REFERENCE_CODES = {
    "MISSING_CASE_BASIS", "PERMISSION_ALREADY_GRANTED",
    "MISSING_CASE_PERMISSION", "INVALID_CASE_STAGE",
    "MISSING_HISTORY", "MISSING_READY", "WRONG_ROOM",
    "DEADLINE_EXPIRED", "ACTOR_NOT_AUTHORIZED", "ACTOR_UNAVAILABLE",
}
TRUST_STATES = ("severe_loss", "minor_loss", "unchanged", "minor_gain", "major_gain")


class DesignError(ValueError):
    """A design artifact contradicts the fixed case contract."""


def require(value: bool, reason: str) -> None:
    if not value:
        raise DesignError(reason)


def load(path: str, root: Path = ROOT) -> dict:
    return json.loads((root / path).read_text(encoding="utf-8"))


def validate_feedback(data: dict) -> int:
    require(data.get("schema") == "deputation.feedback_catalog.v1", "Feedback schema invalid")
    require(data.get("case_id") == "EXP-0042", "Feedback wrong case")
    policy = data.get("policy", {})
    for flag in ("denial_mutates_case", "denial_mutates_clock", "denial_mutates_trust",
                 "denial_mutates_knowledge"):
        require(policy.get(flag) is False, f"Denial may mutate {flag}")
    require(policy.get("feedback_is_a_presentation_projection") is True, "Feedback must be projection only")
    require(policy.get("hidden_fact_leakage") == "forbidden", "Knowledge disclosure policy missing")
    entries = data.get("denials")
    require(isinstance(entries, list) and len(entries) >= 10, "Insufficient denial catalog")
    seen, reference = set(), set()
    for entry in entries:
        key = (entry.get("action"), entry.get("code"))
        require(all(isinstance(x, str) and x.strip() for x in key), "Denial key empty")
        require(key not in seen, "Duplicate denial key")
        seen.add(key)
        require(entry.get("status") in {"reference", "planned_M1", "planned_M2"}, "Unknown denial status")
        for field in ("actor", "visible_reason", "next_action"):
            require(isinstance(entry.get(field), str) and len(entry[field].strip()) >= 4,
                    f"Denial {key} lacks {field}")
        if entry["status"] == "reference":
            reference.add(entry["code"])
    require(REQUIRED_REFERENCE_CODES <= reference,
            "Reference refusal codes missing feedback: " + repr(REQUIRED_REFERENCE_CODES - reference))
    return len(entries)


def validate_social(data: dict) -> int:
    require(data.get("schema") == "deputation.social_dynamics.v1", "Social schema invalid")
    require(data.get("status") == "M2_design_only", "Social matrix cannot claim runtime implementation")
    require(data.get("case_id") == "EXP-0042", "Social matrix wrong case")
    require(tuple(data.get("trust_change_states", [])) == TRUST_STATES, "Trust states changed")
    rows = data.get("matrix")
    require(isinstance(rows, list) and len(rows) == 5, "Need five actor types")
    seen = set()
    for row in rows:
        actor = row.get("actor_type")
        require(isinstance(actor, str) and actor not in seen and actor.strip(), "Actor type invalid/duplicate")
        seen.add(actor)
        cells = row.get("cells")
        require(isinstance(cells, list) and len(cells) == 5, "Each actor needs five effects")
        require([c.get("trust_state_change") for c in cells] == list(TRUST_STATES),
                "Trust effects must be in canonical order")
        values = [c.get("next_wait_delta_minutes") for c in cells]
        require(all(type(v) is int for v in values), "Wait effects must be integers")
        require(values == sorted(values, reverse=True), "More trust must not increase delays")
        require(values[2] == 0, "Unchanged trust must give no scheduling adjustment")
        require(all(isinstance(c.get("availability_rule"), str)
                    and c["availability_rule"] for c in cells), "Missing availability rule")
    events = data.get("events")
    require(isinstance(events, list) and len(events) >= 5, "No social causal events")
    require(len({e.get("event") for e in events}) == len(events), "Duplicate social events")
    require(all(e.get("change") in TRUST_STATES for e in events), "Unrecognized trust delta")
    require("never grants legal permission" in data.get("rule", "").lower(),
            "Trust cannot grant authorization")
    return sum(len(r["cells"]) for r in rows)


def validate_scope(data: dict, catalog: dict) -> int:
    require(data.get("schema") == "deputation.milestone_scope.v1", "Milestone schema invalid")
    require(data.get("status") == "design_not_runtime", "Milestones must not claim runtime")
    ids = {m["id"] for m in catalog["mechanics"]}
    all_ids = []
    for key, size in (("M1", 15), ("M2", 23), ("M3", 7)):
        entries = data.get(key)
        require(isinstance(entries, list) and len(entries) == size, f"{key} wrong scope")
        all_ids.extend(entries)
    require(len(all_ids) == len(set(all_ids)) and set(all_ids) == ids,
            "Milestones overlap or drop source observations")
    require({"DPT-M-022", "DPT-M-025", "DPT-M-026"} <= set(data["M1"]),
            "M1 must include scoped authority/disclosure")
    return len(data["M1"])


def validate_prose(root: Path = ROOT) -> tuple[int, int]:
    arc = (root / "docs/design/EXP-0042_case_arc.md").read_text(encoding="utf-8")
    moment = (root / "docs/design/moment_to_moment.md").read_text(encoding="utf-8")
    arc_words, moment_words = len(arc.split()), len(moment.split())
    require(300 <= arc_words <= 500, f"EXP-0042 case arc outside 300–500 words: {arc_words}")
    require(175 <= moment_words <= 225, f"Moment-to-moment loop not ~200 words: {moment_words}")
    pacing = (root / "docs/design/case_pacing.md").read_text(encoding="utf-8")
    require("xychart-beta" in pacing and pacing.count("  line [") == 2,
            "Winning and losing emotional curves required")
    return arc_words, moment_words


def main() -> int:
    feedback = validate_feedback(load("data/design/feedback_catalog.json"))
    social = validate_social(load("data/mechanics/social_dynamics.json"))
    scope = validate_scope(load("data/design/m1_scope.json"),
                           load("data/mechanics/extraction.v1.json"))
    arc_words, loop_words = validate_prose()
    world = load("data/world/vertical_slice.v1.json")
    require(world["case"]["symbol"] == "EXP0042" and
            world["case"]["deadline_minute"] == 30,
            "Narrative case deadline contradicts canonical world")
    print(f"DESIGN PASS: {feedback} feedback reasons, {social} trust cells, "
          f"{scope} M1 mechanics, arc {arc_words} words, loop {loop_words} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
