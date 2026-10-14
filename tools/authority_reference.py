"""EXP-0042 authorization *reference contract*, not the playable M1 runtime.

Frozen state, no side effects for denials. Feedback is a separate projection.
This intentionally does not simulate navigation, queues, trust or C64 memory.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import FrozenSet

CASE_ID = "EXP-0042"
DEADLINE_MINUTE = 30
CASE_PERMISSION = "ARCHIVE_CASE_0042"


@dataclass(frozen=True)
class CaseState:
    case_id: str = CASE_ID
    minute: int = 0
    room: str = "REGISTRY"
    stage: str = "registered"
    permissions: FrozenSet[str] = field(default_factory=frozenset)
    knowledge: FrozenSet[str] = field(default_factory=frozenset)
    available_actors: FrozenSet[str] = field(
        default_factory=lambda: frozenset({"SECRETARY", "ARCHIVIST"})
    )
    trust: tuple[int, ...] = (0, 0, 0, 0, 0)


@dataclass(frozen=True)
class Decision:
    accepted: bool
    code: str
    actor: str
    next_action: str
    state: CaseState
    remaining_minutes: int


def _decision(state: CaseState, code: str, actor: str, next_action: str,
              new_state: CaseState | None = None) -> Decision:
    return Decision(
        accepted=new_state is not None,
        code=code,
        actor=actor,
        next_action=next_action,
        state=state if new_state is None else new_state,
        remaining_minutes=max(0, DEADLINE_MINUTE - state.minute),
    )


def evaluate(state: CaseState, action: str, *, actor: str | None = None) -> Decision:
    """Pure, deterministic transition; rejected action returns same state object.

    Accepted actions advance one *simulated* minute in this contract fixture;
    production durations belong to the future institution kernel.
    """
    if not isinstance(state, CaseState):
        raise TypeError("state must be CaseState")
    if state.case_id != CASE_ID or not 0 <= state.minute:
        raise ValueError("invalid EXP-0042 state")
    if action not in {"request_permit", "read_archive", "validate_case"}:
        raise ValueError("unknown action")

    expected_room, responsible = {
        "request_permit": ("REGISTRY", "SECRETARY"),
        "read_archive": ("ARCHIVE", "ARCHIVIST"),
        "validate_case": ("REGISTRY", "CASE_OFFICE"),
    }[action]
    operator = actor or responsible
    if state.minute >= DEADLINE_MINUTE:
        return _decision(state, "DEADLINE_EXPIRED", operator, "review_outcome")
    if state.room != expected_room:
        return _decision(state, "WRONG_ROOM", operator, f"travel_to_{expected_room.lower()}")
    if operator != responsible:
        return _decision(state, "ACTOR_NOT_AUTHORIZED", operator, f"find_{responsible.lower()}")
    if action != "validate_case" and operator not in state.available_actors:
        return _decision(state, "ACTOR_UNAVAILABLE", operator, "consult_schedule")

    if action == "request_permit":
        if CASE_PERMISSION in state.permissions:
            return _decision(state, "PERMISSION_ALREADY_GRANTED", operator, "read_archive")
        if "CASE_BASIS" not in state.knowledge:
            return _decision(state, "MISSING_CASE_BASIS", operator, "read_case_file")
        updated = replace(state, minute=state.minute + 1,
                          permissions=state.permissions | {CASE_PERMISSION})
        return _decision(state, "PERMIT_GRANTED", operator, "read_archive", updated)

    if action == "read_archive":
        if CASE_PERMISSION not in state.permissions:
            return _decision(state, "MISSING_CASE_PERMISSION", operator, "request_permit")
        if state.stage != "registered":
            return _decision(state, "INVALID_CASE_STAGE", operator, "inspect_case_status")
        updated = replace(state, minute=state.minute + 1, stage="archive_review",
                          knowledge=state.knowledge | {"HISTORY"})
        return _decision(state, "ARCHIVE_READ", operator, "validate_case", updated)

    if state.stage != "archive_review":
        return _decision(state, "INVALID_CASE_STAGE", operator, "read_archive")
    if "HISTORY" not in state.knowledge:
        return _decision(state, "MISSING_HISTORY", operator, "read_archive")
    if "READY" not in state.knowledge:
        return _decision(state, "MISSING_READY", operator, "await_authoritative_ready")
    updated = replace(state, minute=state.minute + 1, stage="validated")
    return _decision(state, "CASE_VALIDATED", operator, "review_outcome", updated)
