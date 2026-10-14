"""Visual identity, UX and narrative data regression tests (stdlib only)."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.validate_visual import (  # noqa: E402
    PALETTE, CONTENT, WIREFRAMES, VisualContractError,
    validate_copy, validate_palette, validate_wireframes, contrast,
)


class VisualContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.palette = json.loads(PALETTE.read_text(encoding="utf-8"))
        cls.copy = json.loads(CONTENT.read_text(encoding="utf-8"))

    def test_all_16_colors_and_contrast_pairs(self):
        out = validate_palette(self.palette)
        self.assertEqual(out["colors"], 16)
        self.assertGreaterEqual(out["pairs"], 10)

    def test_low_contrast_is_detected(self):
        changed = copy.deepcopy(self.palette)
        changed["colors"]["ink"] = changed["colors"]["paper"]
        with self.assertRaises(VisualContractError):
            validate_palette(changed)

    def test_exact_contrast_formula_for_black_white(self):
        self.assertAlmostEqual(contrast("#000000", "#FFFFFF"), 21.0)

    def test_all_three_svg_wireframes_parse(self):
        self.assertEqual(validate_wireframes(WIREFRAMES), 3)

    def test_narrative_copy_has_actors_and_results(self):
        data = validate_copy(self.copy)
        self.assertGreaterEqual(data["actors"], 4)

    def test_wrong_case_is_rejected(self):
        altered = copy.deepcopy(self.copy)
        altered["case_id"] = "EXP-9999"
        with self.assertRaises(VisualContractError):
            validate_copy(altered)

    def test_missing_actor_motivation_is_rejected(self):
        altered = copy.deepcopy(self.copy)
        altered["actors"][0]["motivation"] = ""
        with self.assertRaises(VisualContractError):
            validate_copy(altered)

    def test_status_copy_is_never_only_color(self):
        for code, event in self.copy["results"].items():
            self.assertGreaterEqual(len(event["label"]), 3, code)
            self.assertTrue(event["next"], code)

    def test_godot_source_and_project_present(self):
        for p in ("project.godot", "godot/Desk.tscn",
                  "godot/Desk.gd", "godot/case_state.gd"):
            self.assertGreater((ROOT / p).stat().st_size, 100)


if __name__ == "__main__":
    unittest.main()
