# AgentSafe — Product Definition

[中文](PRODUCT.zh-CN.md)

**Status:** Experimental source Alpha, version `0.1.0a1`. The local GUI/CLI and manual PNG-copy workflow are implemented. Git integration and automatic redaction are not implemented.
**Research date:** October 5, 2026. Competitor research below has not been re-evaluated in this revision.
**Working name:** AgentSafe; naming clearance and package-name ownership remain unresolved. Source installation uses this repository, not a package named `agentsafe` on PyPI.

<a id="second-pass-review--october-5-2026"></a>

## Current experience

Check screenshots and debugging logs locally before sharing. The browser GUI is the primary interactive interface; the CLI uses the same scanning core. Select PNG/JPEG screenshots or UTF-8 `.log`/`.txt` files, optionally enter sensitive phrases, domains or session-cookie names, then inspect findings and coverage. Bundled fictional samples require no private material.

- Images: click mapped findings, review the whole image, optionally select detected boxes or draw rectangles, create an opaque PNG copy, recheck that exact copy with the original policy, and explicitly save it. Originals remain unchanged. The new report covers only the new image.
- Logs: click a finding to locate its bounded, masked excerpt. Edit the original with an existing editor, reselect the updated file and scan again. There is no raw-log reveal or log export.
- Uncertainty: ordinary emails/cookies and uncertain OCR warn. No readable image text calls for manual review. Zero findings never certify privacy.

Sensitive phrases are explicit literal context, not automatic business classification. They match within one extracted line, case-insensitively with flexible spacing and ASCII word edges. Up to 100 phrases of 2–128 characters are accepted. Chinese phrases work in UTF-8 text; image OCR remains English. Context is optional and lasts only for the session. Normal explanations hide matched values; explicitly displayed image pixels remain visible.

The GUI connects only to an authenticated local process. The A monogram is the default application/favicon identity. Source installation requires Python and Tesseract; the optional Mac development launcher depends on a prepared local runtime and is not a standalone installer. See [validation](docs/VALIDATION.md) for tested environments and remaining gaps.

## 1. Product direction

> Check screenshots and debugging logs locally before you share them.

> Don't accidentally publish what your AI agent saw or generated.

AgentSafe is a small pre-publication artifact check, not a general secret scanner or a universal privacy firewall. Supported files are inspected regardless of whether a person or an AI created them; AI provenance is not inferred. GitHub issues, reports and other sharing destinations motivate the manual workflow, but the tool does not intercept any upload.

Technical feasibility is demonstrated with fictional positive, benign and failure cases. Real-world accuracy, recurring demand and adoption remain unvalidated. An OCR wrapper is easy to copy: useful evidence, understandable limits and a review process people repeatedly use must justify the tool's friction.

## 2. What is supported by evidence

