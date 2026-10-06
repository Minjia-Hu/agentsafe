# AgentSafe — Proposed Architecture

**Status:** Private demo implemented October 5, 2026. Conditional Git design remains unimplemented.

The current proposal is an explicit local file checker using fictional development fixtures. Git integration is a conditional later route. This replaces the earlier mandatory full Git gate architecture; its prior detail remains in Git history. Stack choices are provisional until measured.

## 1. Minimal stack

| Component | Proposal | Reason and validation |
| --- | --- | --- |
| Runtime | Python 3.11+ | Small package and local file-processing ecosystem; verify supported versions before release |
| CLI | Typer and Rich | Clear commands and terminal output; treat filenames/content as plain untrusted text |
| Image input | Pillow | Bounded PNG/JPEG decoding; validate bytes, dimensions and corrupt input |
| OCR | Tesseract via subprocess stdin/stdout TSV | Local OCR with coordinates; avoids temporary input/output files and an unnecessary wrapper dependency |
| Configuration | Standard-library TOML reader | Optional sensitive domains and session-cookie names; no policy framework |
| Verification | pytest | Labeled synthetic behavior cases; no real private data |
| Git later | Git executable via bounded subprocesses | Only if the Git release route is selected; no Git dependency for the file demo |

No cloud model, daemon, database, plugin framework or mandatory secret engine. Native OCR installation may dominate setup. Start on the available development machine; measure other platforms before claiming support. Runtime must not download models or dependencies automatically. Setup downloads are explicit and separate from scanning.

## 2. Demo flow

```text
explicit paths + optional configuration
                  |
        bounded immutable file snapshots
                  |
     PNG/JPEG decoder + OCR | UTF-8 text
                  |
       evidence with coordinates/lines
                  |
       deterministic rules and policy
                  |
       masked terminal report + exit code
```

Selection is explicit: no repository traversal, directory recursion or extension-based trust. Validate format and extension compatibility; unsupported or mismatched inputs yield visible errors. Do not follow symlinks, process devices/pipes or execute file contents. Read each regular file into a bounded byte snapshot once; extraction and rules use those bytes. Report failure if the file changes while being read; changes after the snapshot are outside the manual-check guarantee.

Keep content processing separate from terminal rendering so a later Git adapter can provide blob bytes without changing rules. This is a module boundary, not a public plugin API.

## 3. Data and decisions

Use small internal records:

- Input: display path and local snapshot digest in a transient file record. Format and byte limits are checked while processing; the selection source is always an explicit file. The digest is not an approval or a hash of an extracted private value.
- Evidence: rule/category, severity, source region or line, extraction quality and masked explanation. Raw matched values stay transient.
- Coverage: inspected, uninspected or failed, with engine/config details and a reason. No-readable-text is a visible OCR limitation within completed processing.
- Result: requested-file totals, warnings/HIGH findings, coverage and exit code. Error 2 takes precedence over HIGH 1; 0 permits warnings.

Policy is defined in PRODUCT.md. Generic emails/cookies and uncertain OCR matches warn. Strong configured-domain or populated auth/session evidence produces HIGH. An image with no finding does not require approval. A low OCR confidence value is not a calibrated security probability.

No persistent finding IDs, manifests, approvals or extraction cache in the demo. Normal scans store neither OCR transcripts nor raw input copies and open no viewers. Explicit `--preview` and `demo` may retain the normalized PNG from the same scanned snapshot, render a self-contained page and attempt to open the default browser. No original is edited or reread for preview. `--no-open` suppresses the browser launch. Minimal configuration is loaded only from an explicit `--config` path; do not silently trust repository-local policy.

## 4. Extraction and resource limits

Initial limits to measure, not achieved performance claims:

| Resource | Proposed starting bound | Behavior when exceeded |
| --- | --- | --- |
| Image file | 10 MiB / 20 megapixels | Error; no silent truncation or downsampling |
| UTF-8 text | 5 MiB | Error; no prefix-only clean result |
| OCR | 10 seconds per image | Terminate bounded subprocess; report failed coverage |
| One invocation | 20 explicit files / 60 seconds | Report unprocessed inputs and exit 2 |

