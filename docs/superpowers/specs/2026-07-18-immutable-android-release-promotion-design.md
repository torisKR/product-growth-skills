# Immutable Android Release Promotion for Flutter and Expo — Design

## Objective

Extend `toris-flutter-play-store-release` and add
`toris-expo-play-store-release` so Android application binaries are built once,
stored in a GitHub Release, verified byte for byte, uploaded to Google Play
closed testing, and later promoted to production without rebuilding or
re-uploading the AAB.

The canonical implementation remains in:

```text
/Users/toris/projects/product-growth-skills
```

This repository contains reusable skills and templates, not a deployable Flutter
or Expo application. Implementation must not run a real EAS build, create a real
GitHub Release, change repository settings, upload to Google Play, or mutate any
application repository. Verification uses fixtures, static checks, and mocked
provider boundaries.

All repository and skill documentation is English. Agent-facing progress and
handoff messages may use the user's language.

## Approved release policy

Closed testing and production must refer to the same AAB bytes.

- Build a release AAB exactly once.
- Publish it in a GitHub Release before any Play deployment.
- Upload that archived AAB to the Google Play `alpha` track.
- Promote the existing Play `versionCode` from `alpha` to `production`.
- Never rebuild for production.
- Never upload the AAB a second time for production.
- Never select an artifact through `latest`, an unpinned workflow artifact, or a
  mutable filesystem path.

Production promotion is a distinct, manually dispatched operation protected by
the `play-store-production` GitHub Environment. It requires the release tag, the
expected full commit SHA, the independently reviewed AAB SHA-256, and the exact
confirmation value `promote-production`.

## Alternatives considered

### Selected: GitHub Actions orchestration with framework-specific builders

GitHub Actions owns tag verification, GitHub Release publication, integrity
verification, Environment approvals, and Google Play deployment. Flutter builds
on the GitHub runner. Expo builds on EAS Build, after which GitHub Actions
downloads the exact EAS build by ID.

This provides one security and promotion model for both frameworks, keeps the
GitHub Release as the deployment source of truth, and requires no release
toolchain on the user's computer.

### Rejected: one build-and-production workflow

A single workflow is shorter, but it couples signing, release-write, and Play
production credentials. It also weakens the human review boundary and makes it
easy to rebuild during a production retry.

### Rejected: native EAS Workflows for the Expo package

EAS Workflows can build, submit, download builds, and request approval, but its
current schema has no GitHub Release job. It would require a separately managed
GitHub credential, consume EAS custom-workflow minutes, and would submit by EAS
build ID rather than by a GitHub-Release asset independently verified in the
deployment workflow.

## Shared architecture

Each framework package installs two generated GitHub workflows into an
application repository:

```text
release-android-archive.yml
release-android-deploy.yml
```

The archive workflow builds and publishes. The deployment workflow downloads
and verifies, then either uploads to `alpha` or promotes from `alpha` to
`production`.

```text
verified tag + commit
        |
        v
framework build exactly once
        |
        v
AAB + checksum + manifest
        |
        v
draft GitHub Release -> verify assets -> publish immutable Release
        |
        +------------------------------+
        |                              |
        v                              v
download and verify              download and verify
upload AAB to alpha              verify alpha versionCode
                                       |
                                       v
                              protected Environment approval
                                       |
                                       v
                              promote alpha -> production
```

GitHub Actions artifacts may be used only as short-lived transport between jobs
in one workflow run. They are never a production deployment source.

## GitHub Release contract

### Source identity

The archive workflow accepts an exact release tag. The tag must already exist
and resolve to the full commit checked out for the build. The workflow refuses
branch names, moving aliases, source code from pull requests, and tag/commit
mismatches.

The application repository must enable GitHub immutable releases before this
pipeline is used. The archive workflow checks the repository policy before
building. It creates a draft release, uploads and reconciles every asset, then
publishes the release. The deployment workflow requires the release to be
published, non-draft, and immutable.

The repository should protect the selected Android release tag namespace with a
ruleset that restricts creation, update, and deletion. The skill documents this
external setup but does not change repository settings.

