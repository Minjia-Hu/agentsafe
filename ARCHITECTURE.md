# AgentSafe — Architecture

[中文](ARCHITECTURE.zh-CN.md)

**Status:** Experimental source Alpha `0.1.0a1`: local GUI/CLI, literal context, masked log review and manual opaque PNG copies. Conditional Git design remains unimplemented. The project uses MIT licensing; dependency notices and validated environments are documented separately.

One Python package handles explicit local snapshots. The GUI is a short-lived authenticated loopback interface, not a hosted service. Installation requires Python and Tesseract; standalone runtime packaging remains future work. See [validation](docs/VALIDATION.md) for measured support.

## 1. Minimal stack

| Component | Implementation | Reason and validation |
| --- | --- | --- |
| Runtime | Python 3.11+ | Small package and local file-processing ecosystem; verify supported versions before release |
| CLI | Typer and Rich | Clear commands and terminal output; treat filenames/content as plain untrusted text |
| Human GUI | Packaged HTML/CSS/JavaScript + standard-library loopback HTTP server | Reuse the existing review renderer/core; no new framework or cloud dependency |
| Image input | Pillow | Bounded PNG/JPEG decoding; validate bytes, dimensions and corrupt input |
| OCR | Tesseract via subprocess stdin/stdout TSV | Local OCR with coordinates; avoids temporary input/output files and an unnecessary wrapper dependency |
| Configuration | Standard-library TOML reader | Optional sensitive domains, literal terms and session-cookie names; no policy framework |
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

Policy is defined in PRODUCT.md. Generic emails/cookies and uncertain OCR matches warn. Strong configured-domain/term or populated auth/session evidence produces HIGH. An image with no finding does not require approval. A low OCR confidence value is not a calibrated security probability.

No persistent finding IDs, manifests, approvals or extraction cache in the demo. Normal scans store neither OCR transcripts nor raw input copies and open no viewers. Explicit `--preview` and `demo` may retain the normalized PNG from the same scanned snapshot, render a self-contained page and attempt to open the default browser. No original is edited or reread for preview. `--no-open` suppresses the browser launch. Minimal configuration is loaded only from an explicit `--config` path; do not silently trust repository-local policy.

## 4. Extraction and resource limits

Enforced limits; these are resource bounds, not performance claims:

| Resource | Enforced bound | Behavior when exceeded |
| --- | --- | --- |
| Image file | 10 MiB / 20 megapixels | Error; no silent truncation or downsampling |
| UTF-8 text | 5 MiB | Error; no prefix-only clean result |
| OCR | 10 seconds per image | Terminate bounded subprocess; report failed coverage |
| One invocation | 20 explicit files / 60 seconds | Report unprocessed inputs and exit 2 |

Coordinates refer to source pixels. The demo explicitly rejects EXIF-rotated and animated images instead of reporting misleading coordinates or inspecting only one frame. Transparent pixels are rendered on white; hidden content/metadata is outside coverage. Text also has a 100,000-line and 32,768-character-per-line limit, with at most 200 findings per file; exceeding a limit fails inspection. The 60-second invocation limit is checked between processing stages and bounds each OCR subprocess; it is a cooperative budget, not an OS sandbox for native decoders or blocked filesystem reads. No image rotation is performed. Initially declare the tested OCR language data, rather than assuming all languages work. Bound decoder behavior before full allocation and sanitize dependency diagnostics.

Domain matches must use exact host/subdomain boundaries, not substrings. Treat localhost/test identifiers as nonsensitive unless explicitly configured. Recognize populated HTTP auth and cookie fields in text; a mention of a header without a value is not evidence. Only configured sensitive cookie names become HIGH. The same declared rules may operate on OCR text, with extraction uncertainty retained; do not advertise complete screenshot credential scanning.

