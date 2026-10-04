# AgentSafe — Product Definition

**Status:** Draft for review. No product implementation is authorized yet.  
**Research date:** October 5, 2026.  
**Working name:** AgentSafe; naming clearance is unresolved.

## Second-pass review — October 5, 2026

**Review status:** The first-pass default policy and release scope below are under reconsideration, not approved requirements. The following recommendations require a coordinated revision before implementation; they do not silently replace the detailed contracts below.

1. **Validate the interception point first.** Screenshot exposure demonstrates a problem, but does not establish Git push as the main publishing path. Ask prospective users to reconstruct their last three artifact publications: tracked Git blobs, release/API uploads, attachments or CI artifacts. A pre-push product should be pursued for users whose actual path it covers. Otherwise evaluate an explicit local pre-publication check integrated with one uploader; do not add a universal egress platform.
2. **Prefer selective blocking as the default hypothesis.** Block strong credential/configured-sensitive findings; warn on generic emails, ordinary cookies and uninspected formats. A successfully inspected image without a finding should not require automatic approval merely for being an image. An opt-in strict policy can require review of every selected image. This accepts residual visual-context risk and must state that clearly. Supported-scan failures remain visible errors; changing the default is a product trade-off, not improved detection.
3. **Reduce the first implementation experiment.** Start with PNG/JPEG, explicit file scanning and staged scanning, a few evidence rules, masked output with useful visual locations, and a narrowly scoped exception. Establish useful findings and setup usability before building the complete hook/approval lifecycle. For a Git-focused v0.1, add a correct pre-push adapter after this experiment; defer HAR-specific parsing, export/report coverage, mandatory opaque-artifact approvals and advanced approval administration unless pilots need them.
4. **Do not leave a credential-shaped hole in the screenshot promise.** Keeping an existing source scanner installed does not automatically route OCR text into it. Either add a small adapter to one mature local secret engine or explicitly disclose that standalone API keys/passwords in images are outside the initial rules. Reuse detection; do not write a provider-token catalog.
5. **Narrow the audience by exposure context.** Prioritize developers who work with real authenticated/internal data and publish external demos or reproductions. The weekly-public-Git criterion is appropriate only after validating the publishing channel. A generic open-source frontend developer may have little sensitive content to protect.
6. **Measure unwanted interruptions, not just rule accuracy.** A correctly detected public email can still produce a wrong publishing decision. Label both entity presence and whether publication should be stopped. Report benign pushes interrupted, time to resolve, repeated overrides and tool disablement. The existing 95%/90% targets and 3-of-5 pilot threshold are planning hypotheses, not statistical evidence of product-market fit.
7. **Keep implementation choices provisional.** Benchmark OCR quality on small-font browser screenshots and installation on clean machines before committing to Tesseract. Avoid making every new branch trigger a full-history rescan when trustworthy destination-specific remote refs establish already-published history. Full traversal remains a conservative fallback, not the desired normal UX.
8. **Do not equate an exception with human authorization.** An agent trying to finish a legitimate task may invoke a documented `allow --yes` without being malicious. Default guidance should ask it to report a blocked finding and wait for the user's decision, rather than recommending self-approval. This is cooperative behavior guidance, not tamper-resistant enforcement.

The immediate decision is whether to validate a **Git artifact gate** or a **pre-publication artifact check** at a different upload point. The core local scanner can support either later; the launch promise should choose one covered workflow.

## 1. Recommendation

Build a small, local publication gate for screenshots and debugging artifacts headed to public GitHub repositories. Start with developers who use browser-capable coding agents to produce visual evidence for a change.

The broader vision is **privacy protection for AI-generated development artifacts**. The first product promise should be narrower:

> Review screenshots and debugging artifacts before they enter a public Git repository.

Brand line:

> Don't accidentally publish what your AI agent saw or generated.

