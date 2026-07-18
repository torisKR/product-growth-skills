# Android Release Skills Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the completed Flutter and Expo release packages into the eight-skill repository, verify every contract, update the two approved Flutter global copies, and push the canonical repository.

**Architecture:** The root validator owns collection-wide static validation and invokes both standalone package suites without recursion. Canonical files are verified first; only then does the existing atomic Flutter updater synchronize its two global destinations. Expo remains repository-only.

**Tech Stack:** Python 3, Bash, Ruby, Git, system skill-creator validation, the Flutter atomic package updater, and GitHub remote `origin`.

## Global Constraints

- The repository reports exactly eight skills and includes both `toris-flutter-play-store-release` and `toris-expo-play-store-release`.
- Do not run a real Flutter/EAS build, GitHub workflow, GitHub Release operation, Play operation, notification, repository-policy change, or application bootstrap.
- The root validator is the only component that invokes both standalone test suites; package suites must not recursively invoke the root validator.
- Update only `~/.claude/skills/toris-flutter-play-store-release` and `~/.agents/skills/toris-flutter-play-store-release`, using the canonical updater after all repository tests pass.
- Do not create a global Expo skill copy or install any global Expo/Android release toolchain.
- Push only after tests, quick validators, canonical/global byte comparison, staged diff checks, and clean status checks pass.

---

### Task 1: Integrate the eighth skill without validator recursion

**Files:**
- Modify: `README.md`
- Modify: `scripts/validate_skills.py`
- Modify: `scripts/tests/test_validate_skills.py`
- Modify: `toris-flutter-play-store-release/tests/run_tests.sh`
- Modify: `toris-expo-play-store-release/tests/run_tests.sh`

**Interfaces:**
- `python3 scripts/validate_skills.py` statically validates all eight skills, then executes each standalone package suite once.
- Environment guard: `PRODUCT_GROWTH_ROOT_VALIDATION=1` prevents package suites from spawning the root validator.

- [ ] **Step 1: Write RED root integration tests**

Extend `scripts/tests/test_validate_skills.py` to assert eight expected skills, per-package runtime/executable mappings, both fixture roots ignored by secret scans, and subprocess calls for exactly these runners:

```text
toris-flutter-play-store-release/tests/run_tests.sh
toris-expo-play-store-release/tests/run_tests.sh
```

Mock only `subprocess.run`; assert repository root as `cwd`, a shell-free argument array, and `PRODUCT_GROWTH_ROOT_VALIDATION=1` in the child environment.

- [ ] **Step 2: Run and verify RED**

```bash
python3 -m unittest scripts/tests/test_validate_skills.py -v
```

Expected: FAIL because package-suite execution and the recursion guard are absent.

- [ ] **Step 3: Remove package-to-root recursion**

Change both `repository_integration` groups so they directly assert root README/catalog content and never invoke `scripts/validate_skills.py` when `PRODUCT_GROWTH_ROOT_VALIDATION=1`. Preserve standalone non-recursive root-file assertions.

- [ ] **Step 4: Implement root suite orchestration and README updates**

Run static validation first. When it succeeds, invoke both test runners through argument arrays with the recursion guard. Stop and identify the package on any nonzero status.

Update the root README from seven to eight skills; add the Expo release catalog row, link-loop name, invocation prompt, repository tree, package test command, quick-validator command, and repository-only/no-global-toolchain statement.

- [ ] **Step 5: Run GREEN**

```bash
python3 -m unittest scripts/tests/test_validate_skills.py -v
python3 scripts/validate_skills.py
```

Expected: unit tests PASS and the validator ends with `Validated 8 skills successfully.` after both package suites pass once.

- [ ] **Step 6: Commit root integration**

```bash
git add README.md scripts/validate_skills.py scripts/tests/test_validate_skills.py \
  toris-flutter-play-store-release/tests/run_tests.sh \
  toris-expo-play-store-release/tests/run_tests.sh
git commit -m "feat: integrate Expo release automation skill"
```

### Task 2: Verify canonical packages and update Flutter global copies

**Files:**
- Verify only: all tracked repository files.
- Update through the canonical script:
  - `~/.claude/skills/toris-flutter-play-store-release`
  - `~/.agents/skills/toris-flutter-play-store-release`

**Interfaces:**
- Canonical updater: `toris-flutter-play-store-release/update.sh --source CANON [--dry-run]`.
- Installed equality covers every canonical `install-manifest.txt` path plus equal receipts.

- [ ] **Step 1: Run language and format checks**

