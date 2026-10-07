# AgentSafe — Roadmap

**Status:** Private scanner/static viewer complete; GUI workflow implemented October 6, 2026 for local review. Configured business terms and masked log preview added October 7, 2026. Integration/publication remains conditional.

This roadmap uses fictional development fixtures. Product demand and the appropriate publishing channel remain unknown. PRODUCT.md is the current scope; the earlier full Git gate is a conditional route, not a demo prerequisite.

## Phase 1 — Private technical demo

### Entry

No interviews, private screenshots, real credentials, public repository or final branding are required. The existing private repository is sufficient.

### Build only the experiment

1. Create fictional PNG/JPEG screenshots and UTF-8 `.log`/`.txt` inputs, with labels for expected findings and decisions. Include benign and failure cases, not just dramatic positives.
2. Check local OCR quality on readable and small-font screenshots; record the actual setup on the developer's reference machine. Reconsider the provisional OCR dependency if setup or quality defeats the small experiment.
3. Implement explicit-file `scan`, minimal sensitivity configuration and `doctor`, with locations, masked terminal output and clear coverage/errors.
4. Demonstrate scan → review the original → edit → rescan.
5. Record hits, misses, unwanted HIGH findings, warnings, runtime and setup steps. Keep a small set of layout/font variants separate from initial rule tuning.

### usability follow-up

The approved next iteration adds bundled `demo` and explicit local image-region preview, with English/Chinese pages, local-file lifecycle and unchanged originals. Review the three page groups with `.venv/bin/agentsafe demo`; confirm whether the marked positions and reasons are understandable before adding integrations. This does not authorize automatic redaction or publication.

The next UI revision implements compact static log rows, translated OCR notes, controls only for existing regions and a manual-review status for no readable text. No new integration scope is implied.

### GUI milestone — October 6, 2026

Implemented: file selection/drop and removal, session domains/cookie names, local asynchronous scanning, image regions/static masked log rows, supported-rule/no-text/error states, sample buttons, re-selection/rescan, clear/end session and a Mac development launcher. No new detector formats or publishing integration.

Acceptance: a new user in the prepared workspace can double-click the launcher, try a fictional sample, select files, enter context, understand findings/limitations, then reselect a reviewed copy and scan again. Failures/local authentication are tested and the main file-picker scan/rescan flow has been exercised in the browser; detailed evidence and remaining UI gaps are in README. The native launcher uses a prepared development runtime snapshot and existing Python/OCR, so this does not fulfill clean-machine distribution yet. Broader usability review remains pending.

Before v0.1 launch, choose/package the runtime and OCR, test first-run setup on clean machines and confirm a nontechnical user can complete the workflow without terminal setup. Keep the existing scanner rather than introducing a second detection engine for GUI use.

### context iteration — October 7, 2026

Implemented in the shared GUI/CLI core, with clearer automatic-versus-optional checks, masked phrase locations, strict configuration/finding limits and a fourth fictional GUI business sample. Acceptance: try the sample without domains; select the same files with supplied terms, inspect image boxes/log lines, change the terms and rescan. Chinese text is demonstrated only in logs; no image OCR language expansion. Validation is recorded in README, broader usability review pending.

Next sequence: complete this context review, then prioritize independent installation and a designed manual image-region redaction / Save a copy / recheck workflow for a candidate v0.1. That export workflow is a proposed milestone, unimplemented in this batch; preserve originals and validate actual output bytes before promising redaction. Broad semantic detection, additional formats and Git automation remain later choices. Do not postpone all useful core improvements until post-launch, and do not turn this iteration into an unlimited scanner.

### masked log preview — October 7, 2026

Implemented: bounded excerpts of finding lines, original numbers/field names, hidden detector/auth/cookie values and clickable line highlight/focus in the shared GUI/static renderer. Preserve originals, never expose raw logs or offer a sanitized export. Acceptance: try Before review, click its auth and cookie findings, verify corresponding masked lines; compare After review and the business-term sample. Privacy/location/coverage tests and browser evidence are recorded in README. This improves review, not detection scope or launch readiness.

### Scanner review gate

