#!/usr/bin/env python3
"""Read-only validation of research provenance and illustrative arithmetic.

No network, provider calls, file writes, or model-behavior evaluation occur.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
from decimal import Decimal, ROUND_CEILING
import json
import math
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

import validate_skills as repository

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "research/solo-developer-2026-10-15"
SKILLS = {
    "toris-demand-validation", "toris-cost-guardrails",
    "toris-billing-reliability", "toris-small-sample-experiments",
}
AUTHORITIES = {"primary_guidance", "primary_documentation", "primary_report", "primary_research"}
PRIMARY_HOSTS = {
    "www.gov.uk", "www.revenuecat.com", "docs.cloud.google.com", "supabase.com",
    "owasp.org", "developer.paddle.com", "developer.android.com", "posthog.com", "www.microsoft.com",
}


def _number(value: Any) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("expected a finite numeric value, not a boolean or text")
    value = Decimal(str(value))
    if not value.is_finite() or value < 0:
        raise ValueError("numeric input must be finite and nonnegative")
    return value


def evaluate_fixture(fixture: dict[str, Any]) -> Any:
    """Evaluate a scalar example, not a production statistical or billing engine."""
    if not isinstance(fixture, dict) or not isinstance(fixture.get("parameters"), dict):
        raise ValueError("fixture and parameters must be objects")
    p = fixture["parameters"]
    try:
        if fixture.get("kind") == "sample_size":
            baseline, mde = _number(p["baseline"]), _number(p["relative_mde"])
            if not 0 < baseline < 1 or mde <= 0 or baseline * (1 + mde) > 1:
                raise ValueError("baseline and relative_mde must define a possible positive uplift")
            if type(p["arms"]) is not int or p["arms"] != 2:
                raise ValueError("this planning approximation supports two equal arms only")
            n = 16 * baseline * (1 - baseline) / (baseline * mde) ** 2
            per_arm = int(n.to_integral_value(rounding=ROUND_CEILING))
            return {"per_arm": per_arm, "total": per_arm * 2}
        if fixture.get("kind") == "retention":
            if type(p["returned"]) is not int or type(p["eligible"]) is not int:
                raise ValueError("retention counts must be integers")
            returned, eligible = _number(p["returned"]), _number(p["eligible"])
            if returned > eligible or type(p["complete"]) is not bool:
                raise ValueError("invalid retention counts or maturity flag")
            if not p["complete"] or eligible == 0:
                return None
            return float(returned / eligible)
        if fixture.get("kind") == "admission":
            ceiling, observed, reserved, next_max = (
                _number(p[key]) for key in ("ceiling", "observed", "reserved", "next_max")
            )
            return observed + reserved + next_max <= ceiling
    except KeyError as exc:
        raise ValueError(f"missing fixture parameter: {exc.args[0]}") from exc
    raise ValueError("unknown fixture kind")


def validate_bundle(data: Any, evaluations: Any, root: Path = ROOT,
                    today: date | None = None) -> list[str]:
    """Return actionable schema/provenance errors without changing the bundle."""
    errors: list[str] = []
    today = today or datetime.now(ZoneInfo("Asia/Seoul")).date()
    if not isinstance(data, dict) or not isinstance(evaluations, dict):
        return ["evidence and evaluations must be JSON objects"]

    def required(row: dict, fields: tuple[str, ...], label: str) -> None:
        for key in fields:
            if not isinstance(row.get(key), str) or not row[key].strip():
                errors.append(f"{label}: nonempty {key} is required")

    def valid_date(value: Any, label: str, upper: date) -> date | None:
        try:
            parsed = date.fromisoformat(value) if isinstance(value, str) else None
            if parsed is None or parsed > upper:
                raise ValueError
            return parsed
        except (ValueError, TypeError):
            errors.append(f"{label}: invalid or future date")
            return None

    def records(value: Any, label: str) -> list[dict]:
        if not isinstance(value, list) or not value:
            errors.append(f"{label}: nonempty record array required")
            return []
        result, ids = [], set()
        for index, row in enumerate(value):
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                errors.append(f"{label}[{index}]: object with string id required")
                continue
            if row["id"] in ids:
                errors.append(f"{label}: duplicate id {row['id']}")
            ids.add(row["id"])
            result.append(row)
        return result

    def references(value: Any, available: set[str], label: str, kind: str) -> None:
        if not isinstance(value, list) or not value:
            errors.append(f"{label}: nonempty {kind} references required")
            return
        for ref in value:
            if not isinstance(ref, str) or ref not in available:
                errors.append(f"{label}: unknown {kind} reference")

    if data.get("schema_version") != 1 or evaluations.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("classification") != "external_research_not_personal_experience":
        errors.append("classification must preserve external research provenance")
    collected = valid_date(data.get("collected_on"), "collected_on", today) or today
    sources = records(data.get("sources"), "sources")
    source_ids = {row["id"] for row in sources}
    urls: set[str] = set()
    for row in sources:
        label = row["id"]
        required(row, ("publisher", "title", "url", "locator", "limitations"), label)
        valid_date(row.get("accessed_on"), label, collected)
        if row.get("authority") not in AUTHORITIES:
            errors.append(f"{label}: unsupported source authority")
        url = row.get("url")
        if isinstance(url, str):
            try:
                parts = urlsplit(url)
                if parts.scheme != "https" or parts.hostname not in PRIMARY_HOSTS or parts.username or parts.password:
                    raise ValueError
                if url in urls:
                    errors.append(f"{label}: duplicate source URL")
                urls.add(url)
            except ValueError:
                errors.append(f"{label}: URL must be an approved public primary source")

    rules = records(data.get("rules"), "rules")
    rule_ids = {row["id"] for row in rules}
    rules_by_skill: dict[str, set[str]] = {skill: set() for skill in SKILLS}
    for row in rules:
        label = row["id"]
        required(row, ("source_observation", "decision", "trigger", "verification", "limits"), label)
        references(row.get("source_ids"), source_ids, label, "source")
        skill = row.get("skill")
        if not isinstance(skill, str) or skill not in SKILLS:
            errors.append(f"{label}: unknown skill")
        else:
            rules_by_skill[skill].add(label)
        if type(row.get("inference")) is not bool:
            errors.append(f"{label}: explicit inference boolean required")
        if row.get("personal_validation") != "not_run":
            errors.append(f"{label}: personal_validation must remain not_run in this research snapshot")

    for skill, ids in rules_by_skill.items():
        if not ids:
            errors.append(f"{skill}: missing rule coverage")
        for relative in ("SKILL.md", "references/playbook.md", "agents/openai.yaml"):
            if not (root / skill / relative).is_file():
                errors.append(f"{skill}: missing {relative}")

    measurements = records(data.get("measurements"), "measurements")
    for row in measurements:
        label = row["id"]
        required(row, ("metric", "segment", "statistic", "population", "window", "source_locator", "limitations"), label)
        references([row.get("source_id")], source_ids, label, "source")
        if row.get("evidence_class") not in {"published_benchmark", "publisher_example"}:
            errors.append(f"{label}: unsupported measurement evidence_class")
        try:
            number = _number(row.get("value"))
            if row.get("unit") == "percent" and number > 100:
                errors.append(f"{label}: percentage outside 0..100")
            elif row.get("unit") not in {"percent", "exposures"}:
                errors.append(f"{label}: unsupported unit")
        except ValueError:
            errors.append(f"{label}: measurement must be finite and nonnegative")

    for row in records(data.get("excluded"), "excluded"):
        required(row, ("reason", "locator"), row["id"])
        references(row.get("source_ids"), source_ids, row["id"], "source")
        if row.get("status") != "quarantined":
            errors.append(f"{row['id']}: excluded evidence must remain quarantined")

    if evaluations.get("data_class") != "synthetic_test_scenarios":
        errors.append("evaluation data_class must identify synthetic scenarios")
    if evaluations.get("behavioral_execution") != "not_run":
        errors.append("behavioral_execution must remain not_run; metadata tests do not execute models")
    scenario_coverage: set[str] = set()
    for row in records(evaluations.get("scenarios"), "scenarios"):
        required(row, ("prompt", "expected", "reject"), row["id"])
        references(row.get("rule_ids"), rule_ids, row["id"], "rule")
        skill = row.get("skill")
        if not isinstance(skill, str) or skill not in SKILLS:
            errors.append(f"{row['id']}: unknown scenario skill")
        else:
            scenario_coverage.add(skill)
    if scenario_coverage != SKILLS:
        errors.append("scenarios: incomplete four-skill coverage")
    for row in records(evaluations.get("arithmetic_fixtures"), "arithmetic_fixtures"):
        if row.get("data_class") not in {"synthetic", "publisher_example"}:
            errors.append(f"{row['id']}: arithmetic data_class required")
        if row.get("data_class") == "publisher_example":
            references([row.get("source_id")], source_ids, row["id"], "source")
        try:
            actual = evaluate_fixture(row)
            if "expected" not in row or type(actual) is not type(row["expected"]) or actual != row["expected"]:
                errors.append(f"{row['id']}: arithmetic result differs from expected")
        except (ValueError, TypeError, ArithmeticError) as exc:
            errors.append(f"{row['id']}: invalid arithmetic fixture: {exc}")

    # Reuse, rather than weaken, the repository's existing privacy heuristics.
    text = json.dumps([data, evaluations], ensure_ascii=False)
    for name, pattern in (("machine path", repository.MACHINE_HOME),
                          ("private key", repository.PRIVATE_KEY_BLOCK),
                          ("service credentials", repository.SERVICE_ACCOUNT_PAYLOAD),
                          ("unfinished content", repository.UNFINISHED)):
        if pattern.search(text):
            errors.append(f"bundle contains {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", type=date.fromisoformat, default=None,
                        help="date boundary for reproducible snapshot validation (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        data = json.loads((BUNDLE / "evidence.json").read_text(encoding="utf-8"))
        cases = json.loads((BUNDLE / "evaluations.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"Research validation failed: {exc}")
        return 1
    errors = validate_bundle(data, cases, today=args.as_of)
    if errors:
        print("Research validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validated {len(data['sources'])} sources, {len(data['rules'])} rules, "
          f"{len(data['measurements'])} numeric records, {len(cases['scenarios'])} scenarios, "
          f"and {len(cases['arithmetic_fixtures'])} arithmetic fixtures.")
    print("Agent behavior, live providers and owner business outcomes: not tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
