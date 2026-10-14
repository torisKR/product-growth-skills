<!-- docs-locale: en -->
# Product Growth Skills

> A practical guide to 12 agent skills for solo development and product growth.

[Repository home](../../README.md)

[한국어](../ko/README.md) · [English](../en/README.md) · [日本語](../ja/README.md) · [简体中文](../zh/README.md) · [Français](../fr/README.md)

**Contents** · [Overview](#overview) · [Skills](#skills) · [Quick start](#quick-start) · [Workflow](#workflow) · [Evidence](#evidence) · [Structure](#structure) · [Validation](#validation) · [Safety](#safety) · [Contributing](#contributing)

<a id="overview"></a>
## Overview

This collection connects product decisions to bounded execution and verifiable results. Use it to validate demand, control operating risk, reach users, improve Flutter or Expo apps, and prepare Android delivery.

Start with **`toris-solo-founder`** to coordinate a task, or select a specialist when the problem is already clear. These are instructions and supporting files for an agent, not a hosted service or an autonomous background system.

The five language guides cover the same core material. Skill names, paths, and shell commands stay unchanged; runtime `SKILL.md` files remain in English. Ask the agent to return deliverables in your language unless the target market requires another.

<a id="skills"></a>
## Skill catalog

### Plan and operate

| Skill | Purpose |
|---|---|
| [toris-solo-founder](../../toris-solo-founder/SKILL.md) | Define intent, scope, evidence, handoffs, and reusable lessons |
| [toris-demand-validation](../../toris-demand-validation/SKILL.md) | Separate customer observations from assumptions and design a bounded pilot |
| [toris-cost-guardrails](../../toris-cost-guardrails/SKILL.md) | Map billable operations, cap coverage, concurrent reservations, and residual cost risk |
| [toris-billing-reliability](../../toris-billing-reliability/SKILL.md) | Handle payment verification, duplicate events, subscription access, and recovery |
| [toris-small-sample-experiments](../../toris-small-sample-experiments/SKILL.md) | Define metrics and interpret limited samples, assignment integrity, and retention |

### Reach users

| Skill | Purpose |
|---|---|
| [app-store-listing-creator](../../app-store-listing-creator/SKILL.md) | Prepare store descriptions, icon directions, screenshot plans, and localization notes |
| [seo-geo-optimizer](../../seo-geo-optimizer/SKILL.md) | Inspect technical SEO, search intent, structured data, internal links, GEO, and `llms.txt` |

### Build and ship

| Skill | Purpose |
|---|---|
| [flutter-android-performance](../../flutter-android-performance/SKILL.md) | Measure Flutter startup, frames, CPU, memory, networking, and app size |
| [expo-android-performance](../../expo-android-performance/SKILL.md) | Diagnose Expo performance across JavaScript, UI, and native ownership boundaries |
| [flutter-interactive-design](../../flutter-interactive-design/SKILL.md) | Create responsive Flutter UI, gestures, motion, and bounded 3D with accessible fallbacks |
| [expo-interactive-design](../../expo-interactive-design/SKILL.md) | Build native Expo screens, routing, gestures, motion, and constrained-device fallbacks |
| [toris-flutter-play-store-release](../../toris-flutter-play-store-release/SKILL.md) | Inspect and operate Flutter Android delivery with Fastlane and GitHub Actions; Firebase and Slack actions remain separately scoped |

<a id="quick-start"></a>
## Quick start and optional installation

### Read from a checkout

For a new checkout:

```bash
git clone https://github.com/torisKR/product-growth-skills.git
cd product-growth-skills
```

For an existing checkout at the following location, use it instead of cloning again:

```bash
cd ~/projects/product-growth-skills
```

Give your current agent with local file access this request:

```text
Read toris-solo-founder/SKILL.md from this repository and apply it to my task.
Keep the current agent and project instructions.
Define the outcome, allowed changes, acceptance checks, and cost boundary.
Perform authorized local work and report verified results separately from unknowns.
Record a reusable lesson only when the work provides evidence for it.
Reply in English.
```

This works as an explicit file-reading request; it does not install or reconfigure an agent. Without local file access, provide only the relevant shareable instructions, not private operator notes.

### Preserve sibling references

Keep the complete checkout as the canonical source. Skills may reference `shared-references/`, `research/`, or other skill folders. Copying a single folder without its dependencies can break links. Never include `local-knowledge/` in a shared package.

Native skill discovery, installation locations, and `$skill-name` or slash-command invocation depend on the runtime. Confirm those details for the tool you actually use. Do not infer compatibility with Codex, OpenCodex, Hermes, Grok, agy, or Claude from the presence of a Markdown file. OpenCode and OpenCodex are different names and must remain distinct.

### Standalone Android release package

Only the release package has the lifecycle installer described here. From a trusted repository checkout, preview it first:

```bash
./toris-flutter-play-store-release/install.sh --dry-run
```

After reviewing the proposed global changes and deciding to install:

```bash
./toris-flutter-play-store-release/install.sh
```

For updates, uninstalling, and migration from `flutter-play-store-release`, follow the [release package guide](../../toris-flutter-play-store-release/README.md). Verify the new installation before removing a legacy copy; do not delete global directories manually. The general skills do not install themselves.

The [solo-operator playbook](../../toris-solo-founder/references/solo-operator-playbook.md) adds capacity planning, support triage, cash break-even versus owner income, automation time payback, and recovery decisions. Its [toolkit](../../toris-solo-founder/README.md) includes a read-only calculator and synthetic input. Read it explicitly alongside the founder skill; no automatic loading or business outcome is claimed.

<a id="workflow"></a>
## Working modes and examples

```text
Inspect context → gather evidence → define scope → act → verify → report
```

| Mode | Request | Result |
|---|---|---|
| `execute` | Implement, fix, or improve | Authorized local changes and relevant verification |
| `review` | Review only; do not modify | Findings without file or external-system changes |
| `plan` | Plan only; do not implement | An actionable plan without execution |

Implementation requests default to `execute`. An explicit review or plan takes precedence. See [execution defaults](../../shared-references/execution-defaults.md).

**Demand and cost example**

```text
Read toris-demand-validation/SKILL.md and evaluate this idea.
Separate actual customer evidence from assumptions and propose a bounded pilot.
Then use toris-cost-guardrails/SKILL.md to identify potential paid operations.
Do not contact customers, buy services, or change live billing settings.
```

**Release example**

```text
Read toris-flutter-play-store-release/SKILL.md and inspect this Flutter app.
Prepare and verify the smallest safe Android release path without uploading.
Report the exact checks run and any remaining store, device, or account actions.
```

A handoff should identify **changed**, **verified**, **not verified**, and **remaining owner actions**. Keep implementation, local checks, interaction testing, CI, deployment, public availability, payments, and business results separate.

<a id="evidence"></a>
## Evidence and private knowledge

The founder package preserves distinctions between curated work records, dated user preferences, proposals, and unknowns. Its [provenance reference](../../toris-solo-founder/references/agents-and-provenance.md) explains the six-tool coverage and source limits; it is not a complete export of every tool's raw history.

The four research-backed specialists share the [2026-10-15 research bundle](../../research/solo-developer-2026-10-15/README.md): **16 primary sources, 20 conditional rules, 4 numeric records, 12 synthetic scenarios, and 6 arithmetic fixtures**. Three conflicting items remain quarantined. The numeric records are publisher benchmarks or examples, not owner metrics. Research rules retain `personal_validation: not_run` until actual project evidence supports promotion.

Synthetic scenarios are authored acceptance criteria, not completed agent tests. Source inspection, local tests, runtime compliance, production success, and commercial outcomes are different evidence classes. The [recorded verification](../../research/solo-developer-2026-10-15/VERIFICATION.md) documents the scope of the earlier research task, not a guarantee about the current checkout.

`local-knowledge/torisKR/knowledge-ledger.md` is an optional, Git-ignored local operator record. It is not included in a normal clone and must not be redistributed with skills. Git exclusion is neither encryption nor backup.

Existing deep dives remain in their original languages: [Korean founder guide](../ko/torisKR-solo-founder.md), [Korean research guide](../ko/research-backed-skills.md), and the English research and runtime references. This README translation does not claim to translate those separate documents.

<a id="structure"></a>
## Repository structure

```text
product-growth-skills/
├── README.md
├── docs/
│   ├── ko/README.md
│   ├── en/README.md
│   ├── ja/README.md
│   ├── zh/README.md
│   └── fr/README.md
├── toris-solo-founder/
├── shared-references/
├── research/solo-developer-2026-10-15/
├── scripts/
└── local-knowledge/                   # Local only; Git-ignored
```

The other 11 skill folders are also siblings at the repository root. Each package has `SKILL.md` for invocation and workflow, `agents/openai.yaml` for display metadata and a starter prompt, and `references/` for detailed guidance. The release package additionally contains scripts, templates, tests, and an installation manifest.

<a id="validation"></a>
## Local validation

Run from the repository root using Python 3. The release suite has its own Bash and package prerequisites; consult its guide rather than assuming Python checks cover it.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
bash toris-flutter-play-store-release/tests/run_tests.sh
```

| Check | What it establishes |
|---|---|
| Python tests | Regression cases, language-guide parity, shared commands, and local links |
| Research validator | Source references, dates, evidence classes, numeric metadata, and fixture arithmetic |
| Skill validator | Package structure, interface metadata, links, language boundaries, and existing content checks |
| Git diff check | Whitespace errors in the tracked diff |
| Release suite | The standalone release package's declared test contract |

An undeclared local file such as `.DS_Store` can stop the strict release manifest check. Report the actual failure and unexecuted tests instead of deleting unrelated files or weakening validation. These commands do not verify actual agent behavior, paid transactions, cloud caps, store approval, or business performance.

<a id="safety"></a>
## Safety and scope

Preserve existing user changes, the selected agent, and project instructions. Creating local files does not authorize deployment, public uploads, store submissions, live CMS changes, purchases, account or permission changes, destructive operations, or messages to other people. Those actions require explicit authorization.

Never copy credentials, payment details, customer records, or full conversation histories into shared skills. Verify changing prices, provider behavior, store requirements, and search policies against current primary sources when a real task depends on them. No skill guarantees revenue, rankings, store approval, AI-answer inclusion, or performance gains.

Runtime instructions stay in English. The root README, guides under `docs/ko/`, `docs/en/`, `docs/ja/`, `docs/zh/`, `docs/fr/`, and private human notes can contain localized prose. `SKILL.md`, `AGENTS.md`, and `CLAUDE.md` remain runtime instructions even inside those directories. Link, path, unfinished-content, and credential checks still apply.

<a id="contributing"></a>
## Contributing and license

Read [CONTRIBUTING.md](../../CONTRIBUTING.md). Keep the five guide catalogs, section anchors, shell commands, evidence distinctions, and authorization boundaries aligned when updating documentation. Translate explanations and prompts, not command names or file paths. Existing specialist references keep their own maintenance scope.

The repository uses the [MIT License](../../LICENSE). Linked third-party sources retain their original terms; this license does not relicense their content.
