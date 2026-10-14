# Research-backed solo skills implementation plan

**Goal:** Add reusable research-backed practices for a solo developer, with inspectable evidence data rather than invented personal experience.

**Architecture:** Four focused skill packages extend the existing founder router. A dated JSON research bundle separates primary sources, source observations, authored decision rules, numeric observations, quarantined conflicts, and synthetic evaluation scenarios. Standard-library validation provides reproducible local checks; it does not claim model-behavior verification.

**Tech stack:** Markdown, JSON, YAML interface metadata, Python standard library.

**Request contract:** The owner explicitly requested research, dataset creation, and local skills in this repository. Preserve the current agent and existing changes. Additional paid services/model calls: none. No runtime installation, account changes, commits, pushes, external publishing, or production writes.

## Scope and design

Create `toris-demand-validation`, `toris-cost-guardrails`, `toris-billing-reliability`, and `toris-small-sample-experiments`. Each contains SKILL.md, references/playbook.md, and agents/openai.yaml. Do not duplicate app-store assets, SEO, framework performance, or release installation.

Create `research/solo-developer-2026-10-15/evidence.json`, `evaluations.json`, and README.md. Evidence rows contain stable IDs, primary source links and locators, retrieval dates, scope and limitations; no private data or copied source articles. Preserve unsupported or conflicting facts as excluded records. Benchmarks are not owner metrics or forecasts. Test scenarios are synthetic and not executed LLM conversations.

Create `scripts/test_research_bundle.py` before implementation, then `scripts/validate_research.py`. Tests cover missing artifacts, IDs and foreign keys, source authority, benchmark provenance and units, explicit synthetic status, malformed records, and published arithmetic example checks.

Modify only the existing validator registry, README discovery, and the founder SKILL.md router. Add `docs/ko/research-backed-skills.md`. Do not alter the private experience ledger or the existing release package.

## Tasks

- [x] Record initial status and existing evidence/skill contract.
- [x] Read primary public sources and quarantine conflicting or inaccessible evidence.
- [x] Write and run failing bundle tests before adding data or implementation.
- [x] Create the evidence data and four focused skills with conditional rules and acceptance contracts.
- [x] Implement the offline validator and register new packages without weakening existing checks.
- [x] Run the complete Python tests, bundle validation, repository validation, diff checks, and the existing release suite. Python checks passed; the pre-existing release manifest failure remains.
- [x] Review source-to-rule coverage, links, privacy boundaries, and pre-existing file preservation; record exact results and limits in research/solo-developer-2026-10-15/VERIFICATION.md.

## Review focus

An alert-only budget is not a cap; a provider cap is not universal or instantaneous. A payment notification is not an entitlement. A positive conversion ratio is not causal evidence. Incomplete cohorts are not zero retention. A research-derived rule is not personal experience. Conflicting publication summaries must not become selected benchmark truth.

## Verification boundary

Pressure scenarios are authored acceptance criteria, not independent agent runs. No subagent/model calls are authorized or needed for this local implementation. The existing release suite previously failed on a pre-existing .DS_Store; rerun and report without deleting unrelated files or weakening the suite. Research freshness means inspected public content on 2026-10-15, not a guarantee that every served page is the publisher's newest revision.
