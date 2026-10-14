---
name: toris-small-sample-experiments
description: Use when a solo developer has limited traffic, compares activation or retention cohorts, plans an A/B test, interprets a few conversions, or encounters missing periods and inconsistent experiment allocation.
---

# Small-sample decisions without false winners

Choose a decision the available evidence can support. This research-derived skill does not turn weak traffic into statistical certainty or convert synthetic rows into owner metrics.

## Quick start

1. Read project instructions and [execution defaults](../shared-references/execution-defaults.md). Keep analytics reads, local implementation and live tracking changes within their separate authorization boundaries.
2. Read [the playbook](references/playbook.md), then R16-R20 in the [research bundle](../research/solo-developer-2026-10-15/README.md).
3. Define the metric, assignment/analysis unit, population, exclusions, period, timezone, numerator and denominator. Preserve unknowns; do not fill missing values with zero.
4. For an experiment, assess baseline, meaningful effect, eligible exposure and chosen statistical method before launch. Do not invent a universal minimum audience or fixed run duration.
5. Check assignment/exposure integrity, duplicate identities and maturation before reading uplift. Diagnose credible sample-ratio mismatch before selecting a winner.
6. Use mature comparable cohorts for retention. If traffic cannot support a decision, propose a bounded qualitative or larger-effect test and label it exploratory, not a randomized causal result.
7. Report counts, uncertainty, method, limitations and the next decision. Implement only authorized local tracking/tests; do not publish flags or change a production analytics system implicitly.

## Guardrails

Observed relative change is descriptive, not automatically significant. Planned sample completion is not a successful experiment. Do not interpret lack of significance as proof of no effect. Do not apply unrestricted peeking to a fixed-horizon test; a sequential or Bayesian engine needs its actual decision/stopping contract.

Keep subscription survival, return-event retention, activation and payer conversion separate. Define Day-N versus on-or-after, entry rules, cohort maturity and eligible denominator. Weighted aggregates need original counts; a mean of percentages is a different statistic.

The offline calculator reproduces a publisher planning example and simple scalar fixtures only. It does not compute a production experiment verdict, test SRM, implement identity resolution or guarantee exact power.

## Definition of done

The metric contract, cohort manifest and source classes are complete. Relevant data-quality checks and calculations have actually run; unresolved failures block definitive outcome claims. The readout can conclude supported, contradicted, inconclusive or invalid-data. Counts and caveats travel with any exported number. No actual users, revenue or completed experiment are claimed from the bundled examples. Return the result in the user's language.
