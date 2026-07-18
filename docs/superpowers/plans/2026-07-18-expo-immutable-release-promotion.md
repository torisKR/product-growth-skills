# Expo Immutable Release Promotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `toris-expo-play-store-release`, a CI/CD-first skill that builds one signed Android AAB through EAS Build, stores it in an immutable GitHub Release, uploads the archived bytes to Play `alpha`, and promotes the same version code to production.

**Architecture:** GitHub Actions is the trust and approval boundary; EAS is a pinned cloud build provider only. Offline scripts inspect and bootstrap an Expo repository, a pure Python runtime validates EAS build identity and GitHub Release assets, and Bundler-pinned Fastlane performs alpha upload or existing-track promotion.

**Tech Stack:** Bash, Python 3 standard library, Node 24, EAS CLI 21.0.0 through `npx`, EAS Build, Ruby 3.3, Fastlane 2.237.0, Bundler 4.0.16, GitHub Actions, GitHub CLI, Google bundletool 1.18.3, Minitest, and shell fixtures.

## Global Constraints

- The skill and directory name are exactly `toris-expo-play-store-release`.
- Use the system `skill-creator` initializer before hand-authoring the new package.
- Do not install Expo, EAS CLI, Node, Java, Ruby, Fastlane, Android SDK, or this new skill globally on the user's computer.
- Invoke EAS CLI as exact `npx eas-cli@21.0.0`; never use `latest`, `--auto-submit`, or an unpinned global executable.
- Start one EAS Android store build, persist its exact UUID, and download only that build ID.
- Require exactly one regular non-symlinked nonempty `.aab`; reject APKs and ambiguous downloads.
- Upload the archived AAB to `alpha`; production must use Play track promotion with no AAB or APK argument.
- Require a published immutable GitHub Release, exact tag, full source commit SHA, and independently reviewed lowercase SHA-256 before any Play operation.
- Production requires `confirm_production=promote-production` and the protected `play-store-production` Environment.
- Archive jobs receive `EXPO_TOKEN` but no Play credential; deploy jobs receive the Play credential but no EAS token or signing credential.
- Do not run a real EAS request, GitHub Release operation, Google Play call, notification, repository-policy change, or application bootstrap during implementation tests.
- Keep every runtime document in English and `SKILL.md` below 500 lines.

---

### Task 1: Create a failing root contract and initialize the skill package

**Files:**
- Create: `scripts/tests/test_validate_skills.py`
- Modify: `scripts/validate_skills.py`
- Create with initializer: `toris-expo-play-store-release/SKILL.md`
- Create with initializer: `toris-expo-play-store-release/agents/openai.yaml`
- Create with initializer: `toris-expo-play-store-release/scripts/`
- Create with initializer: `toris-expo-play-store-release/references/`
- Create: `toris-expo-play-store-release/tests/run_tests.sh`

**Interfaces:**
- Root constants become `STANDALONE_SKILLS`, `EXECUTABLE_SCRIPTS_BY_SKILL`, and `REQUIRED_RUNTIME_FILES_BY_SKILL`.
- Expo test groups: `package_contract`, `inspection`, `bootstrap`, `eas_build_contract`, `release_contract`, `fastlane`, `workflows`, `validator`, `documentation`, and `repository_integration`.

- [ ] **Step 1: Write the root RED test**

Create a `unittest` file that imports `scripts/validate_skills.py` without running `main` and asserts the new package contract:

```python
self.assertIn("toris-expo-play-store-release", validator.EXPECTED)
self.assertIn("toris-expo-play-store-release", validator.STANDALONE_SKILLS)
self.assertEqual(
    {
        "scripts/inspect_expo_project.sh",
        "scripts/bootstrap_android_release_ci.sh",
        "scripts/validate_release_setup.sh",
        "tests/run_tests.sh",
    },
    validator.EXECUTABLE_SCRIPTS_BY_SKILL["toris-expo-play-store-release"],
)
```

- [ ] **Step 2: Run the root test and verify RED**

```bash
python3 -m unittest scripts/tests/test_validate_skills.py -v
```

Expected: FAIL because the plural standalone constants and Expo package are missing.

- [ ] **Step 3: Run the required official initializer**