### Deterministic assets

Every successful build produces exactly these required assets:

```text
<package>-<versionName>-<versionCode>.aab
<package>-<versionName>-<versionCode>.aab.sha256
android-release-manifest.json
```

Flutter may additionally upload mapping and native-debug-symbol archives when
the project generates them. Expo may additionally upload JavaScript source maps
when the project explicitly produces them. Optional diagnostics never replace
the three required assets.

The checksum file uses the standard two-space `sha256sum` format and refers only
to the AAB basename. Asset names must use a strict ASCII allowlist and must not
contain path separators.

### Manifest schema

`android-release-manifest.json` is schema version `1` and contains:

- framework: `flutter` or `expo`;
- repository and full source commit SHA;
- release tag and workflow run ID/attempt;
- package name, version name, and integer version code;
- AAB basename, media type, byte size, and lowercase SHA-256;
- build provider and provider build ID where applicable;
- framework/CLI version and selected build profile, flavor, and entrypoint;
- Android upload-certificate SHA-256 fingerprint when it can be resolved;
- UTC creation timestamp.

The manifest is data, not authority. Track selection, production approval, the
expected SHA, and the expected commit come from protected workflow inputs and
GitHub Environment policy, never from the manifest.

### Publication and retry behavior

Asset upload has no assumed idempotency. Before an upload or retry, the workflow
lists all assets and reconciles exact name, `uploaded` state, byte size, and the
GitHub API `sha256:` digest.

- An exact match is a successful no-op.
- A same-name asset with a different digest fails closed.
- A documented empty `starter` asset left by an upstream failure may be removed
  only while the release is still a draft.
- Published assets are never deleted, replaced, or uploaded with `--clobber`.
- The manifest is uploaded last and serves as the draft-completion marker.

Immediately before publication, all required assets are downloaded into a new
empty directory and verified. Once published, retries may only verify the
immutable release or fail. Changed bytes require a new tag and version code.

## Deployment verification

The deployment workflow is manual and runs only from the protected default
branch. It accepts:

```text
release_tag
expected_commit_sha
expected_artifact_sha256
target             # alpha or production
confirm_production # must equal promote-production for production
```

Before a Play credential becomes usable, a non-secret preflight job validates
input syntax and routes the job to either `play-store-nonproduction` or
`play-store-production`. The secret-bearing job then:

1. Retrieves the published release by exact tag, never `latest`.
2. Requires the release to be immutable.
3. Resolves the tag and compares it with the workflow input and manifest SHA.
4. Locates required assets by exact name and asset ID.
5. Downloads them into a new empty runner-temporary directory.
6. Verifies GitHub release integrity when the installed GitHub CLI supports it.
7. Compares API digest, checksum-file digest, manifest digest, expected digest,
   and locally computed digest.
8. Verifies size, package name, version name/code, and certificate fingerprint.
9. Confirms the AAB is a nonempty valid ZIP and contains an Android bundle
   manifest before any Play API call.

Any mismatch fails before network deployment. An unknown provider outcome is
reconciled against Google Play and retried only with the already archived bytes.

## Flutter adapter

`toris-flutter-play-store-release` retains its public name and the stable
project-internal namespace `tool/flutter-play-store-release`.

The package adds explicit archive and archived-deployment Fastlane paths instead
of silently changing the existing lanes:

- `archive_aab` calls the existing fresh-artifact build primitive exactly once,
  computes the release metadata, and writes the manifest inputs. It performs no
  Play upload.
- `deploy_archived_play_store` accepts only a downloaded, verified AAB. For
  `alpha`, it uploads that path once. For `production`, it performs a Play track
  promotion for the recorded version code and does not supply an AAB.

The archived deployment path must make zero Flutter build, dependency-prepare,
signing-secret, or signing-file calls.

The archive path uses the positive Android build number committed in
`pubspec.yaml` or supplied as an explicit build input and embedded in the AAB.
It does not allocate `max + 1` immediately before upload because delayed
deployment would make that allocation unsafe. The deploy path queries active
tracks and rejects a code that cannot be uploaded or promoted without rebuilding.

