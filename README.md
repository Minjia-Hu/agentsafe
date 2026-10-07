# AgentSafe

[中文](README.zh-CN.md)

### Don't accidentally publish what your AI agent saw or generated.

**Check screenshots and debugging logs locally before you share them.**

This private experimental local app checks screenshots and logs for configured private names/phrases, internal domains and populated authentication fields. Use the browser GUI to choose files, optionally add context, scan and review image locations or clickable masked log excerpts. The CLI uses the same core for technical users and agents.

**In this prepared Mac workspace, double-click `AgentSafe.app` in Finder.** Everyday review requires no terminal commands. The development launcher uses a private runtime snapshot prepared from this checkout's environment, plus the existing Python interpreter and Tesseract. It is not a standalone installer.

Choose files → optionally add private names or domains → check → review → edit with your usual tools → choose updated files → check again. No files yet? Try **Customer / project names**, **Before review**, **After review** and **Known OCR miss** in the app.

![Actual local GUI checking fictional customer and project names](docs/images/gui-preview.png)

Abbreviated output from the included fictional demo:

```text
HIGH     examples/synthetic/dashboard.png
  WARN  Configured sensitive domain; value hidden
        region x=122 y=308 w=456 h=24 (source pixels); uncertain OCR extraction
  HIGH  Email uses a configured sensitive domain; value hidden
        region x=171 y=376 w=229 h=24 (source pixels)

HIGH     examples/synthetic/session.log
  HIGH  Populated Authorization field; value hidden (validity not checked)
        line 8

Coverage: 2 inspected, 0 uninspected, 0 failed
Findings: 4 HIGH, 2 WARN | Exit: 1
```

**Private technical demo, not a public release.** The working name and public distribution remain unresolved. No real business artifacts were needed: the examples are fictional, and the reviewed copies were prepared separately rather than produced by automatic redaction. Demand and real-world accuracy remain unvalidated.

For the new interactive GUI from a prepared checkout:

```sh
.venv/bin/agentsafe gui --lang en
```

It opens your default browser. The Mac development launcher opens the Chinese UI. Standalone packaging and clean-machine installation remain future launch work.

To rebuild the Mac development launcher after source/dependency changes, run this once from the prepared environment (Apple Command Line Tools/clang required):

```sh
.venv/bin/python scripts/build_macos_launcher.py
```

The native launcher binary is a local ignored build artifact; app metadata and build sources are tracked. The build copies installed dependencies and current package code to a private OS-temp runtime snapshot; it copies no user scan inputs and downloads nothing. It does not need to read the Desktop checkout during launch. Rebuild if the OS removes that runtime snapshot or the base Python path changes. This development arrangement is not clean-machine distribution.

For the original static visual demo, run:

```sh
.venv/bin/agentsafe demo
```

This scans bundled fictional inputs and opens a local page with image finding regions, reviewed counterparts and a known OCR miss.

## Interactive local GUI

Use a browser file picker or drag/drop, a removable file list, optional sensitive-word/phrase, internal-domain and session-cookie-name fields, asynchronous scan progress, masked results and image-region highlighting. Fictional samples, **Clear results** and **End session** are available. Formats are PNG/JPEG and UTF-8 `.log`/`.txt`. Maximum selection: 20 files and 24 MiB total; the existing 10 MiB image / 5 MiB text and decoder/OCR limits also apply. Unsupported files and errors remain visible. Directories are not scanned.

For the new feature, click **Customer / project names**; no files or settings are required. This sample checks fictional names without configuring a domain. On the reference Mac it finds two image regions and three log lines (5 HIGH / 0 WARN). Original/reviewed/OCR-miss samples still use their own preset policies.

For your own files, both main settings can be empty; general email/authentication/cookie rules still run. **Sensitive words / phrases** accepts customer names, project names or exact phrases, one per line, such as `Project Cedar` and `Acme Training`. **Internal domains** accepts only domain names, such as `northstar.test` for the original sample; it also matches subdomains and emails on them. The sample buttons use their disclosed preset context; the **Check selected files** button uses the fields you entered. Settings are not saved between sessions.

