# Flutter Immutable Release Promotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `toris-flutter-play-store-release` so CI builds one Flutter AAB, publishes it to an immutable GitHub Release, uploads the archived bytes to Play `alpha`, and later promotes the same version code to production without rebuilding or uploading another AAB.

**Architecture:** Preserve the existing direct-release lanes for compatibility, but generate an archive-first CI/CD path with separate archive and deploy workflows. Add a pure archived-artifact contract around the existing one-build primitive, add an upload-versus-promotion Fastlane coordinator, and migrate the old managed workflow transactionally.

**Tech Stack:** Bash 3-compatible shell, Ruby 3.3, Fastlane 2.237.0, Python 3 standard library, GitHub Actions, GitHub CLI, Google bundletool 1.18.3, Minitest, and the repository's existing shell fixture harness.

## Global Constraints

- The public skill name remains `toris-flutter-play-store-release`.
- The generated project namespace remains `tool/flutter-play-store-release` and the generated ownership package ID remains `flutter-play-store-release`.
- Build a release AAB exactly once and never rebuild for production.
- Upload the archived AAB to `alpha`; production must use `track_promote_to: "production"` with no `aab` or `apk` argument.
- Require a published immutable GitHub Release, exact tag, full source commit SHA, and independently reviewed lowercase SHA-256 before any Play operation.
- Production requires `confirm_production=promote-production` and the protected `play-store-production` Environment.
- The archive workflow receives signing credentials but no Play credential; the deploy workflow receives the Play credential but no signing credential.
- Do not run a real Flutter build, GitHub Release operation, Google Play call, notification, repository-policy change, or application bootstrap during implementation tests.
- Do not change, reinstall, or remove either global Flutter skill copy until the canonical full suite passes.
- Keep every runtime document in English and every shell entrypoint compatible with macOS system Bash.

---

### Task 1: Add rollback-safe deletion to project transactions

**Files:**
- Modify: `toris-flutter-play-store-release/tests/run_tests.sh`
- Modify: `toris-flutter-play-store-release/scripts/lib/project_transaction.sh`

**Interfaces:**
- Consumes: existing `fprs_project_transaction_begin`, `register`, `validate`, `commit`, and `abort` functions.
- Produces: `fprs_project_transaction_register_delete RELATIVE_PATH`, using the same validation, race detection, rollback, signal, and error-code contract as file replacement.

- [ ] **Step 1: Write failing deletion lifecycle tests**

Add a `project_transaction_delete` group to `tests/run_tests.sh`. Exercise successful deletion, abort-before-commit, injected failure after quarantine, signal interruption, target replacement after validation, symlink refusal, duplicate registration, and delete/register collision. The central success assertion must be equivalent to:

```bash
fprs_project_transaction_begin "$delete_root"
fprs_project_transaction_register_delete 'managed/legacy.yml'
fprs_project_transaction_validate
fprs_project_transaction_commit
[ ! -e "$delete_root/managed/legacy.yml" ] ||
  fail 'committed deletion retained the legacy file'
```

For every injected failure, save the complete fixture tree before the transaction and require `diff -r` to report byte identity after rollback.

- [ ] **Step 2: Run the focused group and verify RED**

Run:

```bash
bash toris-flutter-play-store-release/tests/run_tests.sh project_transaction_delete
```

Expected: FAIL because `fprs_project_transaction_register_delete` is undefined.

- [ ] **Step 3: Implement delete records**

Extend each transaction record with an `operation` file containing exactly `write` or `delete`. Keep `fprs_project_transaction_register` behavior unchanged and add this public entrypoint:

```bash
fprs_project_transaction_register_delete() {
  [ "$FPRS_PROJECT_TRANSACTION_ACTIVE" -eq 1 ] || return 2
  [ "$#" -eq 1 ] || return 2
  fprs_transaction_target=$(fprs_project_transaction_target_path "$1") || return 2
  [ -f "$fprs_transaction_target" ] && [ ! -L "$fprs_transaction_target" ] || return 2
  # Reject a second record for the same physical target, snapshot identity and
  # mode, and create a record with operation=delete and no candidate body.
}
```

Update record validation, the Python commit worker, rollback, created-directory cleanup, and signal recovery so delete records quarantine an existing regular file and commit by retaining the quarantine until the transaction is committed. A pre-commit failure restores the original name and bytes. A post-commit cleanup failure reports retained quarantine evidence without restoring the deleted file.

- [ ] **Step 4: Run focused and existing transaction groups**

Run:

```bash
bash toris-flutter-play-store-release/tests/run_tests.sh project_transaction_delete
bash toris-flutter-play-store-release/tests/run_tests.sh project_transaction
```