The generated archive workflow receives signing credentials but no Play
credential. The generated deployment workflow receives the Play service account
but no keystore or signing credential.

Existing direct local lanes remain available for backward compatibility, but
the generated CI/CD path and documentation use archive-first delivery. Managed
legacy workflow files are migrated transactionally; customized files continue
to produce a conflict instead of being overwritten.

## Expo adapter

Add the standalone skill package `toris-expo-play-store-release` using the
system skill initializer. It is CI/CD-first and must not install Expo, EAS CLI,
Android SDK, Java, Ruby, or Fastlane globally on the user's computer.

The generated archive workflow:

1. Pins Node and invokes an exact EAS CLI version with `npx`.
2. Validates the EAS project and Android package.
3. Runs one non-interactive EAS Android store build with `--wait --json`.
4. Extracts one exact EAS build ID and rejects missing, duplicate, or incomplete
   build results.
5. Downloads that build by ID, never through `--latest`.
6. Requires exactly one nonempty `.aab` and records EAS build/project identity in
   the shared manifest.
7. Publishes the same immutable GitHub Release contract as the Flutter adapter.

`eas.json` uses remote app-version management, a store-distribution Android
profile, an explicit `app-bundle` build type, and automatic version-code
incrementing. The version code recorded by the completed EAS build is
authoritative for the manifest.

Google Play delivery uses a Bundler-pinned Fastlane installation inside GitHub
Actions, not a global installation. The `alpha` path uploads the verified AAB.
The production path promotes the existing alpha version code without providing
an AAB. EAS Submit is intentionally not the production-promotion mechanism
because its public CLI exposes artifact submission, not an explicit existing
track-version promotion operation.

EAS stores Android build-signing credentials. Google Play service-account JSON
is stored only as a GitHub Environment secret for the deployment workflow. The
archive job receives `EXPO_TOKEN` and release-write permission but no Google Play
credential. The deployment job receives the Play credential and release-read
permission but no EAS token.

The skill documents that Google requires the first application binary to be
uploaded through Play Console before API-based publishing works. That one-time
external bootstrap cannot be automated by this repository.

The Expo skill remains in the canonical GitHub repository and does not install a
new global local toolchain or skill copy as part of this change. The existing
Flutter skill's two previously requested global copies are updated only after
the canonical package passes all tests.

## Permissions and secrets

Workflows use job-level least privilege and pin third-party actions to full
commit SHAs.

- Build: `contents: read`; framework signing/build credential only.
- Attestation when enabled: `contents: read`, `id-token: write`, and
  `attestations: write`.
- Release publication: `contents: write`; no Play credential.
- Deployment: `contents: read` and `attestations: read`; Play credential only
  after Environment approval.

Same-repository release operations use `GITHUB_TOKEN`, not a PAT. Pull request,
fork, and `pull_request_target` events cannot invoke release workflows. Checkout
uses `persist-credentials: false`.

Production requires all of the following:

- `target=production`;
- `confirm_production=promote-production`;
- a protected `play-store-production` Environment with required reviewers,
  prevented self-review, restricted deployment branches, and disabled admin
  bypass where available;
- exact release-tag, commit, and artifact-hash verification;
- confirmation that the manifest version code exists on `alpha`.

The skills generate setup guidance for GitHub Secrets and Environments but never
create or rotate credentials or repository policy.

## Concurrency and failure semantics

Archive concurrency is keyed by repository and release tag. Deployment
concurrency is keyed by Android package and target, with cancellation disabled.
Version-code validation remains authoritative because workflow queue order is
not an allocator.

Failures before release publication leave a draft that a same-input retry may
reconcile. Failures after publication never mutate the release. Alpha upload and
production promotion write non-secret summaries and preserve the release tag,
commit, version code, and digest needed for reconciliation.

Notification failure cannot mask the deployment result. Logs, summaries,
manifests, and test fixtures never include decoded keystores, service-account
JSON, EAS tokens, passwords, or secret paths.

