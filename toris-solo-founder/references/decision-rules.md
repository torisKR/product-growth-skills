# Reusable decision rules

This register separates six lessons supported by the owner's curated work records from historical preferences and proposed operating methods. The source scope is documented in [agents and provenance](agents-and-provenance.md). The underlying conversations were not re-opened during this collection.

## Rules supported by curated experience

| ID | Trigger | Decision | Failure this avoids | Evidence and limit |
|---|---|---|---|---|
| D01 | A checkout is already dirty or several agents touched it | Capture initial status, assign ownership, review the relevant diff, and transfer only the intended change | Cleaning away unrelated work or attributing another writer's edits to this task | E01: October 2026 selective-stage and remote-SHA experience, recorded in the October 14 curated note; not a current remote check |
| D02 | Someone says a task is complete | Attach a separate receipt to each claimed stage | Treating a type check as interaction QA or a build as a release | E02: July Claude local completion preceded a separately authorized deployment; October Codex work explicitly excluded browser/build checks |
| D03 | A metadata warning suggests filling a missing value | Use the actual content source, omit unknown facts, or add genuine content before describing it | Invented authors, modification timestamps, word counts, or article images | E03: October source/DOM/structured-data reconciliation; not a promise of indexing or rich results |
| D04 | A deployment command succeeds but the site looks unchanged | Compare source, artifact, target domain, response body, and headers for the same URL | Declaring live success too early or diagnosing every mismatch as caching | E04: July deployment had temporarily mixed old/new responses; historical, not current service evidence |
| D05 | A payment product loads or a checkout screen appears | Record catalog, checkout, purchase, entitlement, and restoration independently | Calling a cancelled checkout a successful purchase or revenue | E05: September Cursor record stopped after checkout cancellation; purchase and entitlement remained unverified |
| D06 | The same task appears in several agent records | Distinguish execution app, relay, requested model, resolved provider/model, and artifact; link only with correlating evidence | Double-counting work or attributing a provider request to an editor | E06: curated Codex/Claude/Cursor/OpenCodex provenance analysis; HTTP success is only a request-level result |

## Historical preferences and bounded proposals

These are not newly measured productivity or revenue findings. Apply them only when they fit the current request.

| ID | Trigger | Working decision | Basis and qualification |
|---|---|---|---|
| D07 | Considering a new dependency, paid service, or custom platform | First inspect an adequate existing/free option and include maintenance, support, and coordination cost | W01: inspected workspace instruction. It is a directive, not a measured cost-saving result |
| D08 | The owner selected a single-agent workflow | Keep that agent as the operating mode; introduce delegation only if explicitly requested | C01: historical Hermes-only preference. Later use of other tools does not make a permanent global routing rule |
| D09 | Selecting an agent workspace | Evaluate the actual workflow: memory pressure, responsiveness, project/session management, editing needs, remote access, and agent invocation | C02: dated user preferences; no current product ranking or benchmark is asserted |
| D10 | Producing related posts across channels | Keep one factual brief and adapt the purpose, wording, and call to action for each channel | C03: requested Grok content-role consolidation; actual bot reconfiguration was not verified |
| D11 | An idea attracts interest but its operating case is unclear | Write a testable customer/problem hypothesis, bounded cost, distribution route, and continue/change/stop decision before expanding | C04: user emphasis on monetization and prior shutdown decisions; the worksheet is a proposal, not a validated business model |
| D12 | A session produced something useful | Promote a conditional lesson with evidence and limits, not an entire transcript or an unexecuted plan | W02: inspected vault pipeline; promotion is a deliberate knowledge step, not automatic proof of execution |

## How to apply a rule

Write the relevant ID, the triggering condition, the choice made, the evidence inspected, and the exception or unresolved risk. A rule should narrow a decision, not become a ritual detached from the task.

Example: "D05 applies. The store checkout appeared and was cancelled. The release note may say checkout verified; purchase, entitlement, and restore remain unverified. No charge was authorized."

## Conflict handling

1. Respect the current explicit request and access boundaries.
2. Apply current project instructions before unrelated global habits.
3. Keep each historical directive's date, project, and mode; do not compare unlike scopes as if they were contradictory.
4. When a preference truly changes, retain the old entry as superseded and record the new one. Do not claim a change happened merely because a different tool appears in a later task.
5. Keep a candidate rule provisional when the evidence only contains an assistant proposal, a forwarded summary, or an incomplete result.