Expected: both groups PASS with no stderr warnings.

- [ ] **Step 5: Commit the transaction primitive**

```bash
git add toris-flutter-play-store-release/scripts/lib/project_transaction.sh \
  toris-flutter-play-store-release/tests/run_tests.sh
git commit -m "feat(flutter-release): support transactional managed-file deletion"
```

### Task 2: Implement the Flutter archive and archived-deployment contract

**Files:**
- Create: `toris-flutter-play-store-release/tests/immutable_release_test.rb`
- Modify: `toris-flutter-play-store-release/templates/FlutterPlayStoreRelease.rb`
- Modify: `toris-flutter-play-store-release/templates/Fastfile`
- Modify: `toris-flutter-play-store-release/tests/run_tests.sh`

**Interfaces:**
- Produces: `FlutterPlayStoreRelease.archive_aab(options:, env:, actions:, project_root:) -> Hash`.
- Produces: `FlutterPlayStoreRelease.deploy_archived_play_store(options:, env:, actions:, project_root:) -> Hash`.
- Produces lanes: `android archive_aab` and `android deploy_archived_play_store`.
- Archive result schema: `schema_version`, `framework`, `artifact_path`, `artifact_sha256`, `artifact_size`, `package_name`, `version_name`, `version_code`, `flavor`, `entrypoint`, `framework_version`, `upload_certificate_sha256`.

- [ ] **Step 1: Write RED tests for archive creation**

Create `immutable_release_test.rb` with a recording action adapter. Its core test must assert one prepare, one Flutter AAB build, no Play query, no Play upload, and exact metadata:

```ruby
result = FlutterPlayStoreRelease.archive_aab(
  options: { version_name: "1.2.3", version_code: 45 },
  env: signing_env,
  actions: actions,
  project_root: project_root
)

assert_equal "flutter", result.fetch("framework")
assert_equal 45, result.fetch("version_code")
assert_match(/\A[0-9a-f]{64}\z/, result.fetch("artifact_sha256"))
assert_equal 1, actions.calls.count { |call| call.first == :flutter_build }
assert_empty actions.calls.select { |call| [:google_play_track_version_codes, :upload_to_play_store].include?(call.first) }
```

Add cases for pubspec build number fallback, explicit bounded version-code override, missing/zero/out-of-range code, wrong package, empty artifact, symlink artifact, and atomically written `ARCHIVE_RESULT_PATH`.

- [ ] **Step 2: Write RED tests for alpha upload and production promotion**

Use one fixture AAB and one verified manifest. Assert alpha supplies the canonical fixture path once. Assert production requires the exact confirmation, requires the alpha track's normalized active-code set to equal only the requested code, supplies no binary key, and promotes once:

```ruby
promotion = actions.calls.fetch(0).last
assert_equal "alpha", promotion.fetch(:track)
assert_equal "production", promotion.fetch(:track_promote_to)
assert_equal 45, promotion.fetch(:version_code)
assert_equal true, promotion.fetch(:skip_upload_aab)
refute promotion.key?(:aab)
refute promotion.key?(:apk)
```

Add tests proving archived deployment performs zero `prepare`, `flutter_build`, `prepare_signing`, or keystore operations and rejects target values other than `alpha` and `production`.

- [ ] **Step 3: Run the Ruby file and verify RED**

```bash
ruby toris-flutter-play-store-release/tests/immutable_release_test.rb
```

Expected: ERROR or FAIL because both public coordinator methods are missing.

- [ ] **Step 4: Implement archive metadata**

Add `archive_aab` beside `build_only`. Resolve version name through the existing normalized sources. Resolve version code only from `options[:version_code]`, `VERSION_CODE`, or the committed pubspec build number; do not call `git_commit_count` or a Play action. Call `build_once` once, compute `Digest::SHA256.file(path).hexdigest` and `File.size(path)`, and return the schema above.

Write `ARCHIVE_RESULT_PATH` through the existing atomic result writer after extending it to accept the archive schema without removing the current release-result schema.

- [ ] **Step 5: Implement archived alpha upload and production promotion**

Add `deploy_archived_play_store`. It must canonicalize a regular non-symlinked AAB supplied through `options[:aab]` or `VERIFIED_AAB_PATH`, compare the manifest fields supplied by CI, prepare only the Play JSON credential, and use these exact provider shapes:

```ruby
# alpha
actions.upload_to_play_store(
  json_key: credential.fetch(:path),
  aab: artifact_path,
  package_name: package_name,
  track: "alpha",
  release_status: "completed",
  skip_upload_metadata: true,
  skip_upload_changelogs: true,
  skip_upload_images: true,
  skip_upload_screenshots: true
)

# production
actions.upload_to_play_store(
  json_key: credential.fetch(:path),
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

Query alpha before promotion and require the normalized active-code set to equal exactly `[version_code]`. Fastlane promotes every active version on the source track, so an empty, different, or multi-code alpha track must fail before the provider promotion call. Keep the existing direct `release`, Firebase, and retry coordinators unchanged.

- [ ] **Step 6: Expose the lanes and run GREEN**

Route the two lanes in `execute_fastlane_lane`, add explicit `Fastfile` lane blocks, and add `immutable_release` to `run_tests.sh`.

Run:

```bash
ruby toris-flutter-play-store-release/tests/immutable_release_test.rb
ruby toris-flutter-play-store-release/tests/fastlane_helper_test.rb
ruby toris-flutter-play-store-release/tests/authorization_hardening_test.rb
ruby -c toris-flutter-play-store-release/templates/FlutterPlayStoreRelease.rb
ruby -c toris-flutter-play-store-release/templates/Fastfile
```

Expected: all tests PASS and both syntax checks print `Syntax OK`.

- [ ] **Step 7: Commit the Fastlane contract**

```bash
git add toris-flutter-play-store-release/templates/FlutterPlayStoreRelease.rb \
  toris-flutter-play-store-release/templates/Fastfile \
  toris-flutter-play-store-release/tests/immutable_release_test.rb \
  toris-flutter-play-store-release/tests/run_tests.sh
git commit -m "feat(flutter-release): archive and promote exact AABs"
```

### Task 3: Implement immutable GitHub Release publication and download

**Files:**
- Create: `toris-flutter-play-store-release/scripts/github_release_archive.py`
- Create: `toris-flutter-play-store-release/tests/github_release_archive_test.py`
- Modify: `toris-flutter-play-store-release/tests/run_tests.sh`

**Interfaces:**
- `github_release_archive.py publish --repository OWNER/REPO --tag TAG --commit SHA --artifact PATH --metadata PATH`.
- `github_release_archive.py download --repository OWNER/REPO --tag TAG --expected-commit SHA --expected-sha256 SHA --output DIR`.
- Both commands print one non-secret JSON object to stdout and errors to stderr.
- Provider dependency: an authenticated `gh` executable found through `PATH`; tests provide a fake executable and fixture response directory.

- [ ] **Step 1: Write RED publication reconciliation tests**

Use Python `unittest`, a temporary fake `gh`, and recorded argv. Cover repository immutable-policy `404`, new draft creation, exact draft resume, published immutable verification-only retry, duplicate asset names, API digest mismatch, byte-size mismatch, non-`uploaded` state, removable zero-byte draft `starter`, non-removable published `starter`, and normalized-name mismatch.

The exact-match assertion must require `sha256:<local digest>`:

```python
self.assertEqual(
    f"sha256:{hashlib.sha256(aab.read_bytes()).hexdigest()}",
    asset["digest"],
)
```

- [ ] **Step 2: Write RED download and integrity tests**

Cover draft release, mutable release, wrong tag commit, wrong repository, missing/duplicate required assets, path traversal names, asset-ID download, API/checksum/manifest/local/expected digest disagreement, wrong byte size, empty AAB, symlink output, and invalid manifest schema. Assert the output directory must be absent or empty before use.

- [ ] **Step 3: Run tests and verify RED**

```bash
python3 -m unittest toris-flutter-play-store-release/tests/github_release_archive_test.py -v
```

Expected: import failure because `scripts/github_release_archive.py` is absent.

- [ ] **Step 4: Implement strict manifest and asset validation**

Use `argparse`, `hashlib`, `json`, `pathlib`, `subprocess.run`, and `tempfile` only. Validate the three required deterministic names and schema-1 typed fields. Invoke GitHub through argument arrays, never a shell string. Reject any asset basename outside `^[A-Za-z0-9][A-Za-z0-9._-]*$`.

Create drafts with `gh api --method POST repos/{repository}/releases` and `tag_name`, `target_commitish`, and `draft=true`. Reconcile assets through paginated REST results. Never invoke `gh release upload --clobber`. Upload AAB, checksum, and manifest in that order; publish only after a fresh-directory re-download matches every digest.

For downloads, resolve the exact release and asset IDs, require `draft == false` and `immutable == true`, download each ID with `Accept: application/octet-stream`, and compare tag, commit, sizes, API digests, checksum contents, manifest, and expected SHA.

- [ ] **Step 5: Run GREEN and CLI safety checks**

```bash
python3 -m unittest toris-flutter-play-store-release/tests/github_release_archive_test.py -v
python3 toris-flutter-play-store-release/scripts/github_release_archive.py --help
rg -n -- '--clobber|release download.*latest|release view.*latest' \
  toris-flutter-play-store-release/scripts/github_release_archive.py
