# Solo-developer research bundle

Collection date: 2026-10-15. Classification: external research, not personal experience. This is a curated decision dataset, not a customer database, exhaustive systematic review, market forecast or training claim.

## Artifacts and routes

| Artifact | Purpose |
|---|---|
| [evidence.json](evidence.json) | 16 primary sources, 20 conditional decision rules, four numeric records, three quarantined conflicts |
| [evaluations.json](evaluations.json) | 12 synthetic pressure scenarios and six arithmetic fixtures; no executed model conversations |
| [Demand validation](../../toris-demand-validation/SKILL.md) | R01-R05; problem evidence, pilots and decision gates |
| [Cost guardrails](../../toris-cost-guardrails/SKILL.md) | R06-R10; coverage, billable boundaries and reservation design |
| [Billing reliability](../../toris-billing-reliability/SKILL.md) | R11-R15; authenticated events, durable processing and entitlements |
| [Small-sample experiments](../../toris-small-sample-experiments/SKILL.md) | R16-R20; decision feasibility, integrity and cohort maturity |
| [Korean guide](../../docs/ko/research-backed-skills.md) | Operator summary and copy-ready usage prompts |

The existing founder skill remains the overall router. These packages specialize decisions; they do not replace existing store-listing, SEO, framework performance/design, or release tools.

## Collection and analysis method

Select recurring solo-operator risks, look for primary documentation or first-party evidence, open relevant sections, then preserve only a bounded paraphrase, navigation locator and limitation. Convert the observation into an explicitly authored conditional rule with a verification criterion. Link scenarios to rules, and rules to sources. No user source histories, inboxes, payments, private analytics or live consoles were read for this bundle.

Source observations describe what the inspected source supports; `decision` is the package author's synthesis. All rules carry `inference: true` and `personal_validation: not_run`. The primary-source label identifies provenance, not proof of commercial efficacy. Source access date is not publication date or certification that a served/cached representation is the publisher's newest revision.

Use current official documentation again before changing a provider configuration. The source snapshots exposed conflicting representations for some details; Q01-Q03 are deliberately excluded, not resolved by choosing the more convenient value. An inaccessible YC Library page was not adopted as evidence and no derivative retelling was substituted for it.

## Numeric records and interpretation

B01 and B02 preserve two published app-level D35 conversion medians from the same access-method section: hard paywall 10.7%, freemium 2.1%. The report targets 2025 performance from qualifying RevenueCat-integrated subscription apps. These are observational group summaries, not the causal lift from installing a paywall, a Korean market estimate, or an owner's expected performance ([S04](https://www.revenuecat.com/state-of-subscription-apps)). Per-metric underlying sample counts were not available in the inspected section.

B03 and B04 are publisher formula examples, not observed users: a 10% conversion baseline and 20% relative MDE produce 3,600 planned exposures per arm and 7,200 total using the documented approximation ([S14](https://posthog.com/docs/experiments/sample-size-running-time)). The checker independently recomputes this arithmetic. It is not an exact general-purpose power engine.

The six arithmetic fixtures contain one publisher example and five authored synthetic cases. None represents the owner's traffic, money or operational results. Unknown/immature retention remains null; a genuine complete-window zero is different. All cost-fixture numbers are synthetic and unit-consistent, not actual prices.

## Data dictionary

| Section | Grain | Required interpretation |
|---|---|---|
| sources | One inspected canonical public source | ID, publisher, title, authority, URL, access date, locator, limits |
| rules | One reusable conditional decision | Source IDs, observation, inference, trigger, decision, verification, limits |
| measurements | One metric/segment/statistic/window value | Unit, population, period, source locator and evidence class must travel with value |
| excluded | One unresolved discrepancy | Quarantined; not a numeric or automation input |
| scenarios | One authored pressure prompt | Expected response and reject condition; not an executed agent test |
| arithmetic_fixtures | One deterministic example | Input type, evidence class and exact expected result |

## Source directory

| ID | Primary source | Inspected scope |
|---|---|---|
| S01 | [GOV.UK research objectives](https://www.gov.uk/service-manual/user-research/plan-round-of-user-research) | Objectives before method |
| S02 | [GOV.UK interviews](https://www.gov.uk/service-manual/user-research/using-in-depth-interviews) | Neutral prompts and real examples |
| S03 | [GOV.UK usability testing](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing) | Task observation |
| S04 | [RevenueCat 2026 report](https://www.revenuecat.com/state-of-subscription-apps) | Methodology and selected HTML benchmark sections |
| S05 | [Google Cloud budget alerts](https://docs.cloud.google.com/billing/docs/how-to/budgets) | Alert-only boundary |
| S06 | [Google Cloud spend caps](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps) | Eligible scope, delay and exclusions |
| S07 | [Supabase cost control](https://supabase.com/docs/guides/platform/cost-control#spend-cap) | Cap coverage and exclusions |
| S08 | [OWASP API4](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/) | Resource amplification and limits |
| S09 | [Paddle event delivery](https://developer.paddle.com/webhooks/about/how-webhooks-work/) | Event identity and order |
| S10 | [Paddle signatures](https://developer.paddle.com/webhooks/about/signature-verification/) | Authenticity and raw content |
| S11 | [Paddle subscription access](https://developer.paddle.com/build/subscriptions/provision-access-webhooks/) | State-based access and reconciliation |
| S12 | [Google Play purchase security](https://developer.android.com/google/play/billing/security) | Verification and pending purchases |
| S13 | [Google Play RTDN](https://developer.android.com/google/play/billing/rtdn-reference) | Notifications versus authoritative state |
| S14 | [PostHog sample planning](https://posthog.com/docs/experiments/sample-size-running-time) | MDE, planning approximation and interpretation |
| S15 | [Microsoft Research SRM paper page](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/) | Abstract only, not full paper |
| S16 | [PostHog retention](https://posthog.com/docs/product-analytics/retention) | Cohort definitions, incomplete periods and aggregation |

No source article, gated PDF or raw publisher dataset is redistributed. Original source terms remain with the publisher; repository licensing does not relicense linked material.

## Validation and limits

See the [executed verification receipt](VERIFICATION.md): 28 Python tests and the 12-skill structure check passed; the unrelated existing release manifest test still stops on its pre-existing .DS_Store file. Agent-behavior tests were not run.

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
```

The checker is offline and read-only. It checks IDs/references, allowed source categories/hosts, date boundaries, numeric metadata, explicit research/synthetic status, package files, privacy heuristics and fixture arithmetic. A domain allowlist does not prove every claim; semantic source-to-claim review remains necessary. Existing repository checks handle Markdown links and interface metadata.

No LLM pressure test, native skill discovery, live payment, distributed reservation engine, production analytics or deployed intervention was executed. Structural success does not prove runtime obedience or commercial success. Revalidation in a real project is the promotion gate from research-derived practice to personal experience.