`sensitive_terms` is a bounded tuple in the same Policy. Compile escaped literal patterns once per transient policy, never into a global cache. Accept 100 single-line terms at most, 2–128 characters after trimming/collapsing ASCII spaces, reject control characters and deduplicate case-insensitively. Match case-insensitively within one Segment; spacing between phrase words may vary, with ASCII alphanumeric/underscore edges for English words. No normalization of evidence, fuzzy matches, regex syntax or multiline joins. For each match reuse the existing word-overlap box/line logic and OCR confidence downgrade. Stop at the finding budget while collecting, rather than allocating an unbounded match list. A fixed masked explanation never includes the configured term or OCR value. Chinese literals work in UTF-8 text; no new image OCR language is implied.

The GUI term input splits on line breaks only, preserving spaces/commas inside phrases. The authenticated upload carries the same `sensitive_terms` field accepted by explicit CLI TOML. Session results include only policy counts, not configured values. The business sample is packaged fictional PNG/log data plus an explicit in-memory term policy; it does not change the static demo's three groups or require a domain.

Placeholder suppression must not suppress intentionally configured fictional sensitive domains. Use reserved domains and fabricated nonvalid auth values for fixtures, with positive/benign expectations recorded. Arbitrary provider API keys/passwords are outside the rule set. A future mature secret-engine adapter must receive OCR text explicitly; a separate source scanner does not cover it automatically.

## 5. Local processing and output safety

The scanning core and CLI have no network operations: no visibility lookup, telemetry, update check, credential verification or URL fetching. The interactive GUI adds only browser-to-process IPv4 loopback communication, described below. Installation is separate. Never execute embedded content or inspect beyond explicitly selected files.

