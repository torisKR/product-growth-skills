# A one-person operating loop

This is an authored extension of D07-D12, not twelve more proven personal lessons. Its three external sources and attribution limits are in [operator sources](solo-operator-sources.md). Its calculator checks assumptions, not demand or actual profit. Keep the existing 12-skill collection; do not create an agent fleet or an extra management system just to follow this guide.

## Start with one decision card

Keep this card in the current project's existing notes, not a new mandatory dashboard:

```text
Customer / problem / next decision:
Stage: explore | validate | deliver | operate | pause
One customer-visible outcome:
Evidence already available, source class and date:
Available period / total hours / operating commitments:
Cash ceiling / marginal cost / owner-income assumption:
Smallest complete delivery / explicit exclusions:
One reachable distribution route:
Acceptance evidence / observation window / stop condition:
Risk / reversible fallback / authorized external actions:
Current agent / writer / dependency / next action:
```

Proposed default: one main growth bet and one customer-visible change in progress per shared checkout. An active incident may interrupt it; record where work stopped. This is a starting constraint, not a permanent preference or a measured optimum. Honor a current owner decision to work differently.

## Ten conditional operating decisions

| ID | Situation | Choice and acceptance evidence | Boundary |
|---|---|---|---|
| OP01 | Several products compete for the same solo operator | Name one next decision and the work it displaces. Compare customer evidence, reachable distribution and operating load before features. | Do not restart a closed product from an old note or assign invented opportunity scores. |
| OP02 | Feature work assumes every available hour is coding time | Subtract support, maintenance, distribution and buffer from total capacity. Resize the slice when it does not fit. | Allocations are owner inputs, not a universal 50% formula; unknown hours remain unknown. |
| OP03 | Every support message becomes an immediate feature | Triage by user harm, repeatability, workaround and relevant customer segment. Batch nonurgent requests at an owner-chosen interval. | Security, data loss, unauthorized charges and broken core access can override batching; do not promise round-the-clock support. |
| OP04 | Manual work is repeated | First remove unnecessary steps or use an adequate existing tool. Compare build plus ongoing maintenance with realistic hours saved. | Automation payback is a time scenario; reliability or safety benefits may justify a different decision. No paid tool purchase is implied. |
| OP05 | Revenue looks positive | Separate contribution per payer, fixed cash costs and the owner's income target. Check support capacity at the proposed customer count. | A linear break-even target is not demand, sustainable scale, accounting profit or cash-flow proof. |
| OP06 | A feature has no path to a first user | Attach one specific audience, source-backed message and first-value event to the slice. Prepare local copy alongside implementation. | Views, clicks, first value and payment remain different evidence. Do not publish or contact users implicitly. |
| OP07 | A production incident interrupts development | Assess impact, choose an authorized reversible mitigation, preserve a short timeline, then investigate cause and recurrence. | Recovery is not proved by a dashboard turning green; retest the affected user flow. No unapproved rollback or data mutation. |
| OP08 | A backup exists but recovery is untested | Choose acceptable recovery delay and data-loss window; rehearse a restore into an isolated destination and check data/application consistency. | Backup existence is not a restore receipt. Include object storage and dependencies, not only the database. Never overwrite production as a drill. |
| OP09 | A feature or service should be paused | Draft effects on paid access, customer notice, exports, retention obligations, recurring costs and a reactivation condition. | Pausing growth is not deleting data or stopping paid service obligations. Execution needs explicit scope. |
| OP10 | The user requests commit and push | Stage only reviewed deliverables, inspect staged content and secret/privacy checks, run the applicable tests, commit and push the named branch, then compare remote SHA. | This authorization is for this delivery, not standing permission. A remote commit proves source delivery, not CI or production. |

## Decide what to do next without adding process

**Explore:** a decision brief and likely user/problem are sufficient. Do not build a payment stack for an idea with no demand evidence. Use demand validation for a bounded pilot.

**Validate:** distinguish actual user observations from hypotheses. Estimate delivery time and marginal cost; identify the next disconfirming observation. A failed recruitment route is not automatically proof of no demand.

**Deliver:** one complete user flow plus a visible failure/recovery path, a first-value event and local verification. Let the specialist own framework details; do not rewrite architecture just to reuse this document.

