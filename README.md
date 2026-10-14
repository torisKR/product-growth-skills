# Product Growth Skills

> Make better product decisions. Build with evidence. Verify the result.

**12 focused agent skills** for solo development and product growth: demand validation, cost control, reliable billing, experiments, store listings, SEO/GEO, Flutter and Expo performance, interactive design, and Android delivery.

[한국어](docs/ko/README.md) · [English](docs/en/README.md) · [日本語](docs/ja/README.md) · [简体中文](docs/zh/README.md) · [Français](docs/fr/README.md)

---

## Start with your next decision

New to the collection? Start with **[toris-solo-founder](toris-solo-founder/SKILL.md)**. Already have a specific problem? Read the matching specialist below.

### Plan and operate

| Skill | Use it to |
|---|---|
| [toris-solo-founder](toris-solo-founder/SKILL.md) | Connect product intent, bounded execution, verification, and reusable lessons |
| [toris-demand-validation](toris-demand-validation/SKILL.md) | Separate customer evidence from assumptions before expanding an MVP |
| [toris-cost-guardrails](toris-cost-guardrails/SKILL.md) | Map billable operations, distinguish alerts from enforcement, and bound concurrent spending |
| [toris-billing-reliability](toris-billing-reliability/SKILL.md) | Handle duplicate events, purchase verification, subscription access, and recovery |
| [toris-small-sample-experiments](toris-small-sample-experiments/SKILL.md) | Interpret limited traffic, experiment integrity, and mature retention cohorts |

### Reach users

| Skill | Use it to |
|---|---|
| [app-store-listing-creator](app-store-listing-creator/SKILL.md) | Prepare store copy, visual directions, screenshot plans, and localization notes |
| [seo-geo-optimizer](seo-geo-optimizer/SKILL.md) | Improve technical SEO, structured data, internal links, and AI-search discoverability |

### Build and ship

| Skill | Use it to |
|---|---|
| [flutter-android-performance](flutter-android-performance/SKILL.md) | Measure and address Flutter startup, rendering, memory, and package-size issues |
| [expo-android-performance](expo-android-performance/SKILL.md) | Investigate Expo performance across JavaScript, UI, and native boundaries |
| [flutter-interactive-design](flutter-interactive-design/SKILL.md) | Build responsive Flutter interactions with motion and accessibility fallbacks |
| [expo-interactive-design](expo-interactive-design/SKILL.md) | Create native Expo screens, gestures, motion, and bounded 3D experiences |
| [toris-flutter-play-store-release](toris-flutter-play-store-release/SKILL.md) | Inspect, configure, verify, and operate Flutter Android delivery within explicit authorization |

## Quick start

For a new checkout:

```bash
git clone https://github.com/torisKR/product-growth-skills.git
cd product-growth-skills
```

Already have the repository? Use that checkout instead of cloning again. Ask your current agent, with local file access, to read a skill:

```text
Read toris-solo-founder/SKILL.md from this repository and apply it to my task.
Keep the current agent and project instructions.
Define the outcome, allowed changes, acceptance checks, and cost boundary.
Perform authorized local work, then separate verified results from unknowns.
Record a reusable lesson only when the work provides evidence for it.
Reply in my language.
```

**Keep the repository layout intact.** Skills can reference sibling `shared-references/`, `research/`, and other skill folders. Copying one folder alone can break those references. This file-reading workflow does not install skills globally or configure any agent.

For native skill discovery, optional installation, and release-package migration, see the [full guide](docs/en/README.md#quick-start) and the [release package guide](toris-flutter-play-store-release/README.md).

## A practical solo-operator toolkit

The [operator toolkit](toris-solo-founder/README.md) adds a [one-person playbook](toris-solo-founder/references/solo-operator-playbook.md), ten conditional operating decisions, and a read-only calculator for available development hours, cash break-even, owner-income targets, and automation time payback. Read it explicitly alongside the founder skill; automatic loading is not assumed. The sample is synthetic, not your business data. See the [Korean walkthrough](docs/ko/solo-operator-playbook.md).

## One workflow, three modes

```text
Inspect context → gather evidence → define scope → act → verify → report
```

| Mode | Result |
|---|---|
| `execute` | Make authorized local changes and verify them; default for implementation requests |
| `review` | Inspect and report without changing files or external systems |
| `plan` | Produce an actionable plan without implementation |

A request to edit local files does **not** authorize spending, deployment, public posting, account changes, destructive operations, or contacting people. See [execution defaults](shared-references/execution-defaults.md).

## Evidence, not promises

The founder skill distinguishes curated experience, historical preferences, proposals, and unknowns. The four research-backed specialists use a [dated evidence bundle](research/solo-developer-2026-10-15/README.md): **16 primary sources, 20 decision rules, 4 numeric records, 12 synthetic scenarios, and 6 arithmetic fixtures**. Three conflicting items remain quarantined.

Research is not personal experience. Synthetic scenarios are not completed agent tests. A local test is not a live release, a real purchase, or a business result. [Provenance](toris-solo-founder/references/agents-and-provenance.md) and [recorded verification](research/solo-developer-2026-10-15/VERIFICATION.md) preserve those limits.

Private operator notes under `local-knowledge/` are Git-ignored, optional, and excluded from distribution. Git exclusion is not encryption or backup.

## Documentation

Each language guide covers the same skill catalog, quick start, working modes, evidence, repository layout, validation, and safety boundaries.

| Language | Guide |
|---|---|
| 한국어 | [한국어 가이드](docs/ko/README.md) |
| English | [English guide](docs/en/README.md) |
| 日本語 | [日本語ガイド](docs/ja/README.md) |
| 简体中文 | [简体中文指南](docs/zh/README.md) |
| Français | [Guide en français](docs/fr/README.md) |

Existing deep dives remain available: [Korean founder guide](docs/ko/torisKR-solo-founder.md), [Korean research guide](docs/ko/research-backed-skills.md), and [research documentation](research/solo-developer-2026-10-15/README.md). Runtime `SKILL.md` instructions remain in English; the human guides and example prompts are localized.

## Validate locally

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_research.py --as-of 2026-10-15
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py
git diff --check
bash toris-flutter-play-store-release/tests/run_tests.sh
```

These checks cover document parity, links, skill metadata, research contracts, arithmetic, and release-package tests. They do not establish native runtime compatibility or commercial outcomes. The strict release manifest check can reject unrelated local files such as `.DS_Store`; report that failure rather than hiding it.

---

[Contributing](CONTRIBUTING.md) · [MIT License](LICENSE)
