"""Deterministic, host-only paper-playtest trace runner for EXP-0042.

This is a design oracle, *not* the integrated M1 game, ABBI's native C
simulation, a Godot scene or a C64-certified executable. The state transition
that reaches a timestamp applies scripted ABI research milestones in order.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

from tools.authority_reference import CaseState, evaluate, DEADLINE_MINUTE

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "data/world/vertical_slice.v1.json"
FEEDBACK = ROOT / "data/design/feedback_catalog.json"
DEFAULT_TRACE = ROOT / "data/world/simulation_trace.json"
ROOM_SYMBOLS = {"COURTYARD", "REGISTRY", "ARCHIVE"}


class TraceError(ValueError):
    """A trace or canonical precondition was violated."""


def load(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def snapshot(state: CaseState) -> dict:
    """Canonical, renderer-independent state; no sets or wall-clock fields."""
    return {
        "case_id": state.case_id, "minute": state.minute,
        "room": state.room, "stage": state.stage,
        "permissions": sorted(state.permissions), "knowledge": sorted(state.knowledge),
        "available_actors": sorted(state.available_actors), "trust": list(state.trust),
    }


def state_sha(state: CaseState) -> str:
    canonical = json.dumps(snapshot(state), sort_keys=True,
                           ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def advance_to(state: CaseState, minute: int) -> CaseState:
    """Apply known historical M1-relevant ABBI milestones at each minute.

    m18 relation adjustment and m20–24 network incident are deliberately NOT
    ported into this M1 reference oracle. In native ABBI they are different
    mechanisms; claiming they run here would fabricate gameplay coverage.
    """
    if type(minute) is not int or minute < state.minute or minute > 65535:
        raise TraceError("minute must be monotonic and <= 65535")
    for t in range(state.minute + 1, minute + 1):
        state = replace(state, minute=t)
        if t == 10 and state.stage == "registered":
            state = replace(state, stage="archive_review")
        if t == 15:
            state = replace(state, knowledge=state.knowledge | {"REVIEW"})
        if t == 27:
            state = replace(state, knowledge=state.knowledge | {"READY"})
    return state


def denial(code: str, state: CaseState, before: CaseState) -> tuple[CaseState, str]:
    if state is not before:
        raise TraceError("refused action illegally mutated authoritative state")
    return state, code


def perform(state: CaseState, action: dict, world: dict) -> tuple[CaseState, str]:
    """Return (new immutable state, outcome code). No rendering/UI side effects."""
    kind = action.get("type")
    if kind == "move":
        target = action.get("target")
        rooms = {r["symbol"]: r for r in world["rooms"]}
        if target not in rooms:
            return denial("INVALID_EXIT", state, state)
        room = rooms[state.room]
        exits = [next(r for r in world["rooms"] if r["id"] == rid)["symbol"]
                 for rid in room["exits"]]
        if target not in exits:
            return denial("INVALID_EXIT", state, state)
        index = exits.index(target)
        cost = room["travel_minutes"][index]
        if cost <= 0:
            raise TraceError("nonpositive canonical movement cost")
        return replace(advance_to(state, state.minute + cost), room=target), "MOVED"

    if kind == "wait":
        minutes = action.get("minutes")
        if type(minutes) is not int or not 1 <= minutes <= 30:
            raise TraceError("explicit wait needs 1–30 simulated minutes")
        return advance_to(state, state.minute + minutes), "WAITED"

    if kind == "inspect_case_status":
        return state, "STATUS_VIEWED"

    if kind == "read_case_file":
        if state.minute >= DEADLINE_MINUTE:
            return denial("DEADLINE_EXPIRED", state, state)
        if state.room != "REGISTRY":
            return denial("WRONG_ROOM", state, state)
        gained = replace(state, knowledge=state.knowledge | {"CASE_BASIS"})
        return advance_to(gained, state.minute + 1), "CASE_FILE_READ"

    if kind in {"request_permit", "read_archive", "validate_case"}:
        decision = evaluate(state, kind, actor=action.get("actor"))
        if not decision.accepted:
            if decision.state is not state:
                raise TraceError("authority denial mutated state")
            return state, decision.code
        if decision.state.minute <= state.minute:
            raise TraceError("accepted authority event must consume time")
        # Advance through the exact same integer milestones as navigation/wait.
        events = advance_to(state, decision.state.minute)
        changed = replace(decision.state, knowledge=decision.state.knowledge | events.knowledge,
                          stage=("validated" if decision.state.stage == "validated"
                                 else events.stage))
        return changed, decision.code

    raise TraceError(f"unknown action: {kind!r}")


def feedback(code: str, action: str, minute: int, catalog: dict) -> dict:
    choices = [x for x in catalog["denials"]
               if x["code"] == code and x["action"] in (action, "*")]
    if not choices:
        return {"code": code, "message": "Acción aceptada / consulta de estado",
                "next_action": "", "actor": "SYSTEM", "remaining_minutes":
                max(0, DEADLINE_MINUTE - minute)}
    entry = next((x for x in choices if x["action"] == action), choices[0])
    return {"code": code, "message": entry["visible_reason"],
            "next_action": entry["next_action"], "actor": entry["actor"],
            "remaining_minutes": max(0, DEADLINE_MINUTE - minute)}


def outcome(state: CaseState) -> str:
    if state.stage == "validated":
        return "validated"
    if state.minute >= DEADLINE_MINUTE:
        return "expired"
    return "ongoing"


def replay(trace: dict, world: dict, catalog: dict) -> dict:
    if trace.get("schema") != "deputation.simulation_trace.v1":
        raise TraceError("unknown trace schema")
    if trace.get("case_id") != "EXP-0042" or world["case"]["deadline_minute"] != 30:
        raise TraceError("trace/canonical case mismatch")
    cycles = trace.get("cycles")
    if not isinstance(cycles, list) or not cycles:
        raise TraceError("missing cycles")
    state = CaseState(room="COURTYARD")
    seen = set()
    records = []
    for cycle in cycles:
        cid = cycle.get("id")
        if not isinstance(cid, str) or not cid or cid in seen:
            raise TraceError("cycle ID missing or duplicated")
        seen.add(cid)
        actions = cycle.get("actions")
        if not isinstance(actions, list) or not actions:
            raise TraceError(f"{cid}: empty interaction cycle")
        observations = []
        for i, action in enumerate(actions, 1):
            if not isinstance(action, dict):
                raise TraceError(f"{cid}: action {i} is not an object")
            pre = state_sha(state)
            previous = state
            state, code = perform(state, action, world)
            post = state_sha(state)
            if code != action.get("expect_code"):
                raise TraceError(f"{cid} step {i}: expected {action.get('expect_code')}, got {code}")
            if state.minute != action.get("expect_minute"):
                raise TraceError(f"{cid} step {i}: expected minute {action.get('expect_minute')}, got {state.minute}")
            if (code in {x["code"] for x in catalog["denials"]}
                    and pre != post and state is previous):
                raise TraceError(f"{cid} step {i}: denial hash mutated")
            observations.append({
                "step": i, "action": action["type"], "target": action.get("target"),
                "code": code, "minute": state.minute, "room": state.room,
                "stage": state.stage, "knowledge": sorted(state.knowledge),
                "permissions": sorted(state.permissions),
                "state_sha256": post, "unchanged": pre == post,
                "feedback": feedback(code, action["type"], state.minute, catalog),
            })
        expected = cycle.get("expect_end")
        current = {"minute": state.minute, "room": state.room,
                   "stage": state.stage, "outcome": outcome(state)}
        if current != expected:
            raise TraceError(f"{cid}: expected end {expected}, got {current}")
        records.append({"cycle": cid, "intent": cycle.get("intent", ""),
                        "actions": observations, "end": current})
    if outcome(state) != trace.get("expect_outcome"):
        raise TraceError("final outcome mismatch")
    return {"schema": "deputation.trace_report.v1", "trace": trace.get("name", ""),
            "cycles": records, "final_state": snapshot(state),
            "final_state_sha256": state_sha(state), "outcome": outcome(state)}


def run_file(path: Path) -> dict:
    return replay(load(path), load(WORLD), load(FEEDBACK))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace", type=Path, default=DEFAULT_TRACE)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    try:
        report = run_file(args.trace)
    except (TraceError, KeyError, TypeError, OSError, ValueError) as exc:
        parser.exit(1, f"TRACE FAIL: {exc}\n")
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for c in report["cycles"]:
            print(f'\n{c["cycle"]} — {c["intent"]}')
            for a in c["actions"]:
                f = a["feedback"]
                print(f'  {a["step"]}. {a["action"]:<20} m{a["minute"]:02} '
                      f'{a["room"]:<9} {a["code"]}'
                      + (f' — {f["message"]}; next={f["next_action"]}' if a["unchanged"]
                         and a["code"] != "STATUS_VIEWED" else ""))
            print(f'  => {c["end"]}')
        print(f'\nTRACE PASS: {len(report["cycles"])} cycles; '
              f'outcome={report["outcome"]}; hash={report["final_state_sha256"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