```

Expected: tests PASS, help exits zero, and `rg` returns no matches.

- [ ] **Step 6: Commit the GitHub Release helper**

```bash
git add toris-flutter-play-store-release/scripts/github_release_archive.py \
  toris-flutter-play-store-release/tests/github_release_archive_test.py \
  toris-flutter-play-store-release/tests/run_tests.sh
git commit -m "feat(flutter-release): verify immutable GitHub release assets"
```

### Task 4: Generate separated archive and deployment workflows

**Files:**
- Create: `toris-flutter-play-store-release/templates/release-android-archive.yml`
- Create: `toris-flutter-play-store-release/templates/release-android-deploy.yml`
- Create: `toris-flutter-play-store-release/tests/workflow_contract_test.rb`
- Delete: `toris-flutter-play-store-release/templates/release-android.yml`
- Modify: `toris-flutter-play-store-release/tests/run_tests.sh`

**Interfaces:**
- Archive dispatch input: `release_tag`, plus existing flavor/entrypoint switches that affect bytes.
- Deploy dispatch inputs: `release_tag`, `expected_commit_sha`, `expected_artifact_sha256`, `target`, and `confirm_production`.
- Archive output assets: deterministic AAB, `.sha256`, and `android-release-manifest.json`.

- [ ] **Step 1: Write RED workflow contract tests**

Parse both template texts and assert full-SHA action pins, `persist-credentials: false`, tag-keyed concurrency, `cancel-in-progress: false`, exact job-level permissions, and absence of PR triggers. Assert archive jobs contain signing secrets but not the Play secret; deploy jobs contain the Play secret but no keystore variables.

Add explicit forbidden-string checks:

```ruby
forbidden = ["--latest", "--clobber", "pull_request_target", "write-all"]
forbidden.each { |value| refute_includes workflow_text, value }
```

For the production branch, assert the workflow passes `target:production` to `deploy_archived_play_store` and contains no `flutter build`, `archive_aab`, `aab:` provider argument, or signing step.

- [ ] **Step 2: Run and verify RED**

```bash
ruby toris-flutter-play-store-release/tests/workflow_contract_test.rb
```

Expected: FAIL because the two templates do not exist.

- [ ] **Step 3: Implement the archive workflow**

Use `workflow_dispatch` only. A non-secret preflight validates the tag and requires GitHub immutable releases to be enabled. The build job checks out the verified tag commit, restores signing only under runner temporary storage, pins Flutter/Java/Ruby/Bundler, invokes `bundle exec fastlane android archive_aab` exactly once, and sends only the AAB plus non-secret metadata through a same-run Actions artifact.

The publish job has `contents: write`, no signing or Play secrets, invokes `github_release_archive.py publish`, and records the release tag, commit, version code, and SHA in the job summary. Pin existing action versions to their full SHAs and use Actions artifact retention only for same-run transport.

- [ ] **Step 4: Implement the deployment workflow**

Use exactly the five dispatch inputs. A no-secret preflight validates lowercase 64-character SHA-256, full 40-character commit SHA, target allowlist, and exact production confirmation. It emits only `play-store-nonproduction` or `play-store-production`.

The Environment-bound deploy job has release-read and Play credentials. It downloads by exact asset IDs through `github_release_archive.py download`, installs checksum-verified bundletool `1.18.3`, reads the embedded package/version/code, verifies the upload certificate fingerprint, and then invokes the archived Fastlane lane. Alpha passes the downloaded AAB path; production passes only package/version code and promotion confirmation.

- [ ] **Step 5: Run GREEN and YAML validation**

```bash
ruby toris-flutter-play-store-release/tests/workflow_contract_test.rb
ruby -e 'require "yaml"; ARGV.each { |p| YAML.safe_load(File.read(p), aliases: false) }' \
  toris-flutter-play-store-release/templates/release-android-archive.yml \
  toris-flutter-play-store-release/templates/release-android-deploy.yml
```

Expected: tests PASS and YAML parsing exits zero.

- [ ] **Step 6: Commit the workflow split**

```bash
git add toris-flutter-play-store-release/templates \
  toris-flutter-play-store-release/tests/workflow_contract_test.rb \
  toris-flutter-play-store-release/tests/run_tests.sh