## Skill package contents

The Flutter package extends its existing templates, bootstrap, validator,
Fastlane helper, tests, references, installation manifest, and English README.
Its atomic dual-global installer remains unchanged except for the new runtime
files included in the package manifest.

The Expo package contains:

```text
toris-expo-play-store-release/
├── SKILL.md
├── README.md
├── agents/openai.yaml
├── scripts/
│   ├── inspect_expo_project.sh
│   ├── bootstrap_android_release_ci.sh
│   └── validate_release_setup.sh
├── templates/
│   ├── eas.json
│   ├── Gemfile
│   ├── Gemfile.lock
│   ├── Fastfile
│   ├── release-android-archive.yml
│   ├── release-android-deploy.yml
│   └── PLAY_STORE_RELEASE.md
├── references/
│   ├── credentials-and-environments.md
│   ├── immutable-release-contract.md
│   ├── first-release-checklist.md
│   └── troubleshooting.md
└── tests/
    └── run_tests.sh
```

The Expo bootstrap supports dry-run, stages all proposed edits, refuses to
overwrite unowned or customized files, and is idempotent. It may merge a missing
profile into a compatible `eas.json`; ambiguous or conflicting JSON fails with
no project changes.

Root `README.md` and `scripts/validate_skills.py` are updated for eight skills.
The validator treats both release packages as standalone executable skills,
checks their required runtime files, rejects unsafe secret examples, and runs
their package-specific tests.

## Testing strategy

Implementation follows red-green-refactor. No test performs a real build,
release publication, EAS request, Play request, secret mutation, or notification.

Shared fixture coverage proves:

- zero, empty, multiple, stale, or symlinked AAB candidates fail;
- checksum, size, tag, commit, repository, package, version, certificate, asset
  name, API digest, or manifest mismatch fails before a provider call;
- exact asset reconciliation is idempotent and a conflicting asset never gets
  overwritten;
- a published mutable release is rejected;
- `latest`, `--clobber`, production AAB upload, and rebuild-on-promotion commands
  do not appear in generated workflows;
- alpha uses the downloaded GitHub Release asset exactly once;
- production performs one track promotion and zero AAB uploads;
- production requires both exact confirmation and the protected Environment;
- archive jobs cannot read Play secrets and deploy jobs cannot read signing/EAS
  build secrets;
- generated actions are pinned, permissions are minimal, and checkout does not
  persist credentials;
- bootstrap dry-run, idempotency, conflict handling, rollback, ownership, and
  validator behavior remain deterministic.

Flutter regression tests continue to cover all existing modes and the atomic
global installation lifecycle. Expo tests cover project inspection, compatible
and conflicting `eas.json`, managed workflow generation, EAS build-ID parsing,
exact AAB selection, manifest validation, and no-local-global-install behavior.

Verification includes package tests, the root skill validator, shell syntax,
Ruby syntax/tests, YAML parsing, JSON parsing, skill quick-validation, secret
scanning, documentation-link checks, clean-tree inspection, and comparison of
the two installed Flutter copies with the canonical install manifest.

## Documentation and handoff

Each README gives copy-paste setup commands, required repository policies,
Secrets and Environment tables, first-release limitations, alpha deployment,
production promotion, retry/reconciliation, rollback-by-new-version guidance,
and troubleshooting.

The final handoff reports exactly what was implemented and tested. It states
that no real application build or external deployment occurred and identifies
the application-side setup still required before the generated workflows can
run.

## Acceptance criteria

The change is complete when:

1. Both skills generate archive-first, same-AAB Android CI/CD workflows.
2. Every production path promotes an existing alpha version code without an AAB
   upload or rebuild.
3. GitHub Release assets are deterministic, immutable, and verified against an
   independently supplied SHA-256 and commit.
4. Permission and secret boundaries are enforced by generated workflow jobs and
   covered by tests.
5. Both package test suites and the root validator pass from a clean checkout.
6. The existing Flutter skill's two global copies exactly match the verified
   canonical manifest.
7. The canonical repository is committed and pushed without unrelated changes.