Glow's PixelLeak research describes coding agents publishing internal review screenshots to adjacent public repositories. This supports the existence of the failure mode, including public artifact repositories alongside private code repositories. It is a vendor-reported investigation, not independent evidence of market size, willingness to install, or this product's effectiveness. [Primary research](https://www.glow.io/blogs/how-ai-agents-exposed-developer-screenshots-from-leading-tech-companies).

Our inference: the first audience should be people publishing visual debugging evidence, rather than everyone using an AI editor. A repository-local hook would only help in a public destination where it was installed; it would not automatically protect a new adjacent repository created by an agent.

**Publication-path limitation:** [gitshot's documented default backend](https://github.com/vipulgupta2048/gitshot#how-it-works) uploads images as GitHub Release Assets in a dedicated public repository. That upload path does not invoke the developer's local Git pre-push hook. Therefore the cited incident is evidence of artifact exposure, not evidence that this proposed hook would have prevented all or most reported cases. The share of incidents occurring through a covered Git push has not been established.

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
| Unknown visibility means private | Incorrect: authentication, network errors, aliases and unsupported providers create uncertainty | For a future Git gate, apply public policy to UNKNOWN; show the uncertainty |
| Generated artifacts are a large recurring problem for everyone | Unproven; many artifacts never enter Git | Recruit users with actual artifact publishing workflows |
| A dramatic demo demonstrates accuracy | A few staged examples say little about benign assets and OCR misses | Evaluate benign fixtures, misses, latency and repeated use |
| Cross-platform installation will take two minutes | Native OCR dependencies may dominate setup, especially on Windows | Validate setup on clean machines; do not claim a single-binary installation |
| Blocking every changed image is acceptable | Unproven; it may be excessive for asset-heavy projects | Do not require blanket image approval in the proposed experiment; measure review burden |

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

The source Alpha uses AgentSafe as a working name and identifies this exact repository as its installation source. Before registry distribution or wider branding, resolve naming and verify repository, package, executable and domain ownership. Do not tell users to install an unverified package named `agentsafe`.

## 5. Target-user hypothesis

**Hypothesized user:** a developer who shares screenshots or debugging logs outside their original context and sometimes needs to remove account information, internal URLs or authentication data. Browser-capable coding-agent users and open-source maintainers are possible recruitment pools, not verified customers.

Typical job:

> I want to show a bug or a working change without sharing sensitive context along with it.

Self-testing is the first usability observation; it is not evidence of market demand. After a working demo, seek a small convenience sample, initially about 3–5 people, through existing contacts or communities.

Ask about a recent actual sharing event, what they removed, where they posted it and what they did instead of using a scanner. A verbal account is sufficient; do not collect private files. A GitHub star, a positive reaction or a hypothetical willingness to use the tool is not repeated use. If no users can be reached, record demand as unknown and keep further investment bounded.

Exclude enterprise enforcement, adversarial-agent containment, general source-code scanning and comprehensive media inspection from the initial audience promise.

## 6. Threat model and honest boundary

The underlying threat is accidental external publication of sensitive development artifacts by cooperative developers or agents. Examples include configured internal hostnames and populated authentication headers. An email or a cookie alone does not establish confidentiality or credential validity.

The checker covers a **manual check of explicit local files**:

1. The user selects supported files in the GUI or supplies explicit CLI paths before sharing.
2. The scanner reads a bounded snapshot of each file locally.
3. It reports evidence, location, extraction uncertainty and coverage.
4. The user reviews the artifact, creates/rechecks a manually covered image copy or edits/reselects a log, and decides what to share.

There is no enforcement at the upload boundary. Changes after scanning invalidate the relevance of that scan; a filename is not an approval of later bytes. The scanner does not know the destination or whether a file will be published.

Trust the local user, configuration and installed dependencies for this accidental-leak model. Treat all file contents as untrusted parser data. Do not execute embedded commands, visit detected URLs or infer AI authorship. Missing tools, unsupported inputs and failed inspections must not become clean results.

The Alpha excludes Git/index/history inspection, destination visibility, hooks, API/attachment/CI upload interception, credential verification, arbitrary secret detection, automatic customer-name or dashboard classification, hidden metadata and adversarial bypass. OCR can miss tiny, blurred or unsupported-language text. A clean scan means no supported rule matched the inspected input, not that the artifact is safe.

If a Git gate is later selected, it must inspect all relevant outgoing versions, including files deleted or redacted in later commits, and the actual destination. A worktree scan cannot make that promise. Detailed conditional requirements are in ARCHITECTURE.md.

Auth/cookie detection accepts line-local colon/equal fields and quoted scalar keys/values. It does not interpret JSON/HAR documents, nested values, encoded keys or multiline values. Preview masking covers recognized auth/cookie fields even when their values produce no finding; ambiguous auth context falls back to a noninteractive line location.

## 7. Current Alpha scope

### Included

- Local GUI with explicit file selection, session sensitivity settings, progress, shared review rendering, fictional examples and clear/end-session controls; a Mac checkout-dependent launcher. The following CLI scope still applies to the shared core.

- Explicit paths to PNG/JPEG and UTF-8 `.log`/`.txt` files; no automatic directory crawling or provenance detection.
- Local OCR with image coordinates; direct text processing with line numbers.
- Configured sensitive-domain and literal word/phrase matching; possible email detection; populated Authorization/Proxy-Authorization fields; Cookie/Set-Cookie fields with configured sensitive session-cookie names.
- Small optional TOML configuration for sensitive domains, words/phrases and session-cookie names. Show when none are configured; do not pretend to infer organization-specific sensitivity.
- `scan`, `doctor` and a bundled one-command `demo`; opt-in `scan --preview` image-region review, masked terminal output and defined exit codes.
- Fictional positive, benign and failure fixtures; a documented manual review/edit/rescan workflow.
- GUI-only manual image covering, new opaque PNG, original-policy recheck and explicit download; originals unchanged.

### Implemented policy

| Observation | Current behavior |
| --- | --- |
| Configured sensitive domain or literal phrase with reliable extraction | HIGH finding; exit 1 unless a scan error takes precedence |
| Populated non-placeholder Authorization field or configured session cookie | HIGH structural/configured finding; does not prove the value is a valid credential |
| Generic email, unconfigured populated cookie or uncertain OCR match | WARN with location; no automatic HIGH escalation |
| Supported image inspected without a rule match | No detected finding; no mandatory image approval |
| OCR produces no readable text | Display that limitation; do not claim the image contains no sensitive context |
| Explicit unsupported file, missing file/tool, invalid encoding, corrupt image, timeout or exceeded limit | ERROR/uninspected or failed coverage; exit 2 |

Reserved example addresses and obvious placeholders should not trigger generic email/credential findings. An explicitly configured sensitive domain takes precedence over example-domain suppression, allowing fictional `.test` domains to exercise the actual rule. Synthetic auth fixtures must have nonempty structural test values that are not recognized empty/redaction placeholders; no real tokens are needed. Public email detection can be correct while a blocking decision would still be wrong.

There is no visibility-dependent policy, persistent approval, ignore/baseline mechanism or automatic remediation in this experiment. To reduce scope, the user supplies only the paths they want checked; every requested path must appear in coverage. A standalone API key or password in an image is outside the initial rules unless it matches the explicitly supported structure. Installing an existing source scanner does not automatically scan OCR text.

### Outside this Alpha

Automatic redaction, QR decoding, PDF/video inspection, HAR-specific parsing, archive/LFS extraction, JSON/CSV/report understanding, cloud inference, agent plugins, background monitoring, custom provider-token catalogs, credential validation and enterprise features are deferred. Staged scanning, Git visibility, pre-push installation, ignore patterns and approvals are also outside this Alpha; include them in a Git-focused v0.1 only if that route is selected explicitly.

## 8. CLI UX

These commands are implemented. Install from the local checkout as described in README.md; no public package is available:

```text
agentsafe demo
agentsafe doctor
agentsafe scan examples/synthetic/dashboard.png examples/synthetic/session.log --config examples/synthetic/policy.toml
```

Illustrative output; fixture names and coordinates are fictional:

```text
AgentSafe Local Artifact Check
Scope: 2 explicit local files | Processing: local

HIGH  examples/synthetic/dashboard.png
      Configured sensitive domain (OCR); region x=120 y=84 w=210 h=20
HIGH  examples/synthetic/session.log
      Populated Authorization field; line 8; value hidden

Coverage: 2 inspected, 0 uninspected, 0 failed
Result: findings require review (exit 1).
Review the indicated locations, edit if needed, and scan again before sharing.
No upload or Git push was intercepted.
```

Do not print raw tokens, matched emails, full source lines or OCR transcripts. File paths may themselves be sensitive; sanitize terminal controls and keep output local. A coordinate identifies evidence, not a redaction guarantee. Explicit `scan --preview` and `demo` create self-contained local image-region and masked-log pages, then attempt to open the default browser. The page contains visible image pixels and must be kept private; it is not a redacted export. Text log content stays masked. These static commands start no server or image editor; the separate GUI uses the authenticated loopback session above. `--no-open` saves without opening; `--lang zh` selects a Chinese page. See README for the temporary-file lifecycle.

Visual status must distinguish completed processing from readable extraction: an image with no extracted text shows “No readable text — review the image manually”, rather than a green CHECKED label. Group summaries list that limitation separately from findings. The warning does not invent a finding or change exit semantics. Log findings can locate their masked excerpt line; reports without excerpts fall back to static locations. Image controls require mapped regions. The local viewer is optional; teaching demo groups are not the everyday file-review flow.

**Exit codes:** 0 = all requested inputs inspected with no HIGH findings; warnings may exist. 1 = completed scan with HIGH findings. 2 = any setup/input/inspection failure, even when other files also have HIGH findings. Print warnings and coverage explicitly; never equate exit 0 with safe publication. These are scan outcomes, not proof a Git push was blocked. `doctor` uses 0 for ready and 2 for missing/invalid prerequisites.

`demo` scans original, prepared reviewed and known-miss fixtures from package resources; no business material is needed. Demo completion uses exit 0 even when expected HIGH findings exist; failures use 2. `scan --preview` preserves scan decisions, with preview-generation failure overriding to 2.

Default output is terminal text. Structured JSON, stable stored finding IDs, `inspect`, `allow`, `init`, `uninstall` and `redact` are not demo commands. Consider only demonstrated needs for a release.

## 9. Experiment design and stop conditions

Three separately labeled evidence levels prevent overclaiming:

| Evidence | What it can establish | What it cannot establish |
| --- | --- | --- |
| Synthetic fixtures | Rules, locations, failure behavior, output masking and installation on tested machines | Real-world accuracy, market demand or retention |
| Developer self-testing | Whether one person understands setup and results | A representative target-user workflow |
| Later independent use | Concrete publishing channels, perceived value, friction and repeated use | Broad market fit from a few participants |

The implemented experiment uses a small labeled corpus containing fictional dashboard screenshots, fictional auth logs and benign public-page/logo/documentation examples. Include readable and small/blurred text, placeholders, empty headers, ordinary cookies and public contact information. Add missing-tool, corrupt-input and unsupported-format cases. Use synthetic layouts and reserved domains; do not copy real internal pages.

Label both expected entity detection and the desired decision. Record actual hits, misses, benign HIGH findings, warnings, locations, runtime and setup steps, including failed cases. Use a small additional set of layout/font variants not used to tune the first rules. Do not report general 95% precision/90% recall claims from a curated demo. Publish counts and fixture limits if results are later shared.

A technical demo is ready for review when the documented command really runs on a named reference machine, finds its declared supported positive cases, leaves the specified benign cases free of HIGH findings, reports failures as errors, and exposes no raw values in normal/error output. The initial measured results are in [the fixture guide](examples/synthetic/README.md); a synthetic result is not a release or market claim. Fix failures within this scope; do not add formats to compensate for weak core behavior.

Then show the working result to prospective users when access becomes available. Map actual publication routes before investing in a hook. If feedback remains hypothetical or no one can describe a recurring job, keep the project a bounded experiment. If screenshot preparation is useful but Git is irrelevant, choose a standalone check. If the main need is source-code credentials, direct users to established tools.

## 10. Alpha scope and future decisions

Version `0.1.0a1` is an experimental standalone local checker distributed from source under the [MIT license](LICENSE). It is not a stable production release. Reproducible installation, honest diagnostics and clear review boundaries take priority over new formats or integrations. Publication is a maintainer release action; preparation alone does not publish anything.

A Git gate is a separate future decision. It would require outgoing-history inspection, actual destination identity, unknown-visibility handling and safe hook coexistence. Do not add it solely for launch breadth. Independent installers and further languages/formats also need separate validation.

See [ROADMAP.md](ROADMAP.md), [ARCHITECTURE.md](ARCHITECTURE.md) and the [release checklist](docs/ALPHA_RELEASE.md).
