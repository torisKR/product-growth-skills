---
name: toris-billing-reliability
description: Use when a solo developer adds or audits subscription access, consumable credits, payment webhooks, Google Play purchase verification, cancellation handling, or recovery from duplicate and missed billing events.
---

# Billing evidence to reliable entitlement

Verify identity, accept events durably and apply the intended business effect once. These are research-derived engineering practices, not evidence of a completed purchase or a production-ready integration.

## Quick start

1. Read the project's payment model, access policy and [execution defaults](../shared-references/execution-defaults.md). No live purchase, refund, acknowledgement, account change or production migration is authorized implicitly.
2. Read [the playbook](references/playbook.md), then R11-R15 in the [research bundle](../research/solo-developer-2026-10-15/README.md). Select the actual provider; do not mix Paddle event IDs with Play purchase tokens.
3. Trace the full path: authenticated receipt, durable inbox, domain verification, account mapping, business-effect ledger, entitlement state, acknowledgement/retry and reconciliation.
4. Identify the smallest broken invariant. For implementation requests, write the regression case first and change only the authorized local path.
5. Exercise duplicate, out-of-order, tampered, pending, wrong-account, crash and recovery cases with synthetic fixtures or an explicitly authorized test environment.
6. Report transport acceptance, authoritative payment state, grant, renewal, revoke and restore separately. A checkout screenshot is not a verified purchase.

## Non-negotiable invariants

- Verify authentic content before trusting it. A parsed client claim cannot grant access.
- A successful receipt response means durable acceptance, not that every downstream business effect completed.
- Deduplicate transport retries and business effects separately. Use atomic state updates or an idempotent recovery design; do not mark processed before an effect that can be lost.
- Arrival order is not event order. Resolve ambiguous/stale state using authoritative provider state and the correct per-entity transition policy.
- Keep cancellation request, effective expiry, billing grace/hold, refund and immediate revocation distinct.
- A previously seen Play purchase token prevents repeated grants, not future authoritative subscription-state refreshes.
- No entitlement is granted for PENDING. Keep account ownership and product eligibility checks server-side where appropriate.

## Definition of done

A documented state model, identity mapping and business-effect key exist. Applicable local tests cover duplicate delivery, ordering, durability and reconciliation failures. Each claimed stage has evidence, with real-device, provider, purchase and production checks explicitly marked when unrun. No secrets or purchase tokens enter public evidence. Use the owner's language and preserve the distinction between this research and actual personal experience.