```bash
python3 /Users/toris/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  toris-expo-play-store-release \
  --path /Users/toris/projects/product-growth-skills \
  --resources scripts,references \
  --interface display_name="Toris Expo Play Store Release" \
  --interface short_description="Archive and promote Expo Android releases" \
  --interface default_prompt="Use \$toris-expo-play-store-release to inspect this Expo app, configure immutable Android release CI, and verify same-AAB Play Store promotion."
```

Remove every initializer placeholder before committing. Preserve only `name` and `description` in SKILL frontmatter.

- [ ] **Step 4: Generalize static root package validation minimally**

Add the new skill to `EXPECTED`. Parameterize diagnostics by the current package name. Flutter keeps its install-manifest and lifecycle entrypoint contract; Expo receives its own required runtime-file and executable set without `.skill-package-id`, installer, update, uninstall, or global receipt requirements.

Do not make the root validator execute package test suites in this task; that integration occurs after both packages are complete and recursion has been removed.

- [ ] **Step 5: Create the test runner contract and verify GREEN**

Create an executable `tests/run_tests.sh` that accepts one group name or defaults to all groups, creates fixtures under `mktemp -d`, traps cleanup, and fails on unknown group names. Initially, only `package_contract` runs and checks the initialized metadata; the remaining named groups must be recognized and report an explicit not-yet-implemented failure until their tasks land.

Run:

```bash
python3 -m unittest scripts/tests/test_validate_skills.py -v
bash toris-expo-play-store-release/tests/run_tests.sh package_contract
```

Expected: both PASS.

- [ ] **Step 6: Commit the initialized contract**

```bash
git add scripts/tests/test_validate_skills.py scripts/validate_skills.py \
  toris-expo-play-store-release
git commit -m "feat(expo-release): initialize standalone CI skill"
```

### Task 2: Implement offline Expo project inspection

**Files:**
- Create: `toris-expo-play-store-release/scripts/inspect_expo_project.sh`
- Modify: `toris-expo-play-store-release/tests/run_tests.sh`

**Interfaces:**
- `inspect_expo_project.sh --project PATH [--profile NAME] [--format human|json]`.
- Exit `0`: deterministic complete inspection; exit `1`: unresolved/conflicting required identity; exit `2`: bad arguments or unsafe root.
- JSON schema version `1`, exactly one line.

- [ ] **Step 1: Add RED inspection fixtures**

Generate fixtures for `app.json`, static `app.config.json`, ambiguous `app.config.js`, malformed JSON, missing package, missing EAS project ID, monorepo path with spaces, symlinked project root, compatible `eas.json`, conflicting `appVersionSource`, inherited profile, and missing profile.

Assert the JSON keys exactly equal:

```text
schema_version project_root package_manager expo_sdk_version eas_project_id
android_package version config_source config_ownership profile
app_version_source distribution build_type auto_increment warnings failures
```

Install fake `node`, `npm`, `npx`, `eas`, and `expo` canaries that fail the test if executed; inspection must remain static.

- [ ] **Step 2: Run and verify RED**

```bash
bash toris-expo-play-store-release/tests/run_tests.sh inspection
```

Expected: FAIL because the inspector does not exist.

- [ ] **Step 3: Implement argument and path safety**

Use shell only for option parsing and invoke embedded Python for JSON/config inspection. Resolve the physical project root, refuse symlinks, require `package.json`, and read only regular files within the root. Recognize npm, pnpm, Yarn, and Bun from committed lockfiles; more than one lockfile is a warning and deterministic precedence is `pnpm`, `yarn`, `npm`, `bun`.

- [ ] **Step 4: Implement static Expo/EAS resolution**

Read static JSON sources without executing JavaScript or TypeScript config. Resolve `expo.extra.eas.projectId`, `expo.android.package`, version, Expo dependency, `cli.appVersionSource`, and the selected build profile. Report dynamic config as unresolved rather than executing it.

Require the selected profile to resolve directly to `distribution=store`, `android.buildType=app-bundle`, and `autoIncrement=true`; reject inheritance because static merging is ambiguous.

- [ ] **Step 5: Run GREEN**

```bash
bash toris-expo-play-store-release/tests/run_tests.sh inspection
bash -n toris-expo-play-store-release/scripts/inspect_expo_project.sh
```

Expected: inspection PASS and shell syntax exits zero.

- [ ] **Step 6: Commit inspection**

```bash
git add toris-expo-play-store-release/scripts/inspect_expo_project.sh \
  toris-expo-play-store-release/tests/run_tests.sh
git commit -m "feat(expo-release): inspect EAS Android release configuration"
```

