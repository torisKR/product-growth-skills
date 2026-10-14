# Contracts, receipts, and knowledge harvest

These are reusable blank forms, not completed work or confirmed facts. Fill them from the current request and inspected evidence. Use `unknown`, `not run`, or `not authorized` where appropriate rather than inventing values.

## 1. Product outcome contract

```text
Product / decision:
Customer and triggering situation:
Problem and current workaround:
Evidence already available:
Smallest end-to-end outcome:
Explicit exclusions:
First-value event:
Acquisition / distribution hypothesis:
Monetization hypothesis:
Owner-approved cash ceiling:
Owner-approved time / capacity budget:
Acceptance evidence:
Review point:
Continue condition:
Change condition:
Stop condition:
External actions authorized:
Unknowns and assumptions:
```

A hypothesis is not a validated result. Do not describe an owner-unapproved limit as an agreed constraint.

## 2. Dependency-aware task card

```text
Task ID:
Outcome contract:
Depends on:
Owner / selected agent:
Workspace / isolation:
Allowed write paths:
Read-only dependencies:
Forbidden or shared paths:
Acceptance checks:
Required approval boundary:
State: queued | ready | running | verifying | blocked | done
Evidence and artifacts:
Blocking reason:
Next handoff:
```

Independent read-only work can overlap. Shared-path writes require coordination or serialization. A dependency is satisfied by accepted evidence, not merely by a predecessor's finished message.

## 3. Development and release receipt

```text
Requested scope:
Initial unrelated changes:
Changes made:
Reviewed diff:
Commands actually run and results:
Interaction checks and device/browser/build:
CI commit / run result:
Artifact / submission receipt:
Public URL or store-track verification:
Payment stage reached:
Business metrics, if actually available:
Not run / not authorized / blocked:
Remaining risk:
Next decision or action:
```

Keep local checks, CI, deployment, public availability, purchase, entitlement, and business performance separate. Do not include credentials or sensitive customer details in evidence.

## 4. Small business experiment record

```text
Decision this experiment informs:
Customer segment:
Hypothesis:
Intervention and comparison, if any:
Metric definition:
Numerator and denominator:
Observation period:
Data source and collection limits:
Approved cost and capacity bounds:
Observed counts / amounts:
Confounders and uncertainty:
Result: supported | contradicted | inconclusive
Continue / change / stop decision:
Reusable lesson candidate:
```

Do not present a dashboard percentage without its population and period. Preserve uncertainty for small samples and avoid causal claims unsupported by the design.

## 5. Multi-channel content brief

```text
Real event or product change:
Intended audience and problem:
Primary evidence:
Claim and limitation:
Approved public facts:
Private facts to exclude:
One destination / desired action:
Channel-specific angle:
Text / visuals needed:
Asset source and rights status:
Reviewer / approval state:
Publication: draft | approved | published-and-verified
Publication receipt, only if actually published:
Measurement plan:
```

Use one factual brief, not identical copy everywhere. A prepared upload package is still a draft until the external action is authorized and verified.

## 6. Reusable knowledge card

```text
Rule ID and title:
Status: candidate | supported | superseded
Observed date:
Event date:
Situation / trigger:
Options considered:
Decision actually made:
Action actually performed:
Evidence class and source keys:
Verified outcome:
Unverified boundary:
Why it worked or failed (fact versus inference):
Use again when:
Do not apply when:
Supersedes / related rule:
Privacy: private | sanitized-shareable
```

A reusable rule needs a condition and a limit. "Use a better model" is not a useful lesson. "Preserve the existing checkout changes and verify only the paths owned by this task" can be used again and audited.

## Harvest procedure

1. Start with the receipt and actual evidence. Keep requested actions, observed actions, and assistant reports separate.
2. Identify a repeated failure mode or a consequential decision. Do not create a new skill for every session.
3. Search existing rules; merge duplicates without erasing the older evidence or changing its date.
4. Promote supported conditional knowledge. Keep proposals and unresolved experiments in project notes or the candidate queue.
5. Retain source keys and uncertainty. Put raw pointers and personal directives in the private dossier, not in a public skill.
6. Record a changed preference with date, scope, and supersession. Never leave contradictory directives active for the same scope.
7. Validate links, metadata, source coverage, privacy, and the claimed acceptance evidence before reporting completion.

Respect each source vault's own rules. Do not move its inbox, rewrite old journals, run a harvest command, or publish its notes merely because this repository organizes a copy of the knowledge. In this collection the original vaults remain unchanged.

## Suggested review, not a scheduled automation

At an owner-chosen review point, inspect the candidate queue, stale decisions, unresolved checks, operating costs, and actual user signals. Decide what to keep, merge, supersede, or stop. Create a recurring automation only after a separate explicit request and successful tool confirmation.
