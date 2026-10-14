# Receipt, state and business-effect ledger

Research basis: R11-R15 in [evidence.json](../../research/solo-developer-2026-10-15/evidence.json). Receipt durability, transactional coordination and recovery details below are authored design synthesis, not copied provider guarantees.

## Keep three identities

| Identity | Purpose | Typical mistake |
|---|---|---|
| Transport notification | Delivery tracing and duplicate delivery detection | Treating every delivery as a fresh purchase |
| Domain entity/event | Purchase, subscription and provider state | Mixing event arrival with state chronology |
| Business effect | One grant, billing-period allocation or revocation | Granting the same credits through two different event types |

Paddle documents event_id identity, repeated deliveries and potentially reversed arrival order ([S09](https://developer.paddle.com/webhooks/about/how-webhooks-work/)). Verify the original body using the proper endpoint secret and current SDK contract ([S10](https://developer.paddle.com/webhooks/about/signature-verification/)). Do not treat IP allowlisting or a familiar event name as authentication.

## Durable processing pattern

1. Apply bounded payload checks and provider-appropriate authenticity verification.
2. Persist a unique inbox record and a recoverable processing state before acknowledging durable acceptance. If durable persistence fails, do not claim successful receipt. Fit the actual provider's response deadline.
3. In a worker, validate environment, account ownership, product mapping and authoritative state. Enforce business-effect uniqueness in the same transaction as local entitlement updates, or use an idempotent effect/outbox protocol.
4. Mark completion only after the required local invariant holds. An external effect needs a stable idempotency key and a reconciliation strategy because a crash can separate remote success from local recording.
5. Retry recoverable failures with bounds; keep failed records inspectable and provide an authorized repair path. A 200 receipt does not mean the worker succeeded.

For concurrent duplicate receipts, a database uniqueness constraint must be part of the proof, not a pre-insert existence check. A seen-event table without transactional coupling can lose grants or apply them twice. Never log real tokens, raw billing bodies, secrets or customer identities in a shared test report.

## Subscription state is not arrival order

Use entity-scoped transitions and provider chronology/current state. Timestamps alone may tie or fail to order concurrent changes; preserve ambiguity and reconcile rather than guessing. Old active data must not overwrite a later valid expiry or revocation. Scheduled cancellation can preserve access until its effective date, while immediate revocation is a separate case. Paddle documents these distinctions and recommends periodic reconciliation ([S11](https://developer.paddle.com/build/subscriptions/provision-access-webhooks/)).

A proposed reconciliation job needs a bounded customer set, request budget, cursor/checkpoint, idempotent repair and audit output. This skill does not schedule it. Grace and hold decisions must follow the actual provider/product policy; do not blindly grant or revoke every past-due account.

## Google Play branch

Verify the purchase with the backend and bind it to the expected account/product before granting. Play distinguishes PURCHASED and PENDING and requires acknowledgement after fulfilment ([S12](https://developer.android.com/google/play/billing/security)). Use a recoverable acknowledgement path so an app closing cannot lose the action. Test with provider-appropriate fixtures; no real refund or acknowledgement is implied.

RTDN is a change signal, not a complete purchase record ([S13](https://developer.android.com/google/play/billing/rtdn-reference)). Authenticate the transport and fetch current purchase/subscription state. Notification deduplication reduces repeated calls, but a token already associated with a subscription must not suppress later renewal, hold, expiry or restoration updates. Separate one-time grant idempotency from repeatable state reconciliation.

## Acceptance matrix

Exercise tampered body, wrong endpoint secret, wrong environment/account/product, duplicate event, concurrent duplicate, two event types for one credit grant, reversed state updates, tied timestamps, inbox-write failure, worker crash, pending-to-purchased, pending-to-cancelled, acknowledgement failure, future cancellation, immediate revoke and authoritative refresh failure. Run only relevant cases for the chosen product and report omissions.

V07-V09 in [evaluations.json](../../research/solo-developer-2026-10-15/evaluations.json) are pressure scenarios, not executed agent or provider tests. The repository's Python checks validate research metadata and arithmetic, not payment processing.

## Completion receipt

Name environment, build, provider, touched paths, state invariants, executed tests, and remaining device/provider checks. Separate receipt, purchase, grant, restore and settlement results. Delegate store submission mechanics to the existing release skill only when submission is explicitly requested.
