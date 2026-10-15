"""Host-only golden traces for the proposed EXP-0042 game grammar."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.authority_reference import CaseState  # noqa: E402
from tools.simulate_trace import (  # noqa: E402
    TraceError, advance_to, feedback, load, outcome, perform,
    replay, run_file, snapshot, state_sha, WORLD, FEEDBACK,
)

WIN = ROOT / "data/world/simulation_trace.json"
LOSS = ROOT / "data/world/simulation_trace_failure.json"


class GameGrammarTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = load(WORLD)
        cls.feedback = load(FEEDBACK)

    def test_six_cycle_winning_route(self):
        report = run_file(WIN)
        self.assertEqual(len(report["cycles"]), 6)
        self.assertEqual(sum(len(c["actions"]) for c in report["cycles"]), 20)
        self.assertEqual(report["outcome"], "validated")
        self.assertEqual(report["final_state"]["minute"], 28)
        self.assertIn("ARCHIVE_CASE_0042", report["final_state"]["permissions"])
        self.assertEqual(report["final_state"]["knowledge"],
                         ["CASE_BASIS", "HISTORY", "READY", "REVIEW"])

    def test_losing_route_expires_without_fake_victory(self):
        report = run_file(LOSS)
        self.assertEqual(report["outcome"], "expired")
        self.assertEqual(report["final_state"]["minute"], 30)
        self.assertEqual(report["final_state"]["stage"], "archive_review")
        final_action = report["cycles"][-1]["actions"][-1]
        self.assertEqual(final_action["code"], "DEADLINE_EXPIRED")
        self.assertTrue(final_action["unchanged"])
        self.assertEqual(final_action["feedback"]["remaining_minutes"], 0)

    def test_byte_identical_replay_and_state_hash(self):
        a, b = run_file(WIN), run_file(WIN)
        self.assertEqual(a, b)
        self.assertEqual(a["final_state_sha256"], b["final_state_sha256"])
        self.assertEqual(len(a["final_state_sha256"]), 64)

    def test_false_expected_result_is_detected(self):
        modified = copy.deepcopy(load(WIN))
        modified["cycles"][0]["actions"][0]["expect_code"] = "TELEPORT"
        with self.assertRaisesRegex(TraceError, "expected.*TELEPORT"):
            replay(modified, self.world, self.feedback)

    def test_false_expected_time_is_detected(self):
        modified = copy.deepcopy(load(WIN))
        modified["cycles"][0]["actions"][0]["expect_minute"] = 3
        with self.assertRaisesRegex(TraceError, "expected minute"):
            replay(modified, self.world, self.feedback)

    def test_first_request_denied_idempotent_and_explained(self):
        initial = CaseState(room="REGISTRY", minute=2)
        before = state_sha(initial)
        after, code = perform(initial, {"type": "request_permit"}, self.world)
        self.assertIs(after, initial)
        self.assertEqual(code, "MISSING_CASE_BASIS")
        self.assertEqual(before, state_sha(after))
        info = feedback(code, "request_permit", after.minute, self.feedback)
        self.assertIn("SECRETARY", info["actor"])
        self.assertEqual(info["remaining_minutes"], 28)
        self.assertTrue(info["next_action"])

    def test_wrong_exit_keeps_clock_and_all_knowledge(self):
        initial = CaseState(room="COURTYARD", minute=3,
                            knowledge=frozenset({"REVIEW"}))
        after, code = perform(initial, {"type": "move", "target": "ARCHIVE"}, self.world)
        self.assertEqual(code, "INVALID_EXIT")
        self.assertIs(after, initial)
        self.assertEqual(snapshot(after), snapshot(initial))

    def test_all_intermediate_milestones_crossed(self):
        initial = CaseState(room="ARCHIVE", minute=8)
        later = advance_to(initial, 27)
        self.assertEqual(later.minute, 27)
        self.assertEqual(later.stage, "archive_review")
        self.assertEqual(later.knowledge, frozenset({"REVIEW", "READY"}))
        self.assertEqual(initial.stage, "registered")

    def test_milestones_not_backdated(self):
        with self.assertRaisesRegex(TraceError, "monotonic"):
            advance_to(CaseState(minute=18), 17)

    def test_unimplemented_trust_stays_constant(self):
        end = run_file(WIN)["final_state"]
        self.assertEqual(end["trust"], [0, 0, 0, 0, 0])

    def test_presentation_projection_is_noop(self):
        state = CaseState(room="REGISTRY", minute=15)
        before = state_sha(state)
        result = feedback("MISSING_CASE_PERMISSION", "read_archive",
                          state.minute, self.feedback)
        self.assertEqual(result["remaining_minutes"], 15)
        self.assertEqual(before, state_sha(state))

    def test_success_is_terminal_for_world_actions(self):
        state = CaseState(room="ARCHIVE", minute=28, stage="validated",
                          permissions=frozenset({"ARCHIVE_CASE_0042"}))
        before = state_sha(state)
        after, code = perform(state, {"type": "move", "target": "REGISTRY"}, self.world)
        self.assertIs(after, state)
        self.assertEqual(code, "CASE_ALREADY_VALIDATED")
        self.assertEqual(before, state_sha(after))
        info = feedback(code, "move", state.minute, self.feedback)
        self.assertTrue(info["next_action"])
        self.assertEqual(perform(state, {"type": "inspect_case_status"}, self.world),
                         (state, "STATUS_VIEWED"))

    def test_expiry_is_terminal_for_world_actions(self):
        state = CaseState(room="ARCHIVE", minute=30, stage="archive_review")
        after, code = perform(state, {"type": "move", "target": "REGISTRY"}, self.world)
        self.assertIs(after, state)
        self.assertEqual(code, "DEADLINE_EXPIRED")
        self.assertEqual(after.minute, 30)

    def test_invalid_action_refused_without_fabrication(self):
        state = CaseState()
        with self.assertRaisesRegex(TraceError, "unknown action"):
            perform(state, {"type": "secret_backdoor"}, self.world)
        self.assertEqual(state, CaseState())

    def test_explicit_wait_is_not_a_free_rejection(self):
        state = CaseState(minute=24)
        after, code = perform(state, {"type": "wait", "minutes": 3}, self.world)
        self.assertEqual((code, after.minute), ("WAITED", 27))
        self.assertEqual(outcome(after), "ongoing")
        with self.assertRaisesRegex(TraceError, "explicit wait"):
            perform(state, {"type": "wait", "minutes": 0}, self.world)

    def test_actor_wrong_room_rejected_before_scope(self):
        state = CaseState(room="COURTYARD", minute=4)
        after, code = perform(state, {"type": "read_archive"}, self.world)
        self.assertEqual(code, "WRONG_ROOM")
        self.assertIs(after, state)


if __name__ == "__main__":
    unittest.main()