git commit -m "feat(flutter-release): split archive and promotion workflows"
```

### Task 5: Migrate generated projects and update the standalone package

**Files:**
- Modify: `toris-flutter-play-store-release/scripts/inspect_flutter_project.sh`
- Modify: `toris-flutter-play-store-release/scripts/bootstrap_android_fastlane.sh`
- Modify: `toris-flutter-play-store-release/scripts/validate_release_setup.sh`
- Modify: `toris-flutter-play-store-release/install-manifest.txt`
- Modify: `toris-flutter-play-store-release/SKILL.md`
- Modify: `toris-flutter-play-store-release/README.md`
- Modify: `toris-flutter-play-store-release/templates/PLAY_STORE_RELEASE.md`
- Modify: `toris-flutter-play-store-release/templates/env.example`
- Modify: `toris-flutter-play-store-release/references/environment-variables.md`
- Modify: `toris-flutter-play-store-release/references/execution-defaults.md`
- Modify: `toris-flutter-play-store-release/references/first-release-checklist.md`
- Modify: `toris-flutter-play-store-release/references/troubleshooting.md`
- Modify: `toris-flutter-play-store-release/tests/run_tests.sh`

**Interfaces:**
- Fresh bootstrap creates both new workflows and `tool/flutter-play-store-release/github_release_archive.py`.
- Managed legacy bootstrap atomically deletes `.github/workflows/release-android.yml` and creates both replacements.
- Customized or unowned legacy workflow produces exit `2` with zero project changes.

- [ ] **Step 1: Add RED bootstrap migration tests**

Extend `bootstrap_full` fixtures to cover fresh creation, owned legacy migration, customized legacy conflict, missing sidecar conflict, dry-run delete/create plan, second-run idempotency, and an injected failure after every write/delete boundary. The owned migration must assert:

```bash
[ ! -e "$project/.github/workflows/release-android.yml" ]
[ -f "$project/.github/workflows/release-android-archive.yml" ]
[ -f "$project/.github/workflows/release-android-deploy.yml" ]
```

Require the final sidecar to list only current managed targets, not the deleted legacy path.

- [ ] **Step 2: Add RED inspector and validator assertions**

Update expected JSON/human fixtures so `files_bootstrap_may_change` contains the legacy deletion path, both new workflow paths, and the GitHub Release helper. Require validation to fail when either current workflow is missing, when the legacy active workflow remains, or when a mutable action ref/secret-shaped value appears.

- [ ] **Step 3: Run focused groups and verify RED**

```bash
bash toris-flutter-play-store-release/tests/run_tests.sh bootstrap_full
bash toris-flutter-play-store-release/tests/run_tests.sh inspection
bash toris-flutter-play-store-release/tests/run_tests.sh release_validator
```

Expected: each group FAILS on the old one-workflow inventory.

- [ ] **Step 4: Implement source mappings, migration, and validation**

Map the two workflow templates and helper into generated paths. Register the owned legacy path with `fprs_project_transaction_register_delete` in the same transaction as the new files. Refuse deletion unless the current sidecar contains the path and its SHA-256 matches the actual regular file.

Update all target allowlists, staged-candidate checks, YAML parser loops, required-file checks, sidecar records, inspector booleans, and displayed mutation inventories. Preserve the stable package ID and ownership marker strings.

- [ ] **Step 5: Update runtime inventory and English documentation**

Sort `install-manifest.txt` and include the new helper, tests-excluded runtime files, and both new templates while removing `templates/release-android.yml`.

Document immutable-release and tag-ruleset prerequisites, exact Secrets/Environments, archive dispatch, alpha upload, production promotion, independent hash review, first Play Console binary, unknown-outcome reconciliation, rollback by new version, and legacy direct-lane compatibility. Keep `SKILL.md` under 500 lines and retain its Quick start, execution-policy link, and Definition of done.

- [ ] **Step 6: Run focused and full package suites**

```bash
bash toris-flutter-play-store-release/tests/run_tests.sh bootstrap_full
bash toris-flutter-play-store-release/tests/run_tests.sh inspection
bash toris-flutter-play-store-release/tests/run_tests.sh release_validator
bash toris-flutter-play-store-release/tests/run_tests.sh documentation
bash toris-flutter-play-store-release/tests/run_tests.sh installation
bash toris-flutter-play-store-release/tests/run_tests.sh
```

Expected: all groups PASS, including existing installation recovery tests.

- [ ] **Step 7: Commit the Flutter package integration**

```bash
git add toris-flutter-play-store-release
git commit -m "docs(flutter-release): ship archive-first Play delivery"
```
