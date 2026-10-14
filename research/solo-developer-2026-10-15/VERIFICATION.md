# Verification receipt

Date: 2026-10-15. Scope: four research-backed skill packages, dated evidence data, offline validation and repository discovery. No production service or agent runtime was tested.

## Executed checks

| Check | Observed result |
|---|---|
| New test suite before implementation | 18 tests ran; 21 failure entries including four registry subtests. Failures identified missing data, validator and skill registration. This was structural RED, not a model-behavior baseline. |
| Complete Python discovery after implementation | 28 tests passed: 18 new research tests and 10 existing documentation tests. |
| Offline research validation | 16 source records, 20 rules, four numeric records, 12 synthetic pressure scenarios and six arithmetic fixtures passed their declared contract. |
| Repository skill validation | 12 skills passed structure, local-link, interface and existing content checks. |
| `git diff --check` | Exit 0. |
| Existing Flutter release suite | Exit 1: `FAIL: unexpected package file: .DS_Store`. The manifest gate stopped subsequent release test groups. |
| Preserved-file inventory hash | Before and after hashes matched for the seven original skill packages, graphify-out and local-knowledge. |

The existing `.DS_Store` modification timestamp was 2026-07-28T17:50:00+0900. It was not removed and the release test was not weakened. The release suite is not reported as passing.

## Reproducible commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
bash toris-flutter-play-store-release/tests/run_tests.sh
```

The preserved-file inventory used relative file paths and SHA-256 for each regular file, sorted the records, then hashed the inventory. Matching inventory hash:

```text
b5b6f7f39213d5704721e73d3917b903a65f753101c296f12c9aa64e96926099
```

Existing README and validator changes from the preceding task were preserved and extended, not overwritten. The founder SKILL.md received a research routing paragraph; its private evidence was not promoted or rewritten. No commits, pushes, global installs, provider switches, paid calls, account changes, customer contacts, deployments or recurring jobs were performed.

## Evidence review

Public primary sources were read for the selected claims. Numeric records were checked against their source sections; the publisher sample-size example was independently recomputed. Conflicting store statistics and spend-cap restoration descriptions remain quarantined. No source article, PDF or raw private dataset was imported.

The source allowlist verifies declared provenance structure, not truth by itself. The semantic review was targeted to the selected rules and numbers, not a claim of exhaustive publication review or complete source-history capture.

## Not verified

No Codex, OpenCodex, Hermes, Grok, agy or Claude behavioral test was run. Synthetic pressure prompts are acceptance criteria, not passing model transcripts. No real customer demand, experiment outcome, revenue, payment, entitlement change, distributed cost reservation, provider spend cap or native skill discovery was exercised. Those require a separate authorized project-level application and receipt.