Coordinates refer to source pixels. The demo explicitly rejects EXIF-rotated and animated images instead of reporting misleading coordinates or inspecting only one frame. Transparent pixels are rendered on white; hidden content/metadata is outside coverage. Text also has a 100,000-line and 32,768-character-per-line limit, with at most 200 findings per file; exceeding a limit fails inspection. The 60-second invocation limit is checked between processing stages and bounds each OCR subprocess; it is a cooperative budget, not an OS sandbox for native decoders or blocked filesystem reads. No image rotation is performed. Initially declare the tested OCR language data, rather than assuming all languages work. Bound decoder behavior before full allocation and sanitize dependency diagnostics.

Domain matches must use exact host/subdomain boundaries, not substrings. Treat localhost/test identifiers as nonsensitive unless explicitly configured. Recognize populated HTTP auth and cookie fields in text; a mention of a header without a value is not evidence. Only configured sensitive cookie names become HIGH. The same declared rules may operate on OCR text, with extraction uncertainty retained; do not advertise complete screenshot credential scanning.

Placeholder suppression must not suppress intentionally configured fictional sensitive domains. Use reserved domains and fabricated nonvalid auth values for fixtures, with positive/benign expectations recorded. Arbitrary provider API keys/passwords are outside the rule set. A future mature secret-engine adapter must receive OCR text explicitly; a separate source scanner does not cover it automatically.

## 5. Local processing and output safety

Runtime scanning has no network operations: no visibility lookup, telemetry, update check, credential verification or URL fetching. Installation is a separate documented operation. Never execute embedded content or inspect beyond explicitly selected files.