### Task 3: Implement transactional Expo CI bootstrap

**Files:**
- Create: `toris-expo-play-store-release/scripts/bootstrap_android_release_ci.sh`
- Create: `toris-expo-play-store-release/templates/eas.json`
- Create: `toris-expo-play-store-release/templates/Gemfile`
- Create: `toris-expo-play-store-release/templates/Gemfile.lock`
- Create: `toris-expo-play-store-release/templates/PLAY_STORE_RELEASE.md`
- Modify: `toris-expo-play-store-release/tests/run_tests.sh`

**Interfaces:**
- `bootstrap_android_release_ci.sh --project PATH [--profile NAME] [--dry-run]`.
- Default profile: `play-store`.
- Managed sidecar: `tool/expo-play-store-release/managed-files.sha256`, schema `1`, package ID `toris-expo-play-store-release`.
- This task proves the transaction engine and installs the base templates available at this point. Task 5 adds the completed Fastfile, workflow templates, and release helper to the final managed inventory and reruns the full bootstrap matrix.

- [ ] **Step 1: Add RED bootstrap tests**

Test dry-run, fresh install, compatible `eas.json` merge, unrelated JSON-key preservation, malformed JSON, profile inheritance, conflicting app-version source/distribution/build type/auto-increment, unowned target, edited managed target, target symlink, second-run byte identity, permissions, and injected failure after every publish operation.

For every conflict and injected failure, compare the entire application tree to a pre-run copy with `diff -r`.

- [ ] **Step 2: Run and verify RED**

```bash
bash toris-expo-play-store-release/tests/run_tests.sh bootstrap
```

Expected: FAIL because the bootstrap and templates are incomplete.

- [ ] **Step 3: Implement exact EAS JSON merge**

The template must equal:

```json
{
  "cli": {
    "appVersionSource": "remote"
  },
  "build": {
    "play-store": {
      "distribution": "store",
      "autoIncrement": true,
      "android": {
        "buildType": "app-bundle"
      }
    }
  }
}
```

Embedded Python may add these missing keys to compatible JSON while preserving all unrelated keys and formatting the result with two-space indentation plus a final newline. It must refuse conflicting existing values or an `extends` key on the selected profile.

- [ ] **Step 4: Implement staged ownership and rollback**

Build all candidate files in a mode-`0700` temporary directory. Validate JSON, Ruby, YAML candidates, and exact managed target names before the first project write. Snapshot existing regular files and parent identities. Publish with same-directory temporary files and `os.replace`; on any failure or signal restore all prior bytes/modes and remove only directories created by this invocation.

The bootstrap must never invoke a package manager, EAS, Expo, Ruby installer, Java, Gradle, or Android SDK.

- [ ] **Step 5: Pin the Ruby delivery dependencies**

Copy the verified Fastlane/Bundler pins used by the Flutter skill: Fastlane `2.237.0` and Bundler `4.0.16`. The Expo Gemfile contains only the source declaration and exact Fastlane gem; it does not include Firebase plugins.

- [ ] **Step 6: Run GREEN**

```bash
bash toris-expo-play-store-release/tests/run_tests.sh bootstrap
bash -n toris-expo-play-store-release/scripts/bootstrap_android_release_ci.sh
python3 -m json.tool toris-expo-play-store-release/templates/eas.json >/dev/null
```

Expected: all commands exit zero.

- [ ] **Step 7: Commit bootstrap**

```bash
git add toris-expo-play-store-release/scripts/bootstrap_android_release_ci.sh \
  toris-expo-play-store-release/templates \
  toris-expo-play-store-release/tests/run_tests.sh
git commit -m "feat(expo-release): bootstrap archive-first Android CI"
```

### Task 4: Implement EAS build identity and Google Play delivery adapters

**Files:**
- Create: `toris-expo-play-store-release/scripts/expo_release_contract.py`
- Create: `toris-expo-play-store-release/tests/expo_release_contract_test.py`
- Create: `toris-expo-play-store-release/templates/Fastfile`
- Create: `toris-expo-play-store-release/tests/fastlane_test.rb`
- Modify: `toris-expo-play-store-release/tests/run_tests.sh`