Browser selections are snapshots. **After editing an original, reselect the updated file** before scanning again. Changing the selection/settings marks the displayed result as a previous scan. Zero findings do not establish safety; no-readable-text images require manual review.

Logs now have a **masked preview**. Try **Before review**, scroll to `session.log`, and click an authentication/cookie finding to highlight its line. Names such as `Authorization` and `demo_session` remain visible, while values and detected terms/domains/emails become `[HIDDEN]` (`[隐藏]` in Chinese). Only finding lines and short surrounding context are retained; ellipses indicate omitted text. No findings means no excerpt. Full content remains in your original file. This does not produce a sanitized log for sharing: unsupported secrets or private context may still remain. [Actual fictional log-review screenshot](docs/images/gui-log-preview.png).

`gui` binds only to `127.0.0.1` on a random port. File bytes travel from the browser to the process on this computer, never to an external service. Every API action requires a random session token; exact Host/Origin checks and no CORS grants protect the local boundary. Only fixed app assets are served, not filesystem paths. No telemetry, external resources or runtime downloads.

Raw snapshots/OCR are transient in memory. The latest masked result, including log excerpts and normalized visible image pixels, stays in memory until cleared, replaced, the session ends, the process exits or 30 minutes without requests. AgentSafe writes no report file/database. Browsers may maintain their own memory/cache; this is not a browser/OS persistence guarantee. Tab session storage keeps only the random connection token for refresh, never artifacts or policy. Closing the tab does not immediately stop the process: use **End session** for explicit cleanup.

The original `demo` / `scan --preview` commands still generate static temporary HTML with the separate lifecycle below. The GUI does not generate those files. Its visible images are unredacted; it does not edit originals or intercept uploads/Git pushes.

## Run the local demo

Requirements: Python 3.11+ and Tesseract with English (`eng`) data. This run was tested on macOS 26.5.1 arm64, Python 3.12.12 and Tesseract 5.5.2. Linux/Windows installation has not been verified.

