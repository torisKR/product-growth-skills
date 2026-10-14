#!/usr/bin/env python3
"""Read-only, single-period solo-operator planning; no network or file writes.

All money uses one declared currency and all recurring values share one period.
Inputs are scenarios or user-supplied assumptions, never verified by this tool.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_CEILING, localcontext
import json
from pathlib import Path
import re
import sys
from typing import Any

FIELDS = {
    "capacity": {"total_hours", "support_hours", "maintenance_hours", "distribution_hours",
                 "buffer_hours", "feature_hours"},
    "economics": {"net_receipts_per_payer", "variable_cost_per_payer", "fixed_cost",
                  "owner_pay_target", "paying_customers"},
    "automation": {"build_hours", "minutes_saved_per_run", "runs_per_period", "maintenance_hours_per_period"},
}
TOP = {"schema_version", "input_class", "currency", "period", *FIELDS}
MAX_INPUT_BYTES = 1024 * 1024


def _keys(value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise ValueError(f"{label}: exact fields required; use explicit null for unknown numeric inputs")


def _number(value: Any, label: str) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f"{label}: expected a number or null, not boolean or text")
    result = Decimal(str(value))
    if not result.is_finite() or not 0 <= result <= Decimal("1e12"):
        raise ValueError(f"{label}: number must be finite and between 0 and 1e12")
    return result


def _display(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if value == 0:
        return "0"
    return format(value.normalize(), "f")


def _ceiling(numerator: Decimal, denominator: Decimal) -> int:
    return int((numerator / denominator).to_integral_value(rounding=ROUND_CEILING))


def assess(data: dict[str, Any]) -> dict[str, Any]:
    """Evaluate independent known inputs without treating missing values as zero."""
    _keys(data, TOP, "input")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("schema_version must be integer 1")
    if data["input_class"] not in ("synthetic", "user_supplied"):
        raise ValueError("input_class must identify synthetic or user_supplied inputs")
    if not isinstance(data["currency"], str) or not re.fullmatch(r"[A-Z]{3}", data["currency"]):
        raise ValueError("currency must be one uppercase three-letter label; no conversion is performed")
    if data["period"] not in ("week", "month", "year"):
        raise ValueError("period must be week, month or year and apply to all recurring inputs")
    parsed, unknown, flags = {}, [], []
    for section, fields in FIELDS.items():
        _keys(data[section], fields, section)
        parsed[section] = {}
        for key in sorted(fields):
            label, value = f"{section}.{key}", data[section][key]
            if key in ("paying_customers", "runs_per_period") and value is not None and type(value) is not int:
                raise ValueError(f"{label}: count must be an integer or null")
            parsed[section][key] = _number(value, label)
            if value is None:
                unknown.append(label)
    c, e, a = (parsed[key] for key in ("capacity", "economics", "automation"))
    with localcontext() as context:
        context.prec = 40
        operating = (c[key] for key in ("support_hours", "maintenance_hours", "distribution_hours", "buffer_hours"))
        operating = list(operating)
        available = c["total_hours"] - sum(operating) if c["total_hours"] is not None and None not in operating else None
        fits = available >= c["feature_hours"] if available is not None and c["feature_hours"] is not None else None
        if available is not None and available < 0:
            flags.append("capacity_overcommitted")
        if fits is False:
            flags.append("feature_exceeds_available_capacity")

        margin = e["net_receipts_per_payer"] - e["variable_cost_per_payer"] if e["net_receipts_per_payer"] is not None and e["variable_cost_per_payer"] is not None else None
        cash_target = owner_target = contribution = None
        if margin is not None:
            if margin <= 0:
                flags.append("nonpositive_unit_contribution")
            elif e["fixed_cost"] is not None:
                cash_target = _ceiling(e["fixed_cost"], margin)
                if e["owner_pay_target"] is not None:
                    owner_target = _ceiling(e["fixed_cost"] + e["owner_pay_target"], margin)
            if e["paying_customers"] is not None and e["fixed_cost"] is not None:
                contribution = margin * e["paying_customers"] - e["fixed_cost"]
                if contribution < 0:
                    flags.append("cash_costs_not_covered")

        saved = payback = None
        if all(a[key] is not None for key in ("minutes_saved_per_run", "runs_per_period", "maintenance_hours_per_period")):
            saved = a["minutes_saved_per_run"] * a["runs_per_period"] / 60 - a["maintenance_hours_per_period"]
            if saved <= 0:
                flags.append("automation_has_no_positive_time_saving")
            elif a["build_hours"] is not None:
                payback = _ceiling(a["build_hours"], saved)
        if unknown:
            flags.append("incomplete_inputs")
        return {
            "schema_version": 1, "input_class": data["input_class"], "currency": data["currency"],
            "period": data["period"], "business_outcome_verified": False,
            "capacity": {"available_feature_hours": _display(available), "feature_fits": fits},
            "economics": {"contribution_per_payer": _display(margin), "cash_break_even_payers": cash_target,
                          "owner_target_payers": owner_target, "operating_contribution": _display(contribution)},
            "automation": {"net_saved_hours_per_period": _display(saved), "payback_periods": payback},
            "unknown_inputs": unknown, "flags": flags,
            "limits": "Linear, single-period planning only. No demand, churn, taxes, cash timing, support scaling, or real outcomes verified. Monetary and hour results are decimal strings.",
        }


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError("nonfinite JSON number")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="explicit JSON input path, or - for standard input")
    args = parser.parse_args()
    try:
        if args.input == "-":
            raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        else:
            with Path(args.input).open("rb") as stream:
                raw = stream.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("input exceeds 1 MiB")
        data = json.loads(raw.decode("utf-8"), parse_float=Decimal,
                          parse_constant=_reject_constant, object_pairs_hook=_unique_object)
        result = assess(data)
    except (OSError, ValueError, TypeError, ArithmeticError, RecursionError) as exc:
        print(f"Invalid input: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
