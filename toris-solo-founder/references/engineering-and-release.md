# Solo engineering and release

Evidence basis: D01-D06 in [decision rules](decision-rules.md). The workflow below operationalizes those historical lessons; running it still requires current project evidence.

## Establish a bounded task

Inspect the current branch, working-tree changes, project instructions, existing tests, dependency ownership, and acceptance criteria before editing. Record which changes predate this task. Do not make the working tree clean merely to make the report look finished.

Choose the smallest complete user flow rather than disconnected scaffolding. A deliverable includes its loading, empty, failure, and recovery states when they affect acceptance. Reuse the project's architecture unless the request justifies changing it.

## Coordinate by dependency, not by agent count

A task record needs an ID, dependencies, owner, allowed write paths, acceptance checks, evidence, and state. Read-only research can overlap. For writes:

- One writer owns a shared checkout by default.
- Independent writers use explicitly assigned paths and isolated checkouts/worktrees. Shared generated files, manifests, lockfiles, schemas, and migration order still need integration ownership.
- A downstream task starts only after the required upstream artifact is accepted, not when its agent says it is nearly finished.
- A task blocked on access, payment, product choice, or deployment permission remains blocked. Do not silently substitute another outcome.
- An existing solo workflow does not need a permanent agent fleet. Use multiple agents only when the user chose it and the coordination cost is justified.

Suggested states: queued, ready, running, verifying, blocked, done. This is a documentation contract, not an installed scheduler.

## Verification ladder

| Stage | Evidence required | It does not prove |
|---|---|---|
| Source change | Reviewed diff and intended file list | Correct execution |
| Local checks | Actual command, exit status, relevant output, date | Browser/device behavior |
| Interaction | Reproduced user flow on stated browser/device/build | CI, release, or production usage |
| CI | Commit identity and matching run result | Deployment or public availability |
| Artifact/submission | Build identifier, destination, receipt, authorized action | Store approval or a live domain |
| Public verification | Actual requested URL/store track, intended version, observed behavior | Conversion, retention, or revenue |
| Business result | Defined metric, period, denominator, data source | Causality or repeatability without further evidence |

Select checks by risk. Do not run every possible test mechanically, but name omitted high-risk checks. Re-run relevant checks after the final change, not only before editing.

## Safe source delivery

When a commit or push is requested, stage explicit intended paths and inspect the staged diff. Reconcile overlapping edits before committing. Confirm the intended remote branch/commit when remote delivery is part of the task. Without that request, leave a clear local diff; do not opportunistically commit or push.

Never use bulk reset, cleanup, force push, or broad staging to conceal unknown work. A dirty tree can be the correct final state.

## Release diagnosis

Compare these identities: intended source commit, build artifact, deployment receipt, selected environment, bound domain, and actual response. Check the exact affected path and headers before diagnosing cache behavior. A historical failed deployment and a current successful deployment are separate records.

Do not invent a propagation time, keep rebuilding without evidence, or claim a platform dashboard repaired historical failures merely because the latest version succeeded. Use the appropriate existing release skill for actual framework/store procedures.

## Payment acceptance

Maintain distinct results for:

1. Catalog lookup and intended product display.
2. Actual store/payment UI reached.
3. Purchase success or cancellation.
4. Verified entitlement delivery and persistence.
5. Restoration and relevant retry/duplicate/failure behavior.

Capture build version, signing/distribution context, feature flags, environment, and authorized tester conditions without copying account or payment details. A sideloaded artifact and a store-distributed build are not assumed equivalent.

A checkout cancelled by instruction remains a cancelled checkout. The historical payment case behind D05 did not verify purchase, entitlement, or restoration. Do not use it as successful monetization evidence.

## Content and discoverability acceptance

Metadata must describe real visible content. Keep title, author, description, dates, article images, canonical URLs, list count/order, and structured data consistent with the source and rendered output. Unknown values remain absent. A site-wide image is not automatically an article's own image.

Local validity, external structured-data eligibility, indexing, ranking, and AI-answer inclusion are different observations. Use the existing SEO/GEO and store-listing skills where applicable, and verify unstable official requirements at execution time.

## Completion receipt

Use the receipt in [templates and harvest](templates-and-harvest.md). Report the highest verified stage, remaining risk, and the next necessary check. Preserve the separation between source delivery, release delivery, user availability, and a business outcome.
