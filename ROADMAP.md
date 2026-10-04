# AgentSafe — Roadmap Draft

**Status:** Proposed, October 5, 2026. No implementation before explicit approval of the document set.  
**Planning rule:** advance on evidence and exit criteria, not a fixed release date. The scope in PRODUCT.md takes precedence over feature enthusiasm.

**Second-pass review:** Resolve the [product review recommendations](PRODUCT.md#second-pass-review--october-5-2026) before adopting the launch checklist below. First determine where target users actually publish artifacts. The original blanket-review policy and complete hook lifecycle are not prerequisites for the initial scanner experiment.

## Phase 1 — Demo and demand validation

**Question:** does a screenshot/debug-artifact publication gate solve a recurring job better than existing secret hooks and manual review?

### Deliverables after document approval

- Recruit 8–12 developers who actually publish agent/browser-generated evidence to public GitHub; document workflows, existing tooling and recent near misses without collecting private files.
- For each candidate, map recent publications to Git pushes, release/API uploads, attachments or CI artifacts. Record whether an installed pre-push hook would actually have run; do not use a general screenshot-leak incident as validation of a Git-only interception point.
- Create synthetic fixtures: an image with a configured internal URL/email, an authenticated HAR, a benign public screenshot, and a video marked uninspected. Use reserved fictional domains, fake names and nonfunctional credential examples.
- Build one runnable vertical slice: a local repository, a controlled Git push destination, exact committed artifact reads, local image OCR, header rules, a blocked push, inspection and a reviewed retry.
- Demonstrate the add-then-delete failure mode: the gate still detects the earlier outgoing artifact. Do not use a final-diff-only prototype as proof of protection.
- Produce a 30–45 second terminal demo/storyboard and a static synthetic before/review comparison. Label assumptions, fixture data and any mocked visibility API. Never simulate a pass and present it as working software.
- Compare outcomes with an existing credential gate plus manual image review. State the concrete incremental benefit rather than claiming existing tools miss all images.
- Run clean-machine installation experiments for Tesseract/Python on macOS and Linux, plus a Windows feasibility check.

### Exit criteria

- At least 5 interviewees show a recent artifact-publishing workflow and want to try the gate on that workflow.
- The runnable demo reliably blocks the selected synthetic cases, explains the exact version/destination, and never prints raw sensitive values.
- Users can explain its purpose in one sentence after 30 seconds with the README.
- At least 3 target users complete a trial inspection/review without maintainer coaching; record where the CLI fails.
- The proposed install path is credible and its native dependency cost is visible.

### Stop or narrow

If interest is only in API keys, refer users to established scanners rather than expanding the catalog. If capture/export review is valued but a push hook is not, pivot to a smaller screenshot review/export command. If cross-repository/API upload enforcement is required, recognize that a repository-local hook cannot deliver it.

## Phase 2 — v0.1 public launch

**Question:** will target users keep a small local gate enabled during ordinary work?

### Deliverables

- The exact PRODUCT.md v0.1 scope: GitHub.com visibility; robust outgoing artifact-version enumeration; PNG/JPEG OCR and publishing review; debugging text/HAR header scanning; opaque artifact review; hook lifecycle; minimal CLI; exact-content approvals and explicit ignores.
- A one-week pilot with at least 5 target users, collecting voluntary counts and usability feedback rather than artifacts, OCR text or private repository names.
- A labeled synthetic evaluation set of at least 100 cases, separated into supported positive/negative cases and difficult/unsupported cases. Publish per-rule counts, precision, recall, OCR misses and intentional review burden.
- Clean macOS/Linux setup guides and supported runtime versions. Windows is experimental until equivalent installation/hook tests pass. No cross-platform claim based solely on Python.
- A documented limit/error policy, ordinary-hook coexistence recipe, accurate JSON schema/exit codes, and safe historical remediation instructions.
- A distinctive cleared distribution name, approved open-source license, dependency/license inventory, project-owned package/release channels and a SECURITY.md disclosure route.
- Replace all proposed README examples with verified commands and a real synthetic recording. Keep limitations close to the quickstart.
- CI for this project's tests on supported platforms. This is release verification, not a user-facing CI scanner feature.

### Launch gates

| Gate | Proposed threshold |
| --- | --- |
| Demand/retention | At least 3 of 5 pilot users keep the gate enabled and use it on another real push without prompting |
| HIGH findings | At least 95% precision on labeled supported-rule cases; publish numerator/denominator |
| Supported detection | At least 90% recall on legible declared-rule positives; publish misses separately |
| Review friction | Record reviews per push, time per review, overrides and disablement; no unbounded growth hidden behind a precision score |
| Git correctness | Required history/ref/remote scenarios in ARCHITECTURE.md pass; add-then-delete/add-then-redact must stop publication |
| Honest coverage | No silent pass on a required scanner/range/limit failure; unsupported content and ignores remain visible |
| Privacy | No artifact/OCR uploads or default raw-value output; observed/tested network behavior matches docs |
| Performance | Target p95 <15 seconds for 10 fresh 1080p images + 10 small text artifacts on named hardware; <1 second added overhead without candidates, excluding network/Git cost |
| Setup | Target first protected synthetic push in <5 minutes on clean macOS/Linux with documented prerequisites |
| Trust | Name/license/distribution ownership verified; README limitations and review default tested with readers |

Thresholds are goals, not achieved claims. A small synthetic corpus is not a general accuracy guarantee. If quality or retention fails, adjust scope/policy and repeat the pilot before publishing a protection claim.

### Explicitly do not add for launch

Automatic redaction, QR decoding, video/PDF inspection, required gitleaks integration, ML dashboard/name detection, MCP/IDE/agent plugins, global hooks, enterprise enforcement, cloud scanning, SaaS dashboards and organization management.

## Phase 3 — Post-launch, selected by evidence

**Question:** which addition removes the largest observed limitation without weakening trust or expanding into an enterprise platform?

Prioritize maintenance and adoption before format count:

1. Fix reported false positives, OCR usability and setup failures. Stabilize Windows if actual users need it. Publish updated quality/latency measurements and keep backward-compatible JSON semantics where practical.
2. Improve review workflow: better local annotated previews, batch review of individually identified versions, and more useful remediations. Keep exact-content/context approvals and explicit coverage.
3. Evaluate a local redaction/export path only if users repeatedly need it. Start with an immutable input and a separate output file, solid masks, re-encoding/metadata removal, visual review and rescan. It must not imply earlier Git versions were sanitized or automatically rewrite history.
4. Add an optional maintained secret-engine adapter if users request a unified report; reuse an engine rather than implement token rules. Reassess Gitleaks/Betterleaks maintenance before backend commitment.
5. Evaluate local QR decoding or a single additional format using a dedicated corpus. QR presence remains a review signal; PDF layers, animations and video sampling must have explicit incomplete-coverage behavior.
6. Add another visibility provider or an opt-in agent/CLI integration only when a measured workflow requires it. API/attachment publication and adjacent agent-created repositories need a new interception model, not a marketing extension of the pre-push guarantee.

Do not promise all six. Rank requests by affected retained users, expected review burden reduction, maintainability and data-flow implications. Document a new threat model before adding cloud processing or centralized enforcement.

## Evidence to collect

No automatic telemetry in v0.1. Ask for opt-in aggregate feedback: setup time, scan duration, number of inspected/uninspected/ignored artifacts, review decisions, false positives, hook disablement and whether a real workflow benefited. Contributors may submit synthetic reproductions. Never ask users to paste private captures, HAR contents, raw credentials or full OCR transcripts into public issues.

## Current review checkpoint

The deliverable at this checkpoint is five English Markdown drafts, not a runnable demo. Implementation, dependencies, fixtures, hooks, branding assets and release publication begin only after explicit approval. Approval of the product scope does not itself authorize external publication or uploading real user artifacts.
