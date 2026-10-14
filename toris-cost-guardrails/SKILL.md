---
name: toris-cost-guardrails
description: Use when a solo developer exposes paid AI, messaging, storage or compute operations, reviews a cloud budget, adds concurrent workers, or must distinguish spending alerts from enforceable limits.
---

# Cost guardrails at the billable operation

Inspect what can spend, what can stop it, and what remains billable. This research-derived skill is not an invoice audit or a guarantee of zero overshoot.

## Quick start

1. Read project instructions and [execution defaults](../shared-references/execution-defaults.md). Preserve current providers and agent configuration; no purchases, billing changes, service suspension or new integrations are implied.
2. Read [the playbook](references/playbook.md) and R06-R10 in the [research bundle](../research/solo-developer-2026-10-15/README.md).
3. Inventory expensive endpoints, inner operations, units, provider/plan, fixed charges, retries, concurrency, queues and user identity. Mark unknown prices or costs instead of setting them to zero.
4. Separate alerts, provider enforcement and application admission control. Verify current coverage and exclusions; do not generalize an alerts-only warning to every provider feature.
5. In an implementation request, add the smallest safe local controls and non-billable fixtures. Reserve bounded cost atomically before dispatch, reconcile completed cost, and handle unknown in-flight work conservatively.
6. Report covered paths, residual exposure, failure behavior and checks actually run. Remote billing settings and a live spend test are separate authorized actions.

## Required controls

Define limits on billable fan-out, payload/output size, duration, retries, concurrent work and authenticated principal. Apply a global backstop as well as per-user limits where abuse can create multiple accounts. A UI balance or a limiter on outer HTTP requests alone is insufficient.

For an admission design, evaluate `observed + reserved + next_max <= ceiling` in an atomic transaction or equivalent serialized operation. The offline arithmetic fixture only illustrates the inequality; it does not implement concurrency or provider enforcement. When cost cannot be bounded or priced, do not claim a hard ceiling.

## Failure boundaries

A timeout does not prove remote work stopped. Do not release its reservation until the billable outcome is known or a conservative settlement policy applies. Do not disable an entire production project as an unapproved cost-control shortcut. Define a safe degraded response and owner-approved restoration path.

## Definition of done

A cost-control matrix specifies scope, unit, evidence date, enforcement point and exclusions. Authorized local changes have boundary, retry, concurrency and crash tests as applicable. Unknown prices, uncovered charges and non-instant provider enforcement remain explicit. Actual billing or spend changes are not claimed without receipts. Return a Korean handoff when the user works in Korean; do not claim personal cost savings from this research alone.