Use subprocess argument arrays and timeouts. Pillow validates and normalizes image pixels in memory; the Tesseract process receives PNG bytes on stdin and returns TSV on stdout. No raw image or OCR temporary file is created by this pipeline. Never forward raw OCR output/stderr to logs. Tesseract may be found on PATH, in the standard macOS Homebrew locations, or at the explicit AGENTSAFE_TESSERACT executable path. An invalid explicit override fails rather than silently falling back. See its [CLI documentation](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Mask matched values in every normal/error message. Disable Rich markup interpretation for untrusted strings and sanitize terminal control characters. Do not forward decoder/OCR stderr verbatim. Filenames can disclose context even after escaping; keep output local and tell users to review reports before sharing them.

There is no redaction guarantee. Coordinates identify where to inspect; users edit originals with existing tools and rerun the scan. No automatic commit/history changes.

### Explicit preview storage

`preview.py` embeds normalized visible pixels as PNG data URLs with SVG rectangles in a single HTML file. Only fixed packaged CSS/JavaScript executes; the Content Security Policy blocks connections and external resources and permits the fixed script by hash. Untrusted filenames/reasons are escaped. Region bounds are checked against the snapshot dimensions. Raw logs and OCR text are not embedded. Render text findings as compact static rows. Show region controls only for mapped boxes. A completed image extraction with no readable text renders an amber manual-review status and one limitation message before other notes, with a separate group count. This is presentation derived from the scan report; severity, coverage and exit semantics are unchanged.

Store sessions outside Git repositories under the OS temporary directory, with POSIX 700 directories and 600 files. Reject a symlink or unowned storage root. Cleanup occurs on later preview creation for owned, unchanged-layout sessions older than 24 hours, with no background task; preserve sessions with extra files or an unrecognized marker. Document manual removal and the fact the page contains unredacted pixels. Windows ACL behavior remains unverified. Cap normalized image bytes at 24 MiB per page; failure is explicit exit 2.

`demo.py` loads bundled synthetic assets and their policy using package resources, never implicit repository/user config. It produces three real scan reports rather than hard-coded findings. Demo completion and scan privacy decisions have distinct documented exit semantics.

## 6. Proposed repository structure

The following modules and synthetic examples now exist. Failure fixtures are created in pytest temporary directories; there is no persistent private-data corpus.

```text
agentsafe/
├── README.md / README.zh-CN.md
├── PRODUCT.md / PRODUCT.zh-CN.md
├── ROADMAP.md / ROADMAP.zh-CN.md
├── ARCHITECTURE.md / ARCHITECTURE.zh-CN.md
├── AGENTS.md / AGENTS.zh-CN.md
├── .gitignore
├── pyproject.toml                  # Local demo installation
├── src/agentsafe/
│   ├── cli.py                     # scan, doctor and demo
│   ├── demo.py                    # Bundled case orchestration
│   ├── preview.py                 # Explicit private HTML/SVG review
│   ├── ui/                        # Self-contained CSS and JavaScript
│   ├── demo_assets/               # Packaged fictional inputs and policy
│   ├── inputs.py                  # Bounded snapshots and classification
│   ├── extract.py                 # Text and local OCR
│   ├── rules.py                   # Small evidence rules
│   ├── scan.py                    # Coverage and per-invocation orchestration
│   ├── models.py                  # Input, evidence, coverage, result
│   ├── config.py                  # Explicit sensitivity configuration
│   └── output.py                  # Masked terminal rendering
├── examples/synthetic/            # Fictional demo inputs and policy
└── tests/
    └── test_*.py                  # Behavior tests
```

Do not create empty architecture modules or an integration framework for future features. Combine small modules if that improves clarity. Packaging ownership, executable naming and license must be resolved before distribution, not invented in installation instructions.

## 7. Demo verification

Check declared outcomes rather than implementation details:

- Positive domain/auth cases, public/example email cases, ordinary cookies, placeholders, empty headers and domain-boundary spoofing.
- Locations on original coordinates/lines, readable versus small/blurred text, and empty OCR output with visible limitations.
- Missing OCR, invalid config, unreadable/missing/unsupported inputs, symlinks, corrupt images, invalid UTF-8 and resource/time limits; no skipped input becomes success.
- No raw matched values in terminal/errors/subprocess diagnostics; hostile filenames do not become terminal commands or markup.
- Runtime performs no external content transfer; originals remain byte-for-byte unchanged.
- Installation and documented commands on a named machine; record actual timings and misses. Include a small held-out layout/font set, without claiming statistical generalization.

A usable synthetic demo permits a user review and later feedback. It does not establish market demand or release readiness.

## 8. Conditional Git route: requirements before promising push protection

This section is a later design constraint, not demo implementation work. Revisit after actual workflow evidence and explicit scope approval. Git's [pre-push interface](https://git-scm.com/docs/githooks) and [reachability traversal](https://git-scm.com/docs/git-rev-list) are primary references.

- Consume every pre-push ref record and use the actual push destination, including direct URLs and multiple remotes. Staged preview reads index blobs; the gate reads committed blobs, never worktree substitutes.
- Enumerate relevant artifact versions across outgoing history, including add-then-delete, later redaction, merges, renames, tags and force pushes. A final-tree diff is insufficient. Deduplicate extraction without losing path/commit context.
- Bound a new branch using trustworthy state from the actual destination when available; a new ref is not necessarily a first repository push. Full traversal is a conservative fallback. Missing objects/shallow history/incomplete scope must be errors, not clean results.
- Distinguish verified PUBLIC/PRIVATE/INTERNAL from UNKNOWN. Failed metadata lookup never proves private. UNKNOWN uses public policy; unresolved destination identity is a separate error. GitHub metadata lookup would be a newly disclosed network boundary with no artifact uploads.
- Strong findings may block public/unknown pushes; ordinary emails/images do not automatically require approval. Inspection failures remain errors. Reconfirm private-destination behavior when the Git route is designed; do not infer a product policy from current private repository hosting.
- If exceptions are needed, bind exact bytes, path, destination and relevant rules/policy. Changes invalidate approval; no blanket trust of a filename. Errors cannot be converted to successful scans by approval. Agent self-approval is not verified human review.
- Honor worktrees and core.hooksPath. Never overwrite an unrelated hook or install into shared/global hook locations automatically. Manual composition must replay all stdin to every hook. Uninstall removes only owned, unchanged components.
- Test first/new-ref and multi-ref pushes, actual destination, deleted historical versions, force/merge/tag scenarios, Git object formats, hook conflicts, errors and any approval invalidation.
- API uploads, attachments, release assets, CI, LFS payload transfers, unprotected repositories and later visibility changes remain outside a local pre-push guarantee. Do not fetch unsupported payloads or imply privacy certification.

Do not build these modules before the route is selected. If independent users prefer a manual sharing check, ship that boundary honestly instead.