**Interfaces:**
- `expo_release_contract.py select-build --input JSON --expected-commit SHA --output JSON`.
- `expo_release_contract.py select-aab --directory PATH --output JSON`.
- `expo_release_contract.py create-manifest --build JSON --artifact PATH --repository OWNER/REPO --tag TAG --output JSON`.
- `expo_release_contract.py verify --manifest JSON --artifact PATH --expected-commit SHA --expected-sha256 SHA`.
- Fastlane lanes: `android upload_archived_alpha` and `android promote_archived_production`.

- [ ] **Step 1: Write RED EAS build-contract tests**

Cover invalid JSON, non-array JSON, zero/two builds, non-UUID ID, wrong platform/profile/status/commit, missing artifact URL, and exact one-complete-build success. Cover zero/empty/multiple/symlinked AABs and APK-only downloads.

The successful build fixture must include one Android build with a UUID, status `FINISHED`, the expected Git commit, package, version, version code, EAS project ID, and artifact URL. Assert output never selects by timestamp or list order.

- [ ] **Step 2: Write RED manifest integrity tests**

Assert schema-1 typed fields, lowercase digest, size, deterministic basename, source repository/tag/commit, EAS build/project ID, `eas-cli@21.0.0`, profile, and UTC timestamp. Reject traversal names, mismatched size/digest/commit/package/version/code, symlinked input, and non-ZIP artifacts.

- [ ] **Step 3: Write RED Fastlane tests**

Use a fake action adapter and environment. Alpha must call `upload_to_play_store` once with `VERIFIED_AAB_PATH` and track `alpha`. Production must query alpha and require its normalized active-code set to equal exactly `[VERIFIED_VERSION_CODE]`, then call:

```ruby
upload_to_play_store(
  json_key: play_json_path,
  package_name: package_name,
  track: "alpha",
  track_promote_to: "production",
  version_code: version_code,
  track_promote_release_status: "completed",
  skip_upload_aab: true,
  skip_upload_apk: true,
  skip_upload_metadata: true,
  skip_upload_changelogs: true,
  skip_upload_images: true,
  skip_upload_screenshots: true
)
```

Assert empty, different, and multi-code alpha tracks fail before promotion. Assert no build, signing, EAS, Node, or package-manager call occurs in either lane.

- [ ] **Step 4: Run and verify RED**

```bash
python3 -m unittest toris-expo-play-store-release/tests/expo_release_contract_test.py -v
ruby toris-expo-play-store-release/tests/fastlane_test.rb
```

Expected: both fail because the runtime and Fastfile do not exist.

- [ ] **Step 5: Implement the Python contract**

Use only the standard library. Require one build object, exact UUID syntax, `FINISHED`, platform `ANDROID`, matching source commit, and store profile. Require one regular AAB in a new directory. Generate and verify the shared schema from the approved design, with `framework="expo"` and `build_provider="eas"`.

Write JSON atomically through a same-directory mode-`0600` temporary file followed by `os.replace`.

- [ ] **Step 6: Implement the Fastlane lanes**

Decode or accept the Google service-account JSON only under runner-temporary storage, validate its shape without logging values, and clean generated files in `ensure`. Require `PLAY_DEPLOY_TARGET` to be `alpha` or `production`; require `CONFIRM_PRODUCTION_DEPLOY=promote-production` for production. Use the exact provider calls tested above.

- [ ] **Step 7: Run GREEN**

```bash
python3 -m unittest toris-expo-play-store-release/tests/expo_release_contract_test.py -v
ruby toris-expo-play-store-release/tests/fastlane_test.rb
ruby -c toris-expo-play-store-release/templates/Fastfile
```

Expected: tests PASS and syntax prints `Syntax OK`.

- [ ] **Step 8: Commit adapters**

```bash
git add toris-expo-play-store-release/scripts/expo_release_contract.py \
  toris-expo-play-store-release/templates/Fastfile \
  toris-expo-play-store-release/tests
git commit -m "feat(expo-release): pin EAS build identity and Play promotion"
```

### Task 5: Generate Expo archive and deployment workflows

**Files:**
- Create: `toris-expo-play-store-release/scripts/github_release_archive.py`
- Create: `toris-expo-play-store-release/templates/release-android-archive.yml`
- Create: `toris-expo-play-store-release/templates/release-android-deploy.yml`
- Create: `toris-expo-play-store-release/tests/github_release_archive_test.py`
- Create: `toris-expo-play-store-release/tests/workflow_contract_test.rb`
- Modify: `toris-expo-play-store-release/scripts/bootstrap_android_release_ci.sh`
- Modify: `toris-expo-play-store-release/tests/run_tests.sh`