This is a plausible open-source tool, but demand, retention, and differentiation are not established. An OCR wrapper around a secret scanner would be easy to copy. The strongest hypothesis is a useful publication workflow: correct Git scope, evidence tied to the exact artifact, destination-aware decisions, and approvals that expire when content changes.

Do not position v0.1 as comprehensive DLP, guaranteed privacy, or a system that can recognize every confidential screen.

## 2. What is supported by evidence

Glow's PixelLeak research describes coding agents publishing internal review screenshots to adjacent public repositories. This supports the existence of the failure mode, including public artifact repositories alongside private code repositories. It is a vendor-reported investigation, not independent evidence of market size, willingness to install, or this product's effectiveness. [Primary research](https://www.glow.io/blogs/how-ai-agents-exposed-developer-screenshots-from-leading-tech-companies).

Our inference: the first audience should be people publishing visual debugging evidence, rather than everyone using an AI editor. A repository-local hook would only help in a public destination where it was installed; it would not automatically protect a new adjacent repository created by an agent.

**Second-pass correction:** [gitshot's documented default backend](https://github.com/vipulgupta2048/gitshot#how-it-works) uploads images as GitHub Release Assets in a dedicated public repository. That upload path does not invoke the developer's local Git pre-push hook. Therefore the cited incident is evidence of artifact exposure, not evidence that this proposed hook would have prevented all or most reported cases. The share of incidents occurring through a covered Git push has not been established.

## 3. Critical assessment

| Assumption or risk | Assessment | Product consequence |
| --- | --- | --- |
| Traditional scanners cannot inspect images | Too broad: OCR-enabled scanners and local screenshot redactors already exist | Differentiate through publishing workflow, not OCR alone |
| AI-generated files can be reliably identified | Git generally has no reliable authoring provenance for a file | Scan selected artifacts regardless of whether a person or an agent created them |
| An email, private IP, cookie, or QR code proves a leak | False: public contact information, preference cookies, examples, localhost and public QR links are common | Distinguish evidence, sensitivity, and review requirements |
| OCR can identify an internal dashboard | OCR extracts readable text; confidentiality requires context it may not have | No dashboard classifier or confidentiality claims in v0.1 |
| A local-first design is a moat | Existing tools also process locally | Treat local processing as a trust requirement |
| A pre-push scanner only needs the final diff | Unsafe: a removed artifact can still exist in outgoing commits | Inspect relevant artifact versions across outgoing history |
| A hook provides enforcement against an agent | An agent with local shell access can disable or bypass it | Address accidental publishing by cooperative users; no adversarial enforcement claim |
| A private destination is safe forever | Visibility can change without another local push | Display the boundary; later visibility changes need a separate audit |
| Unknown visibility means private | Incorrect: authentication, network errors, aliases and unsupported providers create uncertainty | Apply public policy to UNKNOWN; show the uncertainty |
| Generated artifacts are a large recurring problem for everyone | Unproven; many artifacts never enter Git | Recruit users with actual artifact publishing workflows |
| A dramatic demo demonstrates accuracy | A few staged examples say little about benign assets and OCR misses | Evaluate benign fixtures, misses, latency and repeated use |
| Cross-platform installation will take two minutes | Native OCR dependencies may dominate setup, especially on Windows | Validate setup on clean machines; do not claim a single-binary installation |
| Blocking every changed image is acceptable | Unproven; it may be excessive for asset-heavy projects | Make it an explicit review policy and test retention before launch |

The primary alternative to a new scanner is good artifact hygiene: keep raw captures outside the worktree, use synthetic data, publish only reviewed copies, and use `.gitignore` before files become tracked. AgentSafe must prove that its incremental help justifies its friction.

## 4. Competitive landscape

Capability statements below describe public documentation reviewed on the research date. They are not hands-on evaluations or claims of completeness. Absence from a README is not evidence that a competitor cannot add a feature.

| Project or category | Documented overlap | Implication |
| --- | --- | --- |
| [Prowl](https://github.com/Lercas/prowl) | Documents local OCR for images/image-only PDFs and Git/CLI workflows; README specifies PolyForm Noncommercial 1.0.0 | Close documented capability overlap, not a hands-on validated equivalent or an unrestricted reusable dependency |
| [Screenshot Redactor](https://github.com/cleanroom-ai/screenshot-redactor) | On-device screenshot privacy review and redaction, including PII and QR codes | Direct substitute for preparing an image before sharing; possible component or interoperability reference |
| [RedactShot](https://github.com/SpookySandwich/RedactShot) | Windows capture workflow with local OCR and PII review | Competes earlier in the capture-to-share workflow |
| [Talisman](https://github.com/thoughtworks/talisman) | Git hooks, suspicious file/content/size checks and checksum-based exceptions | Artifact hygiene and content-bound exceptions are not new ideas |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Credential detection in Git, files and stdin; hook integration | Complement for mature secret rules; do not duplicate its rule catalog |
| [GitGuardian / ggshield](https://docs.gitguardian.com/ggshield-docs/integrations/overview) | Secret scanning across Git and coding-agent integrations | Agent integration alone is not differentiation; compare coverage and data flow fairly |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | Credential detection and optional provider verification; multiple sources and file formats | Complement/substitute for secret-focused workflows; avoid unsupported claims about binary coverage |
| [GitHub push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection) | Server-side blocking of supported credential patterns | Strong existing protection; AgentSafe must add artifact context beyond credentials |
| [Presidio Image Redactor](https://github.com/microsoft/presidio/tree/main/presidio-image-redactor) | PII detection/redaction in images | A toolkit rather than a Git publishing product; reuse/reference rather than claim novel image PII detection |
| Enterprise DLP and agent runtime controls | Adjacent prevention budgets and policy workflows | Different scope and deployment burden; not the v0.1 customer |
| Manual review, external redactors and `.gitignore` | Often solve the same job with no new hook | The strongest adoption competitor may be doing nothing beyond existing hygiene |

No exhaustive market survey or unique-category claim is implied. Research has not established a mature tool with precisely this proposed combination; that is not proof of an empty market.

Feature listings establish prior implementations, not product maturity, adoption, reliable detection or market saturation. Evaluate close substitutes on the same workflow before treating them as equivalent alternatives. Public source availability also does not establish a permissive license.

### Name collision

The working name already appears in an [archived agent-tool security project](https://github.com/brian93512/agentsafe), a [local-agent sandbox](https://github.com/Debashish-Mukherjee/agent-safe), and a [scoped npm package](https://www.npmjs.com/package/@decionis/agentsafe). These are branding/search/distribution conflicts, not a determination of trademark rights.

Keep the working name during review. Before launch, select a distinctive name and check repository, package, executable and domain availability. Do not tell users to install an unverified package named `agentsafe`. Naming directions such as "ArtifactGate" or "CaptureGate" are suggestions, with availability unchecked.

## 5. Initial target user

**Primary persona:** an individual open-source web developer or small-project maintainer who uses a browser-capable coding agent or browser test runner, publishes screenshots/debug artifacts to public GitHub at least weekly, and can install a local hook.

Typical job:

> I need to show that a UI change works, without publishing a real account, internal URL, or authenticated debugging session along with it.

Recruit by workflow rather than tool brand. Codex, Claude Code and Cursor users qualify when they actually produce and publish these artifacts. No tool-specific integration is necessary for the first release.

**Secondary later audience:** contributors copying sanitized evidence from internal projects to public reproductions; maintainers of public test fixtures.

**Exclude initially:** developers who only generate source code; enterprise security buyers; teams requiring centrally enforced policy; media-heavy projects expecting video inspection; users seeking prompt filtering, malware prevention or autonomous-agent sandboxing.

## 6. Threat model

### Protected assets and event

Protected data includes credentials in debugging evidence, employee/customer email addresses, configured internal domains, authenticated HTTP headers and unreviewed visual context. The threat event is accidental external publication of a selected development artifact through a local Git push.

Sequence:

1. A developer or agent captures or generates sensitive evidence.
2. The artifact is committed, often after a broad `git add .`.
3. A local Git push targets a public or unverified repository.
4. The installed gate inspects outgoing artifact versions before Git sends the push.
5. It stops the push for strong findings, outstanding artifact review, or incomplete inspection.

The normal workflow includes `git commit` between `git add` and `git push`. Uncommitted/index files are not what pre-push publishes.

### Trust boundary and assumptions

- The user intends to cooperate with the gate and has installed it in the repository being pushed.
- The destination comes from the actual push invocation, not necessarily `origin` or the checked-out branch.
- The gate reads committed blobs rather than trusting current working-tree content.
- Local configuration, approvals and installed dependencies are trusted for this accidental-leak model.
- Artifact content is untrusted parser input and must never become executable instructions.
- Git and visibility services supply routing metadata; uncertainty must remain visible.

### Explicit exclusions

- A malicious agent/user disabling hooks, using `--no-verify`, modifying approval state, or exfiltrating through another channel.
- Uploads through GitHub APIs, issue/PR attachments, release assets, Git LFS transfers, CI uploads, cloud storage or other worktrees without the hook. LFS pointers are identified as uninspected, not scanned payloads.
- Agent prompts sent to a model provider, browser/network exfiltration and files outside Git.
- Guaranteed detection of customer names, faces, charts, trade secrets, tiny text, non-English text, hidden metadata or steganography.
- Existing remote history, unrelated refs, or a private repository later made public through its hosting UI.
- General source-code secret scanning, repository-wide incident response, compliance certification, or credential rotation.

The gate can reduce accidental publication in its covered path. It cannot certify that an artifact is safe or revoke information already published.

## 7. Small v0.1 scope

### Included

1. **GitHub.com destination visibility:** anonymous metadata lookup where possible; optional reuse of authenticated GitHub CLI. PUBLIC, PRIVATE, INTERNAL and UNKNOWN are separate displayed states. UNKNOWN uses public policy. A user may assume public to operate offline; no setting may silently relabel unknown/public as verified private.
2. **Outgoing Git scope:** all hook ref updates, outgoing commit history, changed artifact versions including subsequently deleted versions, deduplicated blob scans. First/new-ref pushes may require full reachable history. Missing history must produce an error, not a clean result.
3. **PNG/JPEG review:** local OCR with coordinates for readable text; email and internal-domain rules. Every selected new/changed image version requires one content-bound publishing approval even with no rule hit. This conservative policy compensates for semantic blind spots; its friction must be validated.
4. **Debugging text:** bounded UTF-8 `.log`/`.txt`, and HAR HTTP headers/cookies. Text-like JSON/CSV and generated Markdown are selected in explicit artifact directories; basic textual rules only. No arbitrary report understanding or full HAR payload analysis.
5. **Small deterministic rule set:** emails, configured internal domain matches, populated Authorization/proxy-authorization values, and populated Cookie/Set-Cookie values. Only explicitly configured session-cookie names justify HIGH cookie findings; other populated cookies require review. Exclude obvious empty/placeholders and reserved example domains from generic identifier findings; an explicitly configured sensitive-domain match takes precedence. Do not implement a provider-secret catalog.
6. **Opaque artifact inventory:** recognized PDF, video, archive, unsupported image and LFS pointer candidates require review as uninspected content. Recognition is cheap inventory, not content scanning. No extension can turn a failed supported scan into an opaque approval shortcut.
7. **Repository-local pre-push hook:** explicit installation/removal, idempotency, no existing-hook overwrite, no interactive prompt inside a push.
8. **CLI:** `init`, `scan`, `inspect`, `allow`, `doctor`, `uninstall`; plain terminal and JSON output with stable exit codes.
9. **Exceptions:** narrowly configured ignore patterns and local approvals tied to exact content, path, destination and policy. No automatic broad allowlist or baseline trust.

QR decoding is deferred. Images still require visual review, including QR content. If QR detection later ships, the presence of a QR code alone must not mean HIGH severity.

### Artifact selection boundary

Select all PNG/JPEG files, known capture/media/document formats, `.log`, `.txt`, `.har`, and LFS pointer blobs, using file signatures and names together. Select JSON, CSV, Markdown and other text in configured artifact directories such as `screenshots/`, `captures/`, `artifacts/`, `debug/` and `reports/`. Directory names only select candidates; they do not prove provenance or sensitivity.

Ordinary source files and generic JSON/CSV/Markdown outside those directories are outside the core gate. Report out-of-scope and ignored counts. Unknown extensionless binary blobs cannot be guaranteed to be classified. `.gitignore` alone does not exempt already tracked artifacts.

### Policy, confidence and coverage

| Observation | Severity / status | PUBLIC or UNKNOWN | Verified PRIVATE or INTERNAL |
| --- | --- | --- | --- |
| Non-placeholder Authorization value or populated configured session cookie in text/HAR | HIGH, direct/configured content evidence | Block until fixed or explicitly approved | Warn |
| Configured internal domain in URL/email, strong extraction | HIGH, configured sensitivity | Block until fixed or explicitly approved | Warn |
| Generic email without sensitivity context | MEDIUM, possible personal information | Review required | Warn |
| Populated cookie without configured session sensitivity | MEDIUM, possible contextual information | Review required | Warn |
| Selected image, including one without rule matches | REVIEW, publishing decision, not a leak finding | Exact-version review required | Inform |
| PDF/video/archive/unsupported image/LFS pointer candidate | REVIEW, not inspected | Exact-version review required with coverage acknowledgement | Inform |
| Large generated artifact within processing limits, no other signal | LOW | Warn only | Inform |
| Required scanner missing, timeout, malformed supported input, unknown Git range or limit exceeded | ERROR, incomplete coverage | Stop with exit 2 | Stop with exit 2 |
| Selected text fully inspected without relevant signals | No detected finding | Pass | Pass |

An OCR-derived match must report extraction uncertainty. A low-confidence domain/header match becomes MEDIUM/review, rather than HIGH certainty. Every image already requires review. No percentage is presented as a calibrated probability of leakage.

Private/internal destinations use advisory privacy policy; they are not declared safe. Selected supported artifacts require inspection in every visibility state; only finding/review enforcement becomes advisory for verified private/internal destinations. Structural/configuration/Git errors remain errors. Automated success must never hide failed inspection. Errors cannot be waived through `allow`; fix the environment/input/limit, or explicitly alter scope with a visible ignore rule.

### Out of v0.1

- Automatic redaction, an image editor, `agentsafe redact`, and automated rewriting/amending/rebasing of commits.
- Video frames/audio transcription, PDF OCR/text extraction, archive recursion, LFS fetching and full export analysis.
- QR decoding, face recognition, person/customer-name recognition, arbitrary organization-name detection and internal-dashboard classification.
- Cloud LLM or vision calls, agent transcript ingestion, provenance attribution and background file monitoring.
- Provider token catalogs and live credential validation; optional existing scanners remain separate initially.
- Mandatory gitleaks adapter, MCP server, Codex/Claude/Cursor plugins and IDE extensions.
- GitLab/Bitbucket/enterprise API adapters; non-GitHub destinations receive UNKNOWN/public policy, without claiming verified visibility.
- Server-side organization enforcement, dashboards, SaaS accounts, RBAC, audit compliance, SARIF and CI products.
- Global hook rollout across arbitrary repositories and automatic protection for agent-created repositories.

## 8. CLI contract

Commands below are a proposed interface, not available software.

| Command | Purpose |
| --- | --- |
| `agentsafe init` | Check dependencies/destination, write a minimal config and install the repository hook if the hook slot is available |
| `agentsafe init --assume-public` | Use conservative public policy without needing a visibility lookup; label the assumption |
| `agentsafe scan --staged` | Inspect index blobs before committing; preview only, does not authorize an arbitrary future push |
| `agentsafe scan --remote origin --ref HEAD` | Read-only rehearsal for one local ref; resolve its destination target or require `--to-ref`; actual hook remains authoritative |
| `agentsafe scan --remote origin --ref HEAD --to-ref refs/heads/main` | Explicit preview of the named update; report that server state may change |
| `agentsafe scan --staged --format json` | Structured output; explicit scan scope and coverage |
| `agentsafe inspect F12` | Masked finding details, committed version, coordinates/line location and remediation instructions |
| `agentsafe inspect F12 --open` | Explicitly materialize/open the exact Git artifact locally for human visual review; disclose that the raw artifact is being opened |
| `agentsafe allow F12 --reason "Reviewed synthetic demo"` | Approve the displayed findings and publishing-review requirements of this exact artifact item; interactive confirmation only in this command |
| `agentsafe allow F12 --reason "Reviewed synthetic demo" --yes` | Explicit noninteractive equivalent; cooperative automation only, not verified human authorization |
| `agentsafe allow --list` / `agentsafe allow --revoke A7` | Inspect masked approval metadata or revoke an approval |
| `agentsafe doctor` | Explain runtime/OCR/hook/config/destination problems without uploading artifacts |
| `agentsafe uninstall` | Remove only AgentSafe's managed hook and installation metadata; retain approvals until separately cleared |

Initialization must be rerunnable. An existing hook directory is normal; an unchanged AgentSafe-owned hook permits reruns. An unrelated hook or a shared/global hook destination is a conflict: provide a manual composition recipe rather than overwriting, auto-chaining, or installing globally. Documentation must show how both hooks receive the same arguments and complete stdin. A visible preflight explains config and hook changes before performing them; `--yes` is the explicit automation mode.

Example of proposed output (synthetic data):

```text
AgentSafe Privacy Gate
Destination: github.com/example/ui-demo
Visibility: PUBLIC (verified for this push)
Scope: 3 outgoing commits -> 4 artifact versions

HIGH    F12  screenshots/dashboard.png @ 8f3a2c1
        Configured internal URL; email address (OCR)
        Exact image version requires review
HIGH    F13  debug/session.har @ 8f3a2c1
        Authorization and session-cookie values present
REVIEW  F14  demo.mov @ 21ab9de
        Video content not inspected; publishing approval required
LOW     F15  artifacts/output.json @ 21ab9de
        Large generated artifact; size alone is not a leak

Coverage: 3 inspected, 1 uninspected, 0 ignored, 0 errors
Push stopped: 2 HIGH artifact items and 1 REVIEW-only item.

Next: agentsafe inspect F12 --open
Fix the outgoing commit history, or explicitly approve reviewed content.
```

Generic email addresses alone must not label a screenshot HIGH. The internal URL and session-cookie name in this example match explicit sensitivity settings; Authorization independently justifies the HAR item's HIGH severity. Do not display raw tokens, full OCR transcripts, decoded payloads or surrounding confidential text by default. Coordinates, line numbers and finding categories are sufficient for terminal triage.

**Exit codes:** 0 = no outstanding gate requirement in the declared scope; 1 = finding/review stops publication; 2 = inspection or setup error. A JSON report distinguishes `pass`, `pass_with_exceptions`, `blocked`, `advisory` and `error`, with visibility and coverage alongside the verdict. Exit 0 does not certify privacy.

### Exceptions and recovery

`allow` uses an artifact-item ID from a stored masked scan manifest. One item groups all evidence and publishing-review requirements for one blob/path/destination; a HIGH image item includes its image review, rather than requiring a second hidden approval. Before recording an exception, the command lists every finding/coverage limitation being accepted and requests explicit confirmation. It records blob ID, path, repository/destination identity, the displayed rule/review requirements, policy fingerprint, reason and timestamp. Changed bytes, destination, path, or relevant policy invalidate approval. Approval never covers another artifact item or newly introduced requirements. IDs are local and resolvable after a blocked push; expired/missing manifests require a rescan.

An UNKNOWN visibility result can still have a well-defined destination identity and use exact-content approvals under public policy. If routing/aliases prevent establishing that identity, inspection may produce a conservative preview, but the gate returns a destination-resolution error until a recognizable destination is used. It must not issue reusable approvals under a generic UNKNOWN identity.

Ignore patterns live in explicit configuration and are visible in every coverage summary. Do not ship broad ignores such as `screenshots/**`, `*.png` or `debug/**`. Ignore rules remove inspection coverage and can persist across content changes; explain that distinction from `allow`. Reasons/paths themselves can contain sensitive information, so approval state stays under the Git directory and prompts recommend nonsensitive reasons.

After a push is stopped, modifying a worktree file or committing a later deletion does not remove an earlier sensitive version. The user must amend/rewrite the unpushed commits that contain it, then rescan. The tool explains this and never performs history surgery. If exposure already happened, refer to incident handling and credential rotation through existing tools.

## 9. Validation and decision gates

These are proposed acceptance targets, not measured results:

- Interview 8–12 people fitting the primary workflow; require at least 5 with recent real artifact-publishing examples, not just interest in AI safety.
- Run a one-week opt-in pilot with at least 5 users; at least 3 keep the gate enabled and use it on another real push without prompting.
- Compare against existing secret hooks and manual review on the same synthetic fixtures. Show incremental screenshot/privacy context, not a relabeled token alert.
- Use at least 100 synthetic cases with a documented positive/negative split, image-quality variations and benign logos/screenshots/public emails/local URLs. Publish per-rule precision and recall with counts; do not extrapolate small-corpus results to all data.
- Target at least 95% precision for automatic HIGH findings and at least 90% recall on legible, declared supported-rule positives. Measure unreadable/unsupported cases separately. REVIEW policy stops are not true-positive leak detections; report their burden independently.
- For 10 fresh 1080p images plus 10 small text artifacts on named reference hardware, target p95 hook overhead under 15 seconds; no candidate changes should add under 1 second excluding network/Git cost. Show cold and cached timings separately.
- Target first successful protected synthetic push within 5 minutes on clean macOS/Linux machines with documented prerequisites. Windows setup remains a separately measured experimental tier unless it passes equivalent tests.
- Zero silently skipped supported artifacts, zero raw payloads in default/JSON reports, and explicit tests for historical deleted blobs and hook conflicts.

If users only care about source-code tokens, redirect them to mature scanners. If they value screenshot review but repeatedly disable the hook, pivot to a smaller **review-and-export command for publishable screenshots**, with integrations to existing redactors. If they need protection across all upload channels and agent-created repositories, a local repository hook is insufficient; do not imply this MVP solves that problem.

## 10. Decisions to review before implementation

1. Accept the narrow primary user and GitHub.com visibility scope.
2. Accept exact-version review for every selected image, subject to pilot evidence; changing this default requires updating the threat/coverage promise.
3. Accept no automatic redaction, QR decoding, video/PDF inspection or mandatory secret-engine adapter in v0.1.
4. Accept Python plus a separate native OCR dependency, with installation as a launch gate.
5. Choose a distinctive public name and an open-source license before distribution. MIT is the default proposal, pending dependency/license review.

ROADMAP.md defines validation stages. ARCHITECTURE.md defines implementation constraints after approval. AGENTS.md preserves the documentation-only review gate.