```bash
find toris-flutter-play-store-release toris-expo-play-store-release \
  -type f -name '*.sh' -exec bash -n {} \;
ruby -c toris-flutter-play-store-release/templates/Fastfile
ruby -c toris-flutter-play-store-release/templates/FlutterPlayStoreRelease.rb
ruby -c toris-expo-play-store-release/templates/Fastfile
python3 -m json.tool toris-expo-play-store-release/templates/eas.json >/dev/null
ruby -e 'require "yaml"; ARGV.each { |p| YAML.safe_load(File.read(p), aliases: false) }' \
  toris-flutter-play-store-release/templates/release-android-archive.yml \
  toris-flutter-play-store-release/templates/release-android-deploy.yml \
  toris-expo-play-store-release/templates/release-android-archive.yml \
  toris-expo-play-store-release/templates/release-android-deploy.yml
```

Expected: every command exits zero and Ruby syntax prints `Syntax OK`.

- [ ] **Step 2: Run package and root suites**

```bash
bash toris-flutter-play-store-release/tests/run_tests.sh
bash toris-expo-play-store-release/tests/run_tests.sh
python3 -m unittest scripts/tests/test_validate_skills.py -v
python3 scripts/validate_skills.py
```

Expected: all commands PASS without contacting EAS, GitHub, Play, Slack, Firebase, or an application repository.

- [ ] **Step 3: Quick-validate all eight skills**

```bash
for skill in app-store-listing-creator seo-geo-optimizer \
  flutter-android-performance toris-flutter-play-store-release \
  flutter-interactive-design expo-android-performance \
  expo-interactive-design toris-expo-play-store-release
do
  UV_CACHE_DIR=/tmp/product-growth-skills-uv uv run --with pyyaml \
    python /Users/toris/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"
done
```

Expected: each skill reports successful validation.

- [ ] **Step 4: Scan the final canonical tree**

```bash
git diff --check
python3 scripts/validate_skills.py
git status --short
```

Expected: diff check and the validator pass, and status contains only intended changes or is clean after task commits.

- [ ] **Step 5: Update the two Flutter copies**

```bash
CANON="$PWD/toris-flutter-play-store-release"
"$CANON/update.sh" --source "$CANON" --dry-run
"$CANON/update.sh" --source "$CANON"
"$CANON/update.sh" --source "$CANON" --dry-run
```

Expected: the first dry-run reports intended updates, the update succeeds atomically, and the final dry-run reports `would no change` for both destinations.

- [ ] **Step 6: Prove installed byte equality**

```bash
for dest in "$HOME/.claude/skills/toris-flutter-play-store-release" \
  "$HOME/.agents/skills/toris-flutter-play-store-release"
do
  while IFS= read -r relative
  do
    cmp -s "$CANON/$relative" "$dest/$relative" || exit 1
  done < "$CANON/install-manifest.txt"
done
cmp -s \
  "$HOME/.claude/skills/toris-flutter-play-store-release/.skill-install-receipt" \
  "$HOME/.agents/skills/toris-flutter-play-store-release/.skill-install-receipt"
```

Expected: all comparisons exit zero. Confirm no global Expo skill directory was created by this task.

### Task 3: Review and push the verified repository

**Files:**
- Modify only when a review finding has a test-first fix.
- Push branch: `main` to `origin/main`.

**Interfaces:**
- Remote: `https://github.com/toris-dev/product-growth-skills.git`.
- Completion means local `main` and `origin/main` identify the same final commit and the worktree is clean.

- [ ] **Step 1: Request a whole-branch review**

Generate the subagent-development review package from merge base `bc21dfc` through current `HEAD`. Ask the reviewer to check the approved design, both implementation plans, security boundaries, same-AAB promotion semantics, tests, documentation, and global installation contract.

Expected: no Critical or Important findings. If findings exist, dispatch one fixer with the complete list, require focused tests, and re-review.

- [ ] **Step 2: Run final verification after review fixes**

```bash
bash toris-flutter-play-store-release/tests/run_tests.sh
bash toris-expo-play-store-release/tests/run_tests.sh
python3 scripts/validate_skills.py
git diff --check
git status --short
```

Expected: all tests PASS and the tree is clean after committing any test-first review fix.

- [ ] **Step 3: Push and verify synchronization**

```bash
git push origin main
git rev-parse HEAD
git rev-parse origin/main
git status --short
```

Expected: push succeeds, both revisions match, and status is empty.

- [ ] **Step 4: Record the implementation boundary**

Report changed skills, commit, test commands, global Flutter-copy equality, and remote synchronization. State that no application build, GitHub Release, EAS request, Play upload/promotion, or repository-policy change was executed, and list the application-side Secrets, Environments, immutable-release setting, tag ruleset, and first Play upload that remain for the user.
