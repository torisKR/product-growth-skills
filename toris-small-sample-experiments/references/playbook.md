# Metric contracts, power and mature cohorts

Research basis: R16-R20 in [evidence.json](../../research/solo-developer-2026-10-15/evidence.json). No owner analytics were fetched. The protocol below is authored synthesis; publication examples and synthetic fixtures are not business results.

## Metric contract

```text
Decision / primary metric / guardrail metrics:
Assignment unit / analysis unit:
Eligible population / entry event / identity rule:
Numerator / denominator / deduplication:
Exposure event / outcome event / attribution window:
Start / end / timezone / ingestion cutoff:
Baseline source and period:
Minimum meaningful effect, absolute and relative:
Statistical engine / stopping and decision rule:
Mature-cohort requirement / exclusions:
Missingness and known quality failures:
```

Separate assignment from actual exposure. Do not exclude inconvenient outcome failures after randomization just to improve a variant. Where account-level treatment creates shared behavior, user-level independence may be invalid; choose the unit before analysis.

## Feasibility before rollout

PostHog documents a planning approximation with baseline, variance and minimum detectable effect inputs ([S14](https://posthog.com/docs/experiments/sample-size-running-time)). Its published example is preserved as B03/B04, not as a universal target. The bundled checker uses Decimal arithmetic to recompute:

```text
d = baseline * relative_MDE
n_per_arm = ceil(16 * baseline * (1 - baseline) / d^2)
```

This approximation is associated with conventional two-arm power planning. It is not exact for every baseline, allocation, outcome distribution or sequential engine. Rare outcomes, clustering, multiple metrics and changed allocation require the selected statistical method's own calculation. Avoid importing the same coefficient into arbitrary experiments.

Use actual eligible exposure rather than page views to assess feasibility. Unknown baseline/variance remains an estimate with sensitivity, not an invented historical measure. Compare a smaller scope, a meaningfully larger change or a bounded qualitative study when the intended effect is not measurable with available traffic. These alternatives do not establish the same causal evidence as randomization.

## Integrity gate before an effect claim

Verify configured allocation, stable assignment, event completeness, identity merging, eligibility filters and instrumentation consistency. Sample-ratio mismatch can signal serious experiment defects ([S15](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/)). A difference of one user is not automatically SRM; use an appropriate test and investigate the mechanism. Do not blindly rebalance the sample after seeing outcomes.

A positive raw rate is not a reliable winner. Report descriptive absolute/relative differences separately from intervals and the chosen statistical decision. Lack of significance may mean insufficient information rather than equivalence. Fixed-horizon, sequential and Bayesian analyses have different stopping/decision contracts; name the one actually used. The checker does not make this inference for you.

## Retention maturity

Specify entry event, return event, first-ever versus recurring entry, and exact versus rolling return criteria. PostHog documents these choices, incomplete periods and weighted versus simple averages ([S16](https://posthog.com/docs/product-analytics/retention)).

For a mature-cohort analysis, a subject is eligible only after the entire required return window plus chosen ingestion delay has elapsed. Include immature subjects in a separate pending count, not the denominator of the completed horizon. If none are eligible, return null. A real zero requires a complete observation window with no qualifying returns.

Compute aggregate return rate from summed returned/eligible counts when that is the chosen statistic; do not average differently sized cohort percentages and label it weighted. Keep event-retention apart from the subscription-level definition used in RevenueCat benchmarks. Different populations or periods cannot be repaired by making their column names match.

## Synthetic walkthrough and receipt

V10-V12 and A01-A04 in [evaluations.json](../../research/solo-developer-2026-10-15/evaluations.json) exercise false-winner, allocation and maturity mistakes. The arithmetic checks are deterministic; no statistical significance or live event pipeline is tested.

Deliver metric contract, actual source query/filter description, cohort counts, quality findings, calculations, uncertainty and decision. Use `invalid-data` when integrity blocks interpretation and `inconclusive` when valid evidence is insufficient. Neither means that the product necessarily failed. Put private user-level details only in an authorized destination, never this public research bundle.