**Interfaces:**
- Archive dispatch inputs: exact `release_tag` and optional exact profile defaulting to `play-store`.
- Deploy dispatch inputs: `release_tag`, `expected_commit_sha`, `expected_artifact_sha256`, `target`, and `confirm_production`.
- GitHub Release helper has the same `publish` and `download` CLI contract as the Flutter package.

- [ ] **Step 1: Refresh official EAS workflow references before generation**

Fetch and inspect all three current official resources:

```bash
node /Users/toris/.codex/plugins/cache/claude-plugins-official/expo/1.8.2/skills/eas-workflows/scripts/fetch.js \
  https://api.expo.dev/v2/workflows/schema
node /Users/toris/.codex/plugins/cache/claude-plugins-official/expo/1.8.2/skills/eas-workflows/scripts/fetch.js \
  https://raw.githubusercontent.com/expo/expo/main/docs/pages/eas/workflows/syntax.mdx
node /Users/toris/.codex/plugins/cache/claude-plugins-official/expo/1.8.2/skills/eas-workflows/scripts/fetch.js \
  https://raw.githubusercontent.com/expo/expo/main/docs/pages/eas/workflows/pre-packaged-jobs.mdx
```

Do not add a native `.eas/workflows` file; record in the package docs that GitHub Actions was selected because the live EAS schema has no GitHub Release publication job.

- [ ] **Step 2: Write RED workflow and fake-provider tests**

Assert full action SHAs, `persist-credentials: false`, exact permissions, no PR trigger, tag-keyed concurrency, and secret separation. Extract EAS command blocks and run them against fake `npx` output for invalid JSON, zero/two builds, unknown outcome, incomplete build, wrong commit, one exact successful build, failed exact-ID recheck, zero/two AAB downloads, and symlinked AAB.

Assert these exact command fragments exist:

```text
npx eas-cli@21.0.0 build --platform android --profile
npx eas-cli@21.0.0 build:view
npx eas-cli@21.0.0 build:download --build-id
```

Assert `--latest`, `--auto-submit`, `eas submit`, global npm installation, and production AAB upload are absent.

- [ ] **Step 3: Run and verify RED**

```bash
ruby toris-expo-play-store-release/tests/workflow_contract_test.rb
```

Expected: FAIL because workflow templates are missing.

- [ ] **Step 4: Add the self-contained GitHub Release helper**

Copy the reviewed Flutter helper, replace only package-specific diagnostics, and run the same fixture suite against the Expo copy. Keep the CLI, manifest schema, immutable-release checks, asset reconciliation, and exact-ID download behavior byte-for-byte compatible where possible.

- [ ] **Step 5: Implement the archive workflow**

Use a non-secret tag preflight, an EAS build job with `contents: read` and `EXPO_TOKEN`, and a separate publisher with `contents: write` and no EAS or Play secret. Pin Node 24 and invoke `npx eas-cli@21.0.0`.

Capture build JSON to a mode-`0600` runner-temporary file, select the one build ID, re-fetch that exact ID, download it into a new directory, require one AAB, and create schema-1 metadata. Transfer only the AAB and non-secret metadata to the publisher; publish the immutable Release through the helper.

If EAS returns an unknown request outcome before a build ID is persisted, fail with explicit reconciliation guidance and never start another build automatically. Support an explicit resume build ID input only when it is a valid UUID and its fetched commit/profile matches.

- [ ] **Step 6: Implement the deployment workflow**

Use the exact five dispatch inputs and no-secret routing to `play-store-nonproduction` or `play-store-production`. Download the immutable release by exact asset IDs, verify the five-way digest agreement and embedded AAB metadata with checksum-pinned bundletool `1.18.3`, then invoke `upload_archived_alpha` with the downloaded path or `promote_archived_production` without a path.

- [ ] **Step 7: Run GREEN and YAML parsing**

```bash
ruby toris-expo-play-store-release/tests/workflow_contract_test.rb
ruby -e 'require "yaml"; ARGV.each { |p| YAML.safe_load(File.read(p), aliases: false) }' \
  toris-expo-play-store-release/templates/release-android-archive.yml \
  toris-expo-play-store-release/templates/release-android-deploy.yml
```

Expected: tests PASS and YAML parsing exits zero.

