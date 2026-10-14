"""Behavioral regression for the reference authorization contract, before M1 port.

Denied action is a *query with feedback*: zero authoritative mutation, zero
time charge, zero trust or knowledge leakage. This does not certify the C64.
"""
from __future__ import annotations

import copy
import sys
import unittest
from dataclasses import asdict, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.authority_reference import (  # noqa: E402
    CASE_PERMISSION, CaseState, evaluate,
)


class DeniedPermitIdempotenceTests(unittest.TestCase):
    def assert_denied_unchanged(self, state, action, reason, **kwargs):
        before = copy.deepcopy(asdict(state))
        first = evaluate(state, action, **kwargs)
        second = evaluate(state, action, **kwargs)
        self.assertFalse(first.accepted)
        self.assertEqual(first.code, reason)
        self.assertIs(first.state, state)
        self.assertIs(second.state, state)
        self.assertEqual(asdict(state), before)
        self.assertEqual(first, second)
        self.assertEqual(first.remaining_minutes, max(0, 30 - state.minute))
        self.assertTrue(first.next_action)
        return first

    def test_denied_permission_does_not_advance_time_or_trust(self):
        self.assert_denied_unchanged(CaseState(minute=19), "request_permit", "MISSING_CASE_BASIS")

    def test_wrong_room(self):
        state = CaseState(room="COURTYARD", knowledge=frozenset({"CASE_BASIS"}))
        self.assert_denied_unchanged(state, "request_permit", "WRONG_ROOM")

    def test_unavailable_issuer(self):
        state = CaseState(knowledge=frozenset({"CASE_BASIS"}),
                          available_actors=frozenset({"ARCHIVIST"}))
        self.assert_denied_unchanged(state, "request_permit", "ACTOR_UNAVAILABLE")

    def test_impersonated_issuer(self):
        state = CaseState(knowledge=frozenset({"CASE_BASIS"}))
        self.assert_denied_unchanged(state, "request_permit", "ACTOR_NOT_AUTHORIZED", actor="ARCHIVIST")

    def test_expired_deadline(self):
        state = CaseState(minute=30, knowledge=frozenset({"CASE_BASIS"}))
        self.assert_denied_unchanged(state, "request_permit", "DEADLINE_EXPIRED")

    def test_grant_is_case_scoped_and_duplicate_denied(self):
        initial = CaseState(minute=17, knowledge=frozenset({"CASE_BASIS"}))
        result = evaluate(initial, "request_permit")
        self.assertTrue(result.accepted)
        self.assertEqual(result.state.minute, 18)
        self.assertEqual(result.state.permissions, frozenset({CASE_PERMISSION}))
        self.assertEqual(initial.permissions, frozenset())
        self.assertEqual(result.state.trust, initial.trust)
        self.assert_denied_unchanged(result.state, "request_permit", "PERMISSION_ALREADY_GRANTED")

    def test_archive_disclosure_denied_no_knowledge_leak(self):
        state = CaseState(room="ARCHIVE", minute=22)
        self.assert_denied_unchanged(state, "read_archive", "MISSING_CASE_PERMISSION")
        self.assertNotIn("HISTORY", state.knowledge)

    def test_invalid_stage_rejected(self):
        state = CaseState(room="ARCHIVE", stage="validated",
                          permissions=frozenset({CASE_PERMISSION}))
        self.assert_denied_unchanged(state, "read_archive", "INVALID_CASE_STAGE")

    def test_missing_ready_cannot_validate(self):
        state = CaseState(room="ARCHIVE", stage="archive_review", knowledge=frozenset({"HISTORY"}))
        self.assert_denied_unchanged(state, "validate_case", "MISSING_READY")

    def test_missing_history_cannot_validate(self):
        state = CaseState(room="ARCHIVE", stage="archive_review", knowledge=frozenset({"READY"}))
        self.assert_denied_unchanged(state, "validate_case", "MISSING_HISTORY")

    def test_complete_reference_happy_path(self):
        start = CaseState(minute=25, stage="archive_review",\n                          knowledge=frozenset({"CASE_BASIS", "READY"}))
        granted = evaluate(start, "request_permit")
        self.assertTrue(granted.accepted)
        self.assertEqual(granted.state.minute, 26)
        archived = evaluate(replace(granted.state, room="ARCHIVE"), "read_archive")
        self.assertTrue(archived.accepted)
        self.assertEqual(archived.state.stage, "archive_review")
        self.assertIn("HISTORY", archived.state.knowledge)
        finished = evaluate(archived.state, "validate_case")
        self.assertTrue(finished.accepted)
        self.assertEqual(finished.state.stage, "validated")
        self.assertEqual(finished.state.minute, 28)

    def test_cannot_validate_after_deadline(self):
        state = CaseState(room="ARCHIVE", stage="archive_review", minute=31,
                          knowledge=frozenset({"HISTORY", "READY"}))
        self.assert_denied_unchanged(state, "validate_case", "DEADLINE_EXPIRED")

    def test_replayable_json_denial_fixtures(self):
        import json
        fixture_file = ROOT / "data/design/denied_actions.v1.json"
        fixture = json.loads(fixture_file.read_text(encoding="utf-8"))
        self.assertEqual(fixture["schema"], "deputation.denied_actions.v1")
        self.assertEqual(len(fixture["fixtures"]), 10)
        for spec in fixture["fixtures"]:
            with self.subTest(spec["id"]):
                state_data = dict(spec["state"])
                for key in ("permissions", "knowledge", "available_actors"):
                    if key in state_data:
                        state_data[key] = frozenset(state_data[key])
                if "trust" in state_data:
                    state_data["trust"] = tuple(state_data["trust"])
                state = CaseState(**state_data)
                kwargs = {"actor": spec["actor"]} if "actor" in spec else {}
                self.assert_denied_unchanged(
                    state, spec["action"], spec["expected_code"], **kwargs
                )

    def test_unknown_action_does_not_write(self):
        state = CaseState()
        with self.assertRaises(ValueError):
            evaluate(state, "magically_grant_global_access")
        self.assertEqual(state, CaseState())


if __name__ == "__main__":
    unittest.main()