- The documented command runs on a named machine; no claimed universal platform support.
- Declared supported positive cases are located; designated benign cases do not produce HIGH findings. Warnings are measured separately.
- Unsupported files, missing OCR, corrupt input and time/resource limits produce explicit coverage failures and exit 2.
- Default and error output do not expose raw matched values; runtime scanning sends no input or extracted content to the network.
- Users can understand what to inspect and what the result does not cover.

Do not add staged scanning, Git visibility, hooks, persistent approvals, redaction or additional formats to rescue an unclear demo. If basic OCR/rules remain unhelpful, revise or stop within the small scope.

### Evidence limit

Successful synthetic cases establish a technical demonstration. They do not establish real-world accuracy, market demand, prevented incidents or repeat use. Self-testing supplies one person's usability observations only.

## Phase 2 — Feedback and candidate v0.1 public launch

### Feedback before integration investment

Use the working demo to seek concrete workflow feedback when people become reachable. Initially about 3–5 participants is a practical learning sample, not a statistical gate or a condition for starting Phase 1. A description of a recent sharing event is sufficient; do not request private files.

Ask what was shared, what was removed, the publication route, existing alternatives and whether the person would use the check on another actual occasion. Separate actual use from praise. No automatic outreach or publication is authorized by this roadmap.

If users cannot be reached or feedback is purely hypothetical, record demand as unknown. Keep the demo private or request authorization to share it explicitly as an experiment; do not treat a public experiment as evidence of a validated product. Avoid expanding integration work while this remains unresolved.

### Choose one release route

| Observed need | Candidate scope |
| --- | --- |
| Useful explicit screenshot/log review across sharing channels | Harden the standalone local checker; preserve the manual-check boundary |
| Repeated relevant Git pushes and a desire for automatic checking | Propose a Git gate addition and seek scope approval; implement the full Git correctness requirements in ARCHITECTURE.md |
| Interest only in source-code credentials | Refer to established scanners; reassess incremental value |
| No recurring job or too much review burden | Retain a bounded experiment, simplify or pause expansion |

The default candidate is the standalone checker. A Git route is not a promise until selected and authorized. JSON output, broader configuration or integration commands need a concrete use case, not a launch checklist slot.

### Launch readiness

- Select the product name and license; verify distribution ownership and dependency/license compatibility. MIT is still a proposal.
- Test installation and the README workflow on clean machines for each claimed supported platform. Target macOS/Linux first; label Windows experimental until equivalently tested.
- Publish declared rule/format coverage, limits, misses and measured timings on named hardware. Do not turn curated fixture metrics into general accuracy claims.
- Show a real recording of a synthetic run and label the synthetic data. Explain the selected publication boundary in the README first screen.
- For a Git route only: verify outgoing history, actual destination, unknown visibility, hook coexistence, safe exception scope and error handling before claiming push protection.
- Obtain explicit authorization for making the repository public and for any package/release publication. Demo approval does not authorize either.

Do not require unsupported 95%/90% accuracy claims, arbitrary interview totals or a 3-of-5 retention threshold. Report observed counts and qualitative evidence; product value remains a hypothesis until repeated independent use supports it.

## Phase 3 — Post-launch learning

Prioritize improvements supported by actual repeated use:

1. Reduce unwanted warnings/HIGH decisions and improve setup, locations and failure explanations.
2. If standalone API keys in screenshots are a demonstrated need, route extracted text to one mature local secret engine and validate masked output. Do not create a provider-rule catalog.
3. Add one publishing integration only after documenting its real channel and limits. A Git hook does not cover API uploads, attachments, release assets or every agent-created repository.
4. Evaluate the proposed manual export workflow before launch; after launch refine it from actual use. Verify resulting bytes and state that old Git versions remain unchanged. Automatic semantic redaction is not implied.
5. Add formats/languages/platforms one at a time with their own labeled cases and installation/resource measurements.

No enterprise service, cloud inference or universal egress enforcement is committed. If actual use stays sporadic or users repeatedly bypass the workflow, simplify or stop rather than accumulating features.

## Current next action

Try **Customer / project names** in the [interactive local GUI](README.md) using the Mac development launcher. Then select the bundled business files, enter the sample phrases and compare with empty settings. Complete sample → select/context → scan → review → reselect edited file → rescan, and record where first-time use is confusing. Then address usability and clean-machine packaging, before broader integration. No real materials or recruited users are required for this review. Synthetic success alone does not advance the project to public launch.
