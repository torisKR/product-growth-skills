# A bounded cost-control design

Research basis: R06-R10 in [evidence.json](../../research/solo-developer-2026-10-15/evidence.json). The application-level design below is authored synthesis. It has not been deployed or measured on the owner's services.

## Three distinct mechanisms

| Mechanism | Question to answer | Evidence required |
|---|---|---|
| Alert | Who learns the threshold was crossed? | Notification rule, coverage and reporting delay |
| Provider enforcement | Which new usage is actually blocked? | Current plan/service documentation and authorized configuration evidence |
| Application admission | Can this billable operation start now? | Atomic check/reservation and local concurrency/crash tests |

Google Cloud alerts-only budgets are not enforcement ([S05](https://docs.cloud.google.com/billing/docs/how-to/budgets)). Eligible project/service spend caps do enforce some new usage, but allow lag, in-flight completion and ongoing-charge exceptions ([S06](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)). Do not rely on reset behavior from this snapshot: Q03 records conflicting retrieved descriptions.

Supabase's cap has explicit exclusions including compute; inspect the actual coverage instead of treating a plan fee as an invoice ceiling ([S07](https://supabase.com/docs/guides/platform/cost-control#spend-cap)). No plan switch or configuration change is performed by reading this guide.

## Inventory the real billable boundary

```text
Operation / endpoint:
Authorized identity and abuse boundary:
Provider / plan / pricing source / checked date:
Billable unit and upper bound:
Maximum batch / input / output / duration:
Retry policy and maximum attempts:
Concurrent work and queued reservations:
Fixed charges and cap exclusions:
Currency / taxes / credits treatment:
Alert / enforcement / local admission:
Failure response and restoration owner:
```

Unrestricted inner operations can defeat a request-frequency limit. OWASP recommends bounding resource consumption and provider spending exposure ([S08](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)). Use synthetic local fixtures; never flood a real endpoint to demonstrate the risk.

## Admission and settlement pattern

Proposed state machine: `requested -> reserved -> dispatched -> settled`, with explicit `rejected`, `cancelled-before-dispatch`, and `outcome-unknown` branches.

Inside a database transaction or equivalent serialized operation, assign an idempotent operation ID, verify eligibility and bounded unit cost, include existing reservations, then reserve before dispatch. A retry with the same operation ID must not allocate or spend twice. Period rollover and multiple currencies require separate ledgers; do not erase outstanding reservations at midnight.

After provider completion, settle the actual charge and release only the unused reservation. If a provider times out, keep the reservation until its result is resolved; timeout is not proof of cancellation. A lease expiring must not authorize a second billable dispatch of work that might still be running. Reconciliation needs an explicit owner, audit trail and conservative fallback.

This is not a universal hard-cap implementation. Unknown model/tool fan-out, price changes, asynchronous provider charging or unbounded output can break an assumed upper bound. Fail closed for optional paid work when a trustworthy bound is missing, while preserving required account, recovery and support paths where possible. Make outage/restoration trade-offs explicit.

## Local acceptance cases

Verify request below/at/above the ceiling, batch amplification, maximum retry behavior, concurrent admissions, crash after reservation, timeout after dispatch, duplicate operation IDs, currency mismatch and billing-period rollover. Use the project's existing transaction test harness rather than proving concurrency with a single scalar assertion.

V04-V06 and A05-A06 in [evaluations.json](../../research/solo-developer-2026-10-15/evaluations.json) supply pressure prompts and illustrative arithmetic. A05 rejects proposed work once reservations are counted; A06 accepts exactly at the scalar boundary. Neither fixture validates real distributed behavior or provider invoices.

## Handoff

Record the matrix, touched local files, exact tests, approximate exposure model and uncovered risk. Separately label provider settings not inspected, live tests not authorized, and prices not refreshed. A local guard does not authorize changing billing accounts, disabling resources, sending alerts, or creating an always-on monitor.
