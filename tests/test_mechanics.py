"""Negative and positive validation tests: source evidence is never platform certification."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.validate_mechanics import (  # noqa: E402
    CATALOG, CONTRACTS, WORLD, CatalogError,
    load_json, validate_catalog, validate_contracts, validate_world,
)


class MechanicCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_json(CATALOG)
        cls.contracts = load_json(CONTRACTS)
        cls.world = load_json(WORLD)

    def test_exact_inventory_coverage(self):
        counts = validate_catalog(self.catalog)
        self.assertEqual(sum(counts.values()), 45)
        self.assertEqual(dict(counts), {
            "c64_source": 19,
            "c_module_not_wired": 2,
            "host_prototype": 18,
            "design_goal": 6,
        })

    def test_duplicate_id_rejected(self):
        duplicate = copy.deepcopy(self.catalog)
        duplicate["mechanics"][1]["id"] = duplicate["mechanics"][0]["id"]
        with self.assertRaises(CatalogError):
            validate_catalog(duplicate)

    def test_unverified_status_cannot_be_promoted(self):
        promoted = copy.deepcopy(self.catalog)
        promoted["mechanics"][21]["evidence_level"] = "validated"
        with self.assertRaises(CatalogError):
            validate_catalog(promoted)

    def test_paths_must_remain_source_relative(self):
        tampered = copy.deepcopy(self.catalog)
        tampered["mechanics"][0]["source_paths"] = ["../secrets.txt"]
        with self.assertRaises(CatalogError):
            validate_catalog(tampered)

    def test_abbi_ids_are_references_not_newly_minted(self):
        tampered = copy.deepcopy(self.catalog)
        tampered["mechanics"][0]["abbi_candidate_relation"] = "ABBI-M-999"
        with self.assertRaises(CatalogError):
            validate_catalog(tampered)

    def test_contracts_have_provenance_and_invariants(self):
        self.assertEqual(validate_contracts(self.contracts, self.catalog), 11)

    def test_contract_cannot_change_source_evidence(self):
        tampered = copy.deepcopy(self.contracts)
        tampered["contracts"][0]["evidence_level"] = "host_prototype"
        with self.assertRaises(CatalogError):
            validate_contracts(tampered, self.catalog)

    def test_contract_cannot_claim_vice_pass(self):
        tampered = copy.deepcopy(self.contracts)
        tampered["contracts"][0]["platform_verification"]["vice"] = "pass"
        with self.assertRaises(CatalogError):
            validate_contracts(tampered, self.catalog)

    def test_reference_world_topology(self):
        self.assertEqual(validate_world(self.world), 3)

    def test_world_rejects_dangling_room(self):
        tampered = copy.deepcopy(self.world)
        tampered["rooms"][0]["exits"] = [99]
        with self.assertRaises(CatalogError):
            validate_world(tampered)


if __name__ == "__main__":
    unittest.main()