Extend the bootstrap managed inventory with `fastlane/Fastfile`, both workflow templates, `tool/expo-play-store-release/github_release_archive.py`, and the final guide. Rerun fresh install, compatible merge, dry-run, idempotency, conflict, and rollback groups so the final generated-project contract is exercised with every template present.

- [ ] **Step 8: Commit workflows**

```bash
git add toris-expo-play-store-release/scripts/github_release_archive.py \
  toris-expo-play-store-release/scripts/bootstrap_android_release_ci.sh \
  toris-expo-play-store-release/templates/release-android-archive.yml \
  toris-expo-play-store-release/templates/release-android-deploy.yml \
  toris-expo-play-store-release/tests
git commit -m "feat(expo-release): archive EAS builds in GitHub Releases"
```

### Task 6: Complete validation, skill instructions, and documentation

**Files:**
- Create: `toris-expo-play-store-release/scripts/validate_release_setup.sh`
- Create: `toris-expo-play-store-release/README.md`
- Modify: `toris-expo-play-store-release/SKILL.md`
- Modify: `toris-expo-play-store-release/agents/openai.yaml`
- Create: `toris-expo-play-store-release/references/credentials-and-environments.md`
- Create: `toris-expo-play-store-release/references/immutable-release-contract.md`
- Create: `toris-expo-play-store-release/references/first-release-checklist.md`
- Create: `toris-expo-play-store-release/references/troubleshooting.md`
- Modify: `toris-expo-play-store-release/templates/PLAY_STORE_RELEASE.md`
- Modify: `toris-expo-play-store-release/tests/run_tests.sh`

**Interfaces:**
- `validate_release_setup.sh [--project PATH] [--profile NAME] [--context doctor|archive|deploy] [--format human|json] [--run-project-commands]`.
- Default behavior is offline/read-only and never installs, builds, submits, promotes, or mutates.

- [ ] **Step 1: Add RED validator tests**

Cover missing tools as warnings in doctor context, missing `EXPO_TOKEN` as an archive-context failure by presence only, missing Play JSON as a deploy-context failure by presence only, invalid managed sidecar, malformed workflow, mutable action pin, wrong EAS profile, wrong package/project ID, and explicit project-command mode with fake pinned commands.

Assert human output uses only `PASS`, `WARN`, and `FAIL`; JSON output is one line and contains no environment values or secret paths.

- [ ] **Step 2: Add RED documentation/package tests**

Require English-only runtime docs, no unfinished markers, working local links, SKILL frontmatter containing only name/description, Quick start, execution-policy link, Definition of done, correct default prompt, no installer/update/uninstall files, and no global-install command.

- [ ] **Step 3: Run and verify RED**

```bash
bash toris-expo-play-store-release/tests/run_tests.sh validator
bash toris-expo-play-store-release/tests/run_tests.sh documentation
```

Expected: both FAIL because validator and final docs are incomplete.

- [ ] **Step 4: Implement offline validation**

Reuse inspector output, validate managed files and workflow structure, and check executable availability without executing it. Only `--run-project-commands` may invoke `npx eas-cli@21.0.0 config --platform android --profile PROFILE --json --non-interactive` and `npx expo-doctor`; it must reject any requested build, submit, workflow, credentials, install, or promotion command.

- [ ] **Step 5: Write final English skill materials**

Make `SKILL.md` imperative and route detail to references. Include setup, doctor, archive CI, alpha deployment, production promotion, and repair modes. State that actual deploys, credentials, environments, immutable-release settings, tag rulesets, first Play binary, and paid account actions require explicit authorization.

Document `EXPO_TOKEN`, the Play service-account Environment secret, immutable releases, protected tags, both GitHub Environments, first manual Play upload, alpha verification, production promotion, exact hash review, retries, EAS unknown outcomes, and rollback by a new version. State explicitly that the package installs no global local toolchain and receives no global skill copy in this change.

- [ ] **Step 6: Run the complete Expo suite and quick validator**

```bash
bash toris-expo-play-store-release/tests/run_tests.sh
UV_CACHE_DIR=/tmp/product-growth-skills-uv uv run --with pyyaml \
  python /Users/toris/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  toris-expo-play-store-release
find toris-expo-play-store-release -type f -name '*.sh' -exec bash -n {} \;
```

Expected: every package group PASS, quick validation reports success, and shell syntax exits zero.

- [ ] **Step 7: Commit the complete Expo skill**

```bash
git add toris-expo-play-store-release
git commit -m "docs(expo-release): document immutable Play promotion"
```
