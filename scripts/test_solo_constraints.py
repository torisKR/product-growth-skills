"""Offline acceptance tests for solo-operator planning, not business outcomes."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "toris-solo-founder"
SCRIPT = PACKAGE / "scripts/assess_constraints.py"
EXAMPLE = PACKAGE / "examples/solo-project.json"


def scenario():
    return {
        "schema_version": 1, "input_class": "synthetic", "currency": "KRW", "period": "month",
        "capacity": {"total_hours": 40, "support_hours": 10, "maintenance_hours": 8,
                     "distribution_hours": 6, "buffer_hours": 4, "feature_hours": 16},
        "economics": {"net_receipts_per_payer": 10000, "variable_cost_per_payer": 3000,
                      "fixed_cost": 100000, "owner_pay_target": 2000000, "paying_customers": 12},
        "automation": {"build_hours": 6, "minutes_saved_per_run": 10, "runs_per_period": 18,
                       "maintenance_hours_per_period": 1},
    }


class SoloConstraintTests(unittest.TestCase):
    def assessor(self):
        self.assertTrue(SCRIPT.is_file(), "solo constraint calculator is missing")
        spec = importlib.util.spec_from_file_location("solo_constraints", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.assess

    def test_time_after_operating_work_is_the_feature_budget(self):
        result = self.assessor()(scenario())
        self.assertEqual(result["capacity"]["available_feature_hours"], "12")
        self.assertFalse(result["capacity"]["feature_fits"])

    def test_negative_capacity_is_visible(self):
        data = scenario()
        data["capacity"]["support_hours"] = 30
        result = self.assessor()(data)
        self.assertEqual(result["capacity"]["available_feature_hours"], "-8")
        self.assertIn("capacity_overcommitted", result["flags"])

    def test_break_even_and_owner_target_are_separate(self):
        result = self.assessor()(scenario())["economics"]
        self.assertEqual(result["contribution_per_payer"], "7000")
        self.assertEqual(result["cash_break_even_payers"], 15)
        self.assertEqual(result["owner_target_payers"], 300)
        self.assertEqual(result["operating_contribution"], "-16000")

    def test_nonpositive_margin_does_not_invent_a_payer_target(self):
        data = scenario()
        data["economics"]["variable_cost_per_payer"] = 11000
        result = self.assessor()(data)
        self.assertIsNone(result["economics"]["cash_break_even_payers"])
        self.assertIn("nonpositive_unit_contribution", result["flags"])

    def test_unknown_values_remain_unknown(self):
        data = scenario()
        data["capacity"]["support_hours"] = None
        data["economics"]["variable_cost_per_payer"] = None
        result = self.assessor()(data)
        self.assertIsNone(result["capacity"]["available_feature_hours"])
        self.assertIsNone(result["economics"]["cash_break_even_payers"])
        self.assertIn("capacity.support_hours", result["unknown_inputs"])
        self.assertIn("economics.variable_cost_per_payer", result["unknown_inputs"])

    def test_unknown_customer_count_does_not_hide_known_margin(self):
        data = scenario()
        data["economics"]["paying_customers"] = None
        result = self.assessor()(data)["economics"]
        self.assertEqual(result["cash_break_even_payers"], 15)
        self.assertIsNone(result["operating_contribution"])

    def test_zero_fixed_cost_has_zero_cash_break_even(self):
        data = scenario()
        data["economics"]["fixed_cost"] = 0
        self.assertEqual(self.assessor()(data)["economics"]["cash_break_even_payers"], 0)

    def test_money_arithmetic_does_not_round_up_float_noise(self):
        data = scenario()
        data["economics"].update(net_receipts_per_payer=0.3, variable_cost_per_payer=0.1,
                                 fixed_cost=0.6, owner_pay_target=0)
        result = self.assessor()(data)["economics"]
        self.assertEqual(result["contribution_per_payer"], "0.2")
        self.assertEqual(result["cash_break_even_payers"], 3)

    def test_automation_includes_recurring_maintenance(self):
        result = self.assessor()(scenario())["automation"]
        self.assertEqual(result["net_saved_hours_per_period"], "2")
        self.assertEqual(result["payback_periods"], 3)

    def test_automation_without_savings_has_no_payback(self):
        data = scenario()
        data["automation"]["maintenance_hours_per_period"] = 4
        result = self.assessor()(data)
        self.assertIsNone(result["automation"]["payback_periods"])
        self.assertIn("automation_has_no_positive_time_saving", result["flags"])

    def test_invalid_numeric_inputs_are_rejected(self):
        assess = self.assessor()
        for value in (True, -1, float("nan"), float("inf"), "100", [], {}):
            data = scenario()
            data["capacity"]["total_hours"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                assess(data)

    def test_counts_must_be_nonnegative_integers(self):
        assess = self.assessor()
        for value in (0.5, True, -1):
            data = scenario()
            data["economics"]["paying_customers"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                assess(data)

    def test_metadata_and_extra_fields_are_rejected(self):
        assess = self.assessor()
        invalid = []
        for key, value in (("currency", "won"), ("period", "mixed"), ("input_class", "proven"),
                           ("schema_version", True)):
            data = scenario()
            data[key] = value
            invalid.append(data)
        data = scenario()
        data["capacity"]["period"] = "week"
        invalid.append(data)
        data = scenario()
        del data["capacity"]["support_hours"]
        invalid.append(data)
        for data in invalid:
            with self.subTest(data=data), self.assertRaises(ValueError):
                assess(data)

    def test_zero_payers_produces_a_real_cost_not_missing(self):
        data = scenario()
        data["economics"]["paying_customers"] = 0
        self.assertEqual(self.assessor()(data)["economics"]["operating_contribution"], "-100000")

    def test_input_is_not_modified(self):
        data = scenario()
        before = copy.deepcopy(data)
        result = self.assessor()(data)
        self.assertEqual(data, before)
        self.assertEqual(result["input_class"], "synthetic")
        self.assertFalse(result["business_outcome_verified"])

    def test_cli_json_stdin(self):
        self.assertTrue(SCRIPT.is_file(), "calculator CLI is missing")
        run = subprocess.run([sys.executable, str(SCRIPT), "-"], input=json.dumps(scenario()),
                             text=True, capture_output=True, check=False)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["economics"]["cash_break_even_payers"], 15)

    def test_cli_rejects_duplicate_keys_and_invalid_json(self):
        self.assertTrue(SCRIPT.is_file(), "calculator CLI is missing")
        for payload in ('{"a":1,"a":2}', '{', 'null', 'NaN'):
            run = subprocess.run([sys.executable, str(SCRIPT), "-"], input=payload,
                                 text=True, capture_output=True, check=False)
            with self.subTest(payload=payload):
                self.assertEqual(run.returncode, 2)
                self.assertIn("Invalid input", run.stderr)
                self.assertNotIn("Traceback", run.stderr)

    def test_sample_and_route_are_available(self):
        self.assertTrue(EXAMPLE.is_file(), "synthetic example is missing")
        data = json.loads(EXAMPLE.read_text())
        self.assertEqual(data, scenario())
        # The core instruction edit was denied by the tool's security check.
        # Verify the explicitly delivered README entry, not automatic skill loading.
        text = (PACKAGE / "README.md").read_text()
        self.assertIn("references/solo-operator-playbook.md", text)
        for locale in ("en", "ko", "ja", "zh", "fr"):
            self.assertIn("solo-operator-playbook.md", (ROOT / "docs" / locale / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
