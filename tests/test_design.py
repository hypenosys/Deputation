"""Machine-check authored narrative promises, distinct from game runtime claims."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.validate_design import (  # noqa: E402
    DesignError, load, validate_feedback, validate_denied_fixtures,
    validate_social, validate_scope,
    validate_prose,
)


class NarrativeDesignContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feedback = load("data/design/feedback_catalog.json")
        cls.social = load("data/mechanics/social_dynamics.json")
        cls.denied_fixtures = load("data/design/denied_actions.v1.json")
        cls.scope = load("data/design/m1_scope.json")
        cls.catalog = load("data/mechanics/extraction.v1.json")

    def test_feedback_matrix_complete(self):
        self.assertEqual(validate_feedback(self.feedback), 16)

    def test_denials_never_advance_clock(self):
        data = copy.deepcopy(self.feedback)
        data["policy"]["denial_mutates_clock"] = True
        with self.assertRaises(DesignError):
            validate_feedback(data)

    def test_denials_cannot_leak_knowledge(self):
        data = copy.deepcopy(self.feedback)
        data["policy"]["hidden_fact_leakage"] = "allowed"
        with self.assertRaises(DesignError):
            validate_feedback(data)

    def test_reference_denial_requires_explanation(self):
        data = copy.deepcopy(self.feedback)
        data["denials"] = [
            d for d in data["denials"] if d["code"] != "MISSING_CASE_PERMISSION"
        ]
        with self.assertRaises(DesignError):
            validate_feedback(data)

    def test_denied_fixtures_reference_codes(self):
        self.assertEqual(validate_denied_fixtures(self.denied_fixtures, self.feedback), 10)

    def test_denied_fixture_without_feedback_rejected(self):
        data = copy.deepcopy(self.denied_fixtures)
        data["fixtures"][0]["expected_code"] = "FABRICATED_REASON"
        with self.assertRaises(DesignError):
            validate_denied_fixtures(data, self.feedback)

    def test_all_25_social_effects(self):
        self.assertEqual(validate_social(self.social), 25)

    def test_trust_matrix_must_not_reverse_incentives(self):
        data = copy.deepcopy(self.social)
        data["matrix"][0]["cells"][0]["next_wait_delta_minutes"] = -10
        with self.assertRaises(DesignError):
            validate_social(data)

    def test_trust_is_not_authorization(self):
        data = copy.deepcopy(self.social)
        data["rule"] = "High trust grants global access."
        with self.assertRaises(DesignError):
            validate_social(data)

    def test_milestone_scope_covers_every_mechanic_once(self):
        self.assertEqual(validate_scope(self.scope, self.catalog), 15)

    def test_dropped_or_duplicate_mechanic_rejected(self):
        data = copy.deepcopy(self.scope)
        data["M2"][0] = data["M1"][0]
        with self.assertRaises(DesignError):
            validate_scope(data, self.catalog)

    def test_case_arc_loop_and_emotional_curves(self):
        arc, loop = validate_prose(ROOT)
        self.assertTrue(300 <= arc <= 500)
        self.assertTrue(175 <= loop <= 225)


if __name__ == "__main__":
    unittest.main()