**Operate:** first protect existing customer value, then work on the current bottleneck. A release, a support fix, a distribution experiment and an optimization compete for the same capacity. Keep one concise checkpoint: result, cost, support load, evidence and next decision.

**Pause:** preserve obligations and recoverable assets while deciding which cost or commitment can actually end. Do not call a repository archive a completed business shutdown.

## Offline constraint calculator

Run from the repository root:

```bash
python3 toris-solo-founder/scripts/assess_constraints.py toris-solo-founder/examples/solo-project.json
```

The [example](../examples/solo-project.json) is synthetic. For real planning, supply a separate explicitly named input file or standard input (`-`). Use `input_class: user_supplied`; this label still does not mean the assumptions were verified. Do not commit a private business input. The tool reads only its named input, prints JSON, makes no network calls, writes no files and changes no provider settings.

### Input meanings

All recurring values share `period` (`week`, `month` or `year`) and all monetary amounts use one uppercase three-letter currency label. The script does not verify currencies or convert units. Field names must match the example; use JSON `null` for unknown numeric inputs, not missing fields or guessed zeroes. Values must be finite, nonnegative numbers no larger than 1e12; payer/run counts must be integers. Unknown fields, booleans as numbers and duplicate JSON keys are rejected.

- Capacity is non-overlapping hours for the same period. `feature_hours` is the proposed slice's work within that period; buffer is reserved capacity, not extra availability.
- `net_receipts_per_payer` is already net of refunds and collection/store fees for that period. Do not deduct those fees again in `variable_cost_per_payer`. Include fixed free-tier delivery costs in `fixed_cost` or model them separately; omitted costs make results optimistic.
- `owner_pay_target` is an additional planning target, not an accounting wage rule. Do not include it again in fixed cost. `paying_customers` is a period-consistent average/count chosen for this simplified model; an annual payment is not monthly recurring cash without explicit normalization.
- Automation uses one-time `build_hours`, hours saved from repeated runs, and recurring maintenance. Do not count the same saved work twice in capacity or assume future run volume is certain.

### Transparent formulas

```text
feature capacity = total - support - maintenance - distribution - buffer
unit contribution = net receipts per payer - variable cost per payer
cash break-even payers = ceil(fixed cost / positive unit contribution)
owner-target payers = ceil((fixed cost + owner target) / positive unit contribution)
operating contribution = unit contribution * payers - fixed cost
net automation time saving = minutes saved per run * runs / 60 - maintenance hours
time payback periods = ceil(one-time build hours / positive net time saving)
```

The cash and owner targets are null when contribution is unknown or nonpositive. Missing inputs remain unknown, but independent known calculations still run. Negative capacity and negative operating contribution are not hidden. Decimal strings preserve money/hour calculations without binary-float rounding at ceiling boundaries. Payback is rounded to whole periods.

The synthetic example leaves 12 hours for a 16-hour slice, gives a cash break-even of 15 payers versus 300 for the added owner target, and a three-period time payback. These values describe the example only. They exclude demand, churn, taxes, cash timing, support scaling and changing prices; there is no automatic go/no-go verdict.

## A compact support and recovery notebook

```text
Issue / affected user flow / first observed time:
Impact and affected population, or unknown:
Environment / artifact / recent change evidence:
Safe workaround / explicit authorization:
Mitigation performed and exact result:
Source/restore point / data-loss window / destination:
User-flow and consistency checks:
Remaining exposure / communication draft / approval:
Next preventive change / owner / review condition:
```

One person can perform coordination, operations and communication sequentially; a role list is not a claim of extra staff. Draft public updates but send only when authorized. Use a restore test with temporary isolated resources only if its cost and access are approved. Record rollback compatibility with data migrations; restoring application code alone may not restore data correctness.

## Promotion to personal knowledge

Keep externally informed OP rules as proposals until the owner's actual execution supports them. Add a dated receipt to D07-D12 rather than inventing a new success story. A calculator test validates arithmetic and input handling only. A successful push can support D01/D02 source-delivery evidence, but cannot promote demand, profitability, recovery or model behavior to verified status.
