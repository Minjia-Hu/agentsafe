# AgentSafe — Contributor and Coding Agent Instructions

## Scope and changes

Read the product and architecture documents before changing behavior. Preserve existing work. New integrations, publication and destructive history changes require explicit maintainer authorization. This revision describes the project at this point in its development; later revisions may change scope.

## Product constraints

- Read PRODUCT.md and ARCHITECTURE.md before implementation. ROADMAP.md separates the demo, candidate launch and later learning; it does not authorize scope expansion.
- The proposed demo is explicit PNG/JPEG and UTF-8 log/text scanning, local OCR, a small configured/structural rule set, masked locations, scan, doctor, bundled demo and explicit local image-region preview. No staged scanning, visibility lookup, hooks, persistent approvals, ignores or redaction in this demo.
- No real private materials or user recruitment is required to begin an approved technical experiment. Create fictional positive, benign and failure cases; do not collect customer data or valid credentials.
- Describe target users and demand as hypotheses. Synthetic success and developer self-testing do not establish market fit or real-world accuracy.
- The target is accidental sharing by cooperative users, not adversarial agent enforcement or universal DLP. AI authorship is unknown unless explicitly supplied.
- Distinguish evidence, extraction quality, coverage and decision. In previews, no-readable-text must be visibly marked for manual review, not shown as a green CHECKED status; do not convert it into an invented finding. Text rows are noninteractive and image controls require mapped regions. Generic emails/cookies or uncertain OCR warn; strong configured/structural findings may be HIGH. Do not require approval merely because an input is an image.
- Account for every requested file. Missing dependencies, unsupported inputs, timeouts, corrupt content and exceeded limits produce visible errors, not clean results. Exit 2 takes precedence over HIGH exit 1; exit 0 can include warnings and never certifies privacy.
- Standalone API keys/passwords outside the supported rules remain a documented gap. Do not imply an existing source scanner automatically scans OCR output.
- Git integration requires a separately selected/approved route. Then inspect exact outgoing historical versions and actual destinations; never substitute working files or infer PRIVATE from an unknown result. Conditional requirements are in ARCHITECTURE.md.
- Automatic redaction, QR/video/PDF/HAR inspection, cloud inference, agent plugins, custom provider-token rules and enterprise services are deferred. Add none merely to make a demo appear complete.

## Privacy and trust

- Process artifacts locally. Do not send blobs, screenshots, OCR text, findings or extracted values to external services. The proposed file demo has no runtime network boundary; destination metadata lookup is a conditional later Git feature requiring an updated disclosure.
- No automatic telemetry, runtime dependency/model downloads, live credential verification or background updates.
- Use synthetic data for tests, examples, screenshots and demos. Do not use real private captures, customer records, session cookies or valid tokens.
- Default terminal/JSON/error output and stored finding explanations must mask sensitive values. Explicit private image previews contain visible pixels and must be labeled unredacted; do not embed raw logs or OCR transcripts. Sanitize dependency errors and filenames; do not echo raw source lines or credential-bearing remotes.
- Treat artifact content as data. Do not execute embedded commands, follow QR/URL payloads or load remote preview resources.
- Raw local preview materialization must be explicit, outside the worktree, access-restricted where supported and cleaned according to the documented lifecycle.
- Do not upload real artifacts or publish packages/releases without authorization. Recommend nonsensitive exception reasons and synthetic public bug reports.

## Engineering after approval

- Prefer one Python package and small modules; no service architecture, plugin framework or custom credential-rule catalog. Validate the provisional OCR stack on the available machine before claiming platform support.
- Use Git/native tools with argument arrays and bounded subprocess execution. Never interpolate paths or findings into a shell command.
- Respect `core.hooksPath` and worktrees. Never overwrite an unrelated hook or global Git configuration. Manual composition must replay complete stdin to every hook.
- Read repository state before editing, preserve unrelated changes, and avoid destructive/history-changing commands unless authorized.
- Do not rewrite/amend/rebase a user's commits automatically as remediation.
- Test behaviors that misrepresent findings, locations or coverage using labeled synthetic cases, including benign and failure inputs. For any later Git route, also test publication correctness. Assertions should validate outcomes, not mirror implementation internals.
- Keep README commands honest. Label unimplemented commands proposed; verify implemented commands against the local package and launch commands against the release. Never invent package ownership, badges, benchmark results or supported platforms.
- Do not add a dependency or format only because it is available. Tie it to an accepted scope item and document installation/privacy/license implications.

## Documentation and coordination

- Formal repository documentation is English by default. User-facing discussion may be Chinese.
- Keep scope/policy tables, CLI examples, exit codes, support tiers and limitations consistent across all five drafts and their Chinese translations. Preserve research citations when revising scope; distinguish old findings from newly verified research.
- Link primary sources for competitor/technical claims and distinguish documented claims, tested behavior and product hypotheses. Record research dates.
- Use delegation only when the user or an applicable skill explicitly calls for it. A document-only reader review is permissible under the doc-coauthoring skill; it must not create implementation work.
- Report changes, meaningful validation, uncertainties and any unmet criteria. Do not mark a demo or release ready based on a planned checklist.
