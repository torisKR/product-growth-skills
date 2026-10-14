"""Offline research-contract tests; these do not execute any agent or provider."""
from __future__ import annotations

import copy
import importlib
import json
from datetime import date
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "research" / "solo-developer-2026-10-15"
SKILLS = {
    "toris-demand-validation", "toris-cost-guardrails",
    "toris-billing-reliability", "toris-small-sample-experiments",
}


class ResearchBundleTests(unittest.TestCase):
    def load(self):
        self.assertTrue((BUNDLE / "evidence.json").is_file(), "research evidence is missing")
        self.assertTrue((BUNDLE / "evaluations.json").is_file(), "evaluation fixtures are missing")
        self.assertTrue((ROOT / "scripts/validate_research.py").is_file(), "validator is missing")
        evidence = json.loads((BUNDLE / "evidence.json").read_text(encoding="utf-8"))
        evaluations = json.loads((BUNDLE / "evaluations.json").read_text(encoding="utf-8"))
        module = importlib.import_module("validate_research")
        return evidence, evaluations, module

    def errors(self, evidence, evaluations, module):
        return module.validate_bundle(evidence, evaluations, ROOT, date(2026, 10, 15))

    def test_bundle_is_valid(self):
        data, cases, module = self.load()
        self.assertEqual(self.errors(data, cases, module), [])

    def test_all_four_packages_meet_repository_contract(self):
        import validate_skills
        for name in SKILLS:
            with self.subTest(skill=name):
                self.assertIn(name, validate_skills.EXPECTED)
                self.assertEqual(validate_skills.validate_skill(name), [])

    def test_expected_evidence_coverage(self):
        data, cases, _ = self.load()
        self.assertEqual(len(data["sources"]), 16)
        self.assertEqual(len(data["rules"]), 20)
        self.assertEqual({row["skill"] for row in data["rules"]}, SKILLS)
        self.assertEqual(len(cases["scenarios"]), 12)

    def test_duplicate_source_ids_are_rejected(self):
        data, cases, module = self.load()
        data["sources"].append(copy.deepcopy(data["sources"][0]))
        self.assertTrue(any("duplicate" in x for x in self.errors(data, cases, module)))

    def test_broken_rule_source_reference_is_rejected(self):
        data, cases, module = self.load()
        data["rules"][0]["source_ids"] = ["S-missing"]
        self.assertTrue(any("unknown source" in x for x in self.errors(data, cases, module)))

    def test_future_retrieval_date_is_rejected(self):
        data, cases, module = self.load()
        data["sources"][0]["accessed_on"] = "2099-01-01"
        self.assertTrue(any("date" in x for x in self.errors(data, cases, module)))

    def test_nonprimary_source_is_rejected(self):
        data, cases, module = self.load()
        data["sources"][0]["authority"] = "search_snippet_only"
        self.assertTrue(any("authority" in x for x in self.errors(data, cases, module)))

    def test_measurement_requires_population_and_window(self):
        data, cases, module = self.load()
        data["measurements"][0]["population"] = ""
        data["measurements"][0]["window"] = ""
        self.assertTrue(any("population" in x for x in self.errors(data, cases, module)))
        self.assertTrue(any("window" in x for x in self.errors(data, cases, module)))

    def test_nonfinite_numeric_values_are_rejected(self):
        data, cases, module = self.load()
        data["measurements"][0]["value"] = float("nan")
        self.assertTrue(any("finite" in x for x in self.errors(data, cases, module)))

    def test_research_cannot_claim_personal_validation(self):
        data, cases, module = self.load()
        data["rules"][0]["personal_validation"] = "proven"
        self.assertTrue(any("personal_validation" in x for x in self.errors(data, cases, module)))

    def test_synthetic_cases_cannot_claim_agent_execution(self):
        data, cases, module = self.load()
        cases["behavioral_execution"] = "passed_all_models"
        self.assertTrue(any("behavioral_execution" in x for x in self.errors(data, cases, module)))

    def test_quarantined_measurements_cannot_be_promoted_silently(self):
        data, cases, module = self.load()
        data["excluded"][0]["status"] = "verified"
        self.assertTrue(any("quarantined" in x for x in self.errors(data, cases, module)))

    def test_malformed_records_report_errors_instead_of_crashing(self):
        data, cases, module = self.load()
        data["sources"] = [None, 1, {"id": []}]
        self.assertTrue(self.errors(data, cases, module))

    def test_declared_sample_formula_recomputes_publisher_example(self):
        _, _, module = self.load()
        result = module.evaluate_fixture({"kind": "sample_size", "parameters": {
            "baseline": 0.1, "relative_mde": 0.2, "arms": 2}})
        self.assertEqual(result, {"per_arm": 3600, "total": 7200})

    def test_incomplete_and_empty_cohorts_remain_unknown(self):
        _, _, module = self.load()
        for parameters in ({"returned": 0, "eligible": 20, "complete": False},
                           {"returned": 0, "eligible": 0, "complete": True}):
            self.assertIsNone(module.evaluate_fixture({"kind": "retention", "parameters": parameters}))

    def test_mature_cohort_uses_eligible_denominator(self):
        _, _, module = self.load()
        self.assertEqual(module.evaluate_fixture({"kind": "retention", "parameters": {
            "returned": 4, "eligible": 20, "complete": True}}), 0.2)

    def test_budget_includes_in_flight_reservations(self):
        _, _, module = self.load()
        self.assertFalse(module.evaluate_fixture({"kind": "admission", "parameters": {
            "ceiling": 100, "observed": 85, "reserved": 10, "next_max": 6}}))
        self.assertTrue(module.evaluate_fixture({"kind": "admission", "parameters": {
            "ceiling": 100, "observed": 85, "reserved": 10, "next_max": 5}}))

    def test_invalid_fixture_inputs_are_rejected(self):
        _, _, module = self.load()
        invalid = [
            {"kind": "sample_size", "parameters": {"baseline": 0, "relative_mde": .2, "arms": 2}},
            {"kind": "sample_size", "parameters": {"baseline": .1, "relative_mde": 0, "arms": 2}},
            {"kind": "retention", "parameters": {"returned": 3, "eligible": 2, "complete": True}},
            {"kind": "admission", "parameters": {"ceiling": True, "observed": 0, "reserved": 0, "next_max": 1}},
        ]
        for fixture in invalid:
            with self.subTest(fixture=fixture), self.assertRaises(ValueError):
                module.evaluate_fixture(fixture)


if __name__ == "__main__":
    unittest.main()