Use subprocess argument arrays and timeouts. Pillow validates and normalizes image pixels in memory; the Tesseract process receives PNG bytes on stdin and returns TSV on stdout. No raw image or OCR temporary file is created by this pipeline. Never forward raw OCR output/stderr to logs. Tesseract may be found on PATH, in the standard macOS Homebrew locations, or at the explicit AGENTSAFE_TESSERACT executable path. An invalid explicit override fails rather than silently falling back. See its [CLI documentation](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Mask matched values in every normal/error message. Disable Rich markup interpretation for untrusted strings and sanitize terminal control characters. Do not forward decoder/OCR stderr verbatim. Filenames can disclose context even after escaping; keep output local and tell users to review reports before sharing them.

There is no redaction guarantee. Coordinates identify where to inspect; the GUI can manually cover chosen regions in a new PNG and recheck it, while users edit logs with existing tools and rerun the scan. No automatic commit/history changes.

### Explicit preview storage

`preview.py` embeds normalized visible pixels as PNG data URLs with SVG rectangles in a single HTML file. Only fixed packaged CSS/JavaScript executes; the Content Security Policy blocks connections and external resources and permits the fixed script by hash. Untrusted filenames/reasons are escaped. Region bounds are checked against the snapshot dimensions. Raw logs and OCR text are not embedded. Explicit previews include the masked finding-line excerpts described below, with clickable line locations. Show region controls only for mapped boxes. A completed image extraction with no readable text renders an amber manual-review status and one limitation message before other notes, with a separate group count. This is presentation derived from the scan report; severity, coverage and exit semantics are unchanged.

Store sessions outside Git repositories under the OS temporary directory, with POSIX 700 directories and 600 files. Reject a symlink or unowned storage root. Cleanup occurs on later preview creation for owned, unchanged-layout sessions older than 24 hours, with no background task; preserve sessions with extra files or an unrecognized marker. Document manual removal and the fact the page contains unredacted pixels. Windows ACL behavior remains unverified. Cap normalized image bytes at 24 MiB per page; failure is explicit exit 2.

`demo.py` loads bundled synthetic assets and their policy using package resources, never implicit repository/user config. It produces three real scan reports rather than hard-coded findings. Demo completion and scan privacy decisions have distinct documented exit semantics.

### Masked finding-line context

`text_preview.py` builds excerpts only after the full supported text inspection succeeds and only when preview capture is explicit (`scan_buffers`, `scan --preview`, `demo`). Normal CLI scans retain no excerpt. Findings carry source character masking spans, never matched values; the rules share their Authorization/Cookie parser with preview masking. Preserve header/cookie names, hide auth values and all cookie values on retained lines, including placeholders, unparsed cookie parts and unnecessary Set-Cookie attribute tails. Merge overlapping detector spans to hide terms, domains and emails before constructing snippets.

Only finding lines are retained. Merge windows with up to 48 source characters on each side of masking spans, use ellipses for omitted context, and cap each file's UTF-8 excerpt text at 64 KiB. An exceeded preview limit is explicit failed coverage/exit 2, with no partial findings or excerpts retained. Existing input/line/finding limits still apply. Masked excerpt records are excluded from repr; terminal rendering ignores them. HTML escapes text/control characters and never turns a URL into a link. Line buttons use scoped IDs, keyboard activation and visible focus/highlight; no excerpt means no clickable target. Never retain an OCR transcript or reread an original for review.

This limited masking is not a complete sanitizer: unsupported secrets or private context can remain. Keep previews private. GUI excerpts live only in the latest in-memory result; explicit static previews embed them under the existing private temporary-page lifecycle. Neither workflow creates a sanitized log file or edits the original.

### Interactive GUI session

`gui.py` starts a short-lived server bound only to `127.0.0.1` at an OS-selected port. It serves an allowlist of packaged UI assets, never arbitrary paths. The launcher passes a random session token in the URL fragment, so it is not sent in HTTP paths/logs; the UI removes the fragment and stores only that token in tab session storage for refresh. All API reads/actions require the token in a custom header. Validate exact Host, any supplied Origin and cross-site fetch metadata; grant no CORS. Responses use no-store, no-referrer, nosniff and a CSP limited to local scripts/styles/connections and embedded PNGs, with framing disabled. Access logging is disabled.

File selection submits a bounded binary frame: four-byte metadata length, at most 64 KiB of JSON metadata (names, byte sizes, session policy/language), followed by explicit file bytes. Names cannot be paths or URLs. Reject malformed/trailing/missing data, more than 20 files or over 24 MiB total before starting. Only one upload/scan reservation is allowed per session. HTTP reads time out after 15 seconds. The existing engine applies per-file type/size, decoding, OCR and findings/time bounds; every accepted file appears in coverage. This cooperative native-parser budget is not an OS memory sandbox.

`scan_buffers` and `scan_files` share one orchestrator. A worker scans without blocking the UI; polling reports the current file/count, not a claimed precise overall percentage. `preview.render_cards` supplies escaped masked results and normalized visible-image regions. Only masked finding-line excerpts may enter result HTML, never raw logs/OCR transcripts. Failed inspection takes precedence in summaries. No-readable-text remains manual review, not a finding or privacy pass.

Raw snapshots remain in worker memory and are released after processing. The session keeps the latest masked card HTML (including masked log excerpts and explicitly selected visible image pixels), normalized image sources and the original policy for manual copies, plus exact exported PNG bytes when a copy was created, cleared on replacement, Clear results, End session, process exit or 30 minutes without requests. There is no artifact spool, database or report file. Browser/OS persistence is outside the promise; a same-user malicious process or browser extension is not prevented. A browser File is a selected snapshot: edits require re-selection. Settings/selection changes mark prior results stale. The existing static-preview disk lifecycle is separate.

`AgentSafe.app` is a small native Mac development launcher, built by `scripts/build_macos_launcher.py` from `macos_launcher.m` using existing Apple clang/AppKit. The ignored native binary contains paths to an owned private OS-temp runtime snapshot and the existing base Python. The build copies current package code and installed environment dependencies, never scan inputs. It starts Python with `-S` and that snapshot on PYTHONPATH, without shell evaluation, Desktop checkout access or automatic installation/downloads. Rebuild after source/dependency changes or temp-runtime removal. It opens the default browser in Chinese. This unsigned development setup still depends on the existing base Python/Tesseract; it is not a distributable standalone app. Signed/notarized runtime/OCR bundles and Windows/Linux launchers require separate launch validation.

### Manual PNG copy boundary

`redaction.py` accepts only a normalized in-memory PNG from the latest completed scan and 1–100 integer rectangles within its dimensions. `POST /api/redact` requires the session token, a current random `review_id`, an integer image index and bounded JSON (64 KiB); it has no filesystem path or URL input. Stale reviews, log indices, malformed rectangles and busy sessions are rejected. The reservation covers generation and rescan.

The editor selects boxes with a clamped 4 px margin or arbitrary user rectangles. SVG screen-transform inversion preserves source-pixel coordinates when the display scales/letterboxes; previews are overlays, not the exported file. The server creates a fresh RGB image, fills inclusive integer pixel regions with opaque `(23, 63, 57)`, omits source metadata and bounds the output to 10 MiB / 20 MP. Originals are never reopened or written. The exact new PNG bytes go to `scan_buffers` with the retained original policy. The one-image result exposes a data URL and new `*-redacted.png` download name for those same bytes. Download is an explicit browser action, not a server spool. Failed coverage remains visible; no readable text is not a pass. PNG output can still contain unknown private content outside the chosen areas.

Latest image/policy/export state is released on new scans, clear, end, idle expiry or process exit; user downloads have their own lifecycle. No pixel selection/policy is stored in browser storage. A same-session stale page cannot silently edit a newer scan. Static previews and logs remain read-only.

### Browser identity assets

The local asset allowlist includes `/brand`, three original SVG icons, 32/180 px PNGs and multi-size ICOs, including `/favicon.ico` fallback. `scripts/build_icons.py` creates the geometric designs without remote assets/fonts; package data includes the icon subdirectory. The comparison page switches only its own favicon and uses no stored preference or artifact input. The app uses the A monogram (01) in its header and favicon links; `/favicon.ico` serves that same design. CSP allows same-origin icon images plus existing PNG data URLs, not external image resources.

## 6. Repository structure

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
│   ├── cli.py                     # scan, doctor, demo and gui
│   ├── gui.py                     # Authenticated in-memory loopback UI session
│   ├── demo.py                    # Bundled case orchestration
│   ├── preview.py                 # Explicit private HTML/SVG review
│   ├── ui/                        # Self-contained CSS and JavaScript
│   ├── demo_assets/               # Packaged fictional inputs and policy
│   ├── inputs.py                  # Bounded snapshots and classification
│   ├── extract.py                 # Text and local OCR
│   ├── rules.py                   # Small evidence rules
│   ├── text_preview.py            # Masked finding-line excerpts
│   ├── redaction.py               # Bounded opaque PNG copies, no paths
│   ├── scan.py                    # Coverage and per-invocation orchestration
│   ├── models.py                  # Input, evidence, coverage, result
│   ├── config.py                  # Explicit sensitivity configuration
│   └── output.py                  # Masked terminal rendering
├── AgentSafe.app/                 # Mac development launcher; binary ignored
├── scripts/                      # Native launcher source and local build
├── examples/synthetic/            # Fictional demo inputs and policy
└── tests/
    └── test_*.py                  # Behavior tests
```

Do not create empty architecture modules or an integration framework for future features. Combine small modules if that improves clarity. Packaging ownership, executable naming and license must be resolved before distribution, not invented in installation instructions.

## 7. Demo verification

Check declared outcomes rather than implementation details:

- Positive domain/auth/phrase cases, literal regex-like/punctuation and Chinese text, English word-edge negatives, masked invalid policy and phrase boxes with uncertain OCR; public/example email cases, ordinary cookies, placeholders, empty headers and domain-boundary spoofing.
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