From this checkout, create an environment with an available Python 3.12 interpreter and install the local project:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install '.[dev]'
```

Install the native OCR dependency separately. On macOS with Homebrew:

```sh
brew install tesseract
```

Tesseract is discovered on PATH and, on macOS, in standard Homebrew locations. No environment variable is needed on this workspace. To override discovery explicitly:

```sh
export AGENTSAFE_TESSERACT=/opt/homebrew/bin/tesseract
```

The environment and OCR dependency are already prepared in this workspace. Run:

```sh
.venv/bin/agentsafe doctor --config examples/synthetic/policy.toml
.venv/bin/agentsafe scan examples/synthetic/dashboard.png examples/synthetic/session.log --config examples/synthetic/policy.toml
```

The scan intentionally returns **1**, because the fictional originals contain supported risk signals. Then compare the manually reviewed versions:

```sh
.venv/bin/agentsafe scan examples/synthetic/dashboard-reviewed.png examples/synthetic/session-reviewed.log --config examples/synthetic/policy.toml
```

This returns **0**, with one warning for a preference cookie. Open the originals in your local viewer/editor, inspect the indicated region or line, make your own changes and rescan. AgentSafe never edits them.

Use `--` before filenames beginning with a dash. No directory traversal is performed. Do not install an unrelated public package named `agentsafe`; the only installation described here is from this local checkout. Ordinary installation is used because this machine skips hidden editable-install `.pth` files; reinstall the local package after source changes when checking the installed CLI.

## Visual review

```sh
.venv/bin/agentsafe demo
.venv/bin/agentsafe scan examples/synthetic/dashboard.png --config examples/synthetic/policy.toml --preview
```

`demo` includes its fictional images, logs and policy in the installed package; it works outside the checkout. It scans three groups: original inputs, separately prepared reviewed copies, and the known small/blurred OCR miss. Select a tab, click an image finding to highlight its region, or hide the overlays to see the unchanged image. Log findings show masked finding-line excerpts; click a reason to highlight its original line number. No raw log is embedded. Region controls appear only when mapped boxes exist. Images with no readable OCR text use an amber manual-review status and a separate group summary; this does not add WARN/HIGH findings or change scan exit codes. Chinese pages translate the OCR guidance and show the no-text limitation once. Reviewed copies are not generated by automatic redaction.

Use `--lang zh` for a Chinese page (ordinary `scan` terminal output stays English). `--no-open` generates the page without launching a browser. Otherwise the command attempts to open the local HTML file in your default browser; if opening fails, open the printed path manually. Missing OCR still yields explicit errors. `demo` returns 0 when all bundled scans and preview generation complete, even though the original group has HIGH findings; 2 means incomplete inspection or preview generation. `scan --preview` keeps normal scan exit codes, with preview-generation failures returning 2.

**The preview contains visible image pixels, not a redacted export.** It uses the normalized image snapshot that was scanned, with SVG overlays; it never rereads or edits the original. Only bounded masked excerpts of log finding lines are embedded, never raw logs or OCR transcripts. No server, external scripts, fonts or network requests are required. Images and unmatched log context may disclose private information: keep your previews private.

Pages are saved under the OS temporary directory in `agentsafe-previews-<user>/`, outside Git repositories. On POSIX, directories use mode 700 and files 600; Windows permission behavior is not yet verified. Unmodified session layouts older than 24 hours are eligible for cleanup when the next preview is generated; there is no background deletion. Delete your page/session directory manually when finished if needed. There is a 24 MiB total normalized-image budget per page. Ordinary `scan` without `--preview` creates no preview and opens no viewer.

## What it checks

- Explicit PNG/JPEG paths and UTF-8 `.log`/`.txt` files.
- Readable English image text using local OCR, with source-pixel coordinates.
- Configured literal words/phrases and sensitive domains, populated Authorization/Proxy-Authorization fields and configured session-cookie names.
- Generic emails and other populated cookies as warnings; low-confidence OCR matches also warn.

Configuration is read only when `--config` is supplied:

```toml
sensitive_domains = ["northstar.test"]
session_cookie_names = ["demo_session"]
sensitive_terms = ["Project Cedar", "Acme Training", "华星演示客户"]
```

Terms are literal, case-insensitive matches within a line, with flexible phrase spacing and ASCII word boundaries for English names. Spaces/commas stay inside a phrase; no regex, fuzzy spelling or multiline matching. Trim/collapse spaces and deduplicate by case; at most 100 phrases, 2–128 characters each, no control characters. Reliable configured matches are HIGH; uncertain OCR matches WARN. Explanations hide the text; images locate visible pixels and logs provide original line numbers and, in explicit previews, masked excerpts. Chinese terms work in UTF-8 text; image OCR remains English. This does not automatically discover confidential names or understand business data.

To compare configured business context through the shared CLI:

```sh
.venv/bin/agentsafe scan examples/synthetic/business-context.png examples/synthetic/business-context.log --config examples/synthetic/terms-policy.toml
```

The example domain and all authentication values are fictional. Reserved example emails and obvious placeholders are suppressed unless a domain is explicitly configured as sensitive. HIGH indicates structural/configured evidence, not a verified working credential. An image without a finding does not require approval.

## Results and limits

| Exit | Meaning |
| --- | --- |
| 0 | All requested inputs inspected; no HIGH findings. Warnings can remain. |
| 1 | Scan completed with HIGH findings to review. |
| 2 | Setup/input/inspection failure. Takes precedence over findings. |

Unsupported inputs, corrupt images, invalid encoding, missing OCR and exceeded limits cannot pass silently. `doctor` uses 0 for ready and 2 for prerequisite/configuration problems. Text scans work without Tesseract; image scans do not.

**Known miss:** the included tiny blurred screenshot contains a configured domain, but OCR extracts no text and the scan returns 0 with an explicit limitation. That is a real demonstration of the coverage gap, not a safe-image verdict. See [fixture labels and measured results](examples/synthetic/README.md).

Initial limits: 10 MiB/20 megapixels per image, 5 MiB/100,000 lines per text input, 32,768 characters per line, 200 findings per file, 20 files per invocation and 10 seconds per OCR subprocess. The 60-second invocation budget is cooperative between stages, not a hard sandbox for decoders/filesystem reads. No input is silently truncated. Animated images and EXIF-rotated JPEGs are rejected; transparent pixels are rendered on white. Hidden pixels and metadata are not inspected.

Only declared text patterns are covered. Arbitrary API keys/passwords, confidential-dashboard recognition, automatic name/sensitivity classification, faces, QR codes, PDF/video/HAR parsing and automatic redaction are outside the demo. A source-code secret scanner does not automatically scan image OCR output.

Ordinary CLI scanning makes no network requests and creates no raw input/OCR temporary files. The GUI adds only the loopback connection described above. Explicit `--preview` and `demo` materialize a private local HTML page as described above. Tesseract runs through stdin/stdout; installation downloads are separate. Reports still contain filenames, which may be sensitive: review output before sharing.

This is a manual local check. It does not inspect Git history, install hooks or intercept any upload or push. Changes after scanning need a new check. Passing is not privacy certification.

## Development and evidence

```sh
.venv/bin/python -m pytest -q
.venv/bin/python examples/synthetic/generate.py
```

The tests cover decisions, masking, coverage failures and real OCR. OCR tests explicitly skip if Tesseract/eng is unavailable; do not report a skipped run as OCR validation. Source tests use `src/`; reinstall with `.venv/bin/python -m pip install .` after editing source to refresh the installed command. The fixture generator draws fictional layouts with Pillow and never captures a screen.

October 6, 2026: **93 tests passed, zero skipped** on the reference Mac, including authenticated loopback requests, malformed/oversized selection, visible coverage failures, missing OCR, masking, real OCR, clear/rescan and shutdown. Browser checks exercised the file chooser, invalid domain settings, original files (4 HIGH / 2 WARN), reviewed files (0 HIGH / 1 WARN), image highlighting and refresh recovery. The actual GUI screenshot above contains fictional data. Native LaunchServices startup was verified with a loopback-only listening process. Some later browser-tool button dispatches timed out; drag/drop and small-screen layout have not been fully exercised. No clean-machine/platform or independent usability claim follows.

October 7, 2026: **122 tests passed, zero skipped** on the reference Mac. New cases cover configured phrases without domains, Chinese log text, literal punctuation/regex-like text, English word boundaries, masking, configuration/resource failures and OCR phrase boxes/confidence. The fictional business image/log produced 2 + 3 HIGH findings. Browser verification exercised the new sample, image click/highlight, user-selected files with three explicit phrases, invalid-term/stale-result feedback, and rechecking the same files with empty settings (0 findings) and restored terms (5 HIGH). Installation and the development launcher were rebuilt from this source; native launch served the new interface on a loopback-only listener. This remains synthetic evidence; clean-machine distribution and wider UI testing are pending.

October 7, 2026, masked-log follow-up: **137 tests passed, zero skipped**. Added tests cover auth/cookie/term/domain/email masking, overlapping spans, malformed cookie context, placeholders, HTML/control escaping, long-line windows, default-off preview capture, unchanged snapshot/originals and no partial excerpts after failures. Browser checks verified original (4 HIGH / 2 WARN), reviewed (0 HIGH / 1 WARN) and business (5 HIGH / 0 WARN) samples, clicks moving highlight/focus between lines and Chinese text masking. No browser warnings/errors were observed in that run. The screenshots above contain fictional data only; broader responsive, clean-machine and independent-user validation remain pending.

The project is currently at private demo review. Evaluate whether the findings and locations are understandable before adding integrations. Public release, licensing and a Git route are later decisions; MIT remains a proposal, with no license grant established yet.

## Design documents

- [Product definition and competitive assessment](PRODUCT.md)
- [Roadmap](ROADMAP.md)
- [Architecture and coverage](ARCHITECTURE.md)
- [Contributor and agent instructions](AGENTS.md)
