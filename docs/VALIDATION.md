# Validation record

This is measured evidence on named environments, not a general accuracy or platform-support claim. The historical runs below predate the Alpha preparation.

## October 18, 2026 — Alpha preparation

- A new virtual environment installed the project from source through the normal isolated build and dependency resolution. Reference host: macOS, Python 3.12.12, Tesseract 5.5.2 with English data, Pillow 12.3.0, Rich 14.3.4 and Typer 0.27.3. Python and Tesseract were already installed on this Mac; this is not a clean-machine installation claim.
- **156 tests passed in 15.42 seconds, zero skipped**, in that fresh environment. `doctor` reported ready.
- Source and wheel distributions for **0.1.0a1** built successfully. Outside the checkout, the installed-package smoke exercised packaged GUI/icon assets, authentication, the fictional terms scan, opaque PNG generation, original-policy recheck, exact exported pixels and session clear.
- Gitleaks **8.30.1**, downloaded from its official release and checked against its published SHA-256, reported **zero findings** in all four existing reachable commits and the 109-file candidate tree. Supplementary review found no personal workstation paths in current/historical text; flagged email-like test strings were fictional. Documentation screenshots contain fictional examples. This is a scoped publication review, not a guarantee that every sensitive datum or vulnerability has been found.
- GitHub repository metadata confirmed **private** visibility. The three-job CI matrix was configured; see the completed October 24 run below.

Open checks: a completely fresh Mac following Homebrew setup, Windows, broader browser/responsive coverage, pointer-drag ergonomics and independent-user feedback. No public release or registry upload has occurred.

## October 24, 2026 — final wheel follow-up

The final source archive and wheel were rebuilt through build isolation and installed into another independent environment. An initial installation under macOS's `/var` alias caused the CLI demo to exit 2: packaged input paths contained a symlink, which the scanner deliberately rejects. Installing under the resolved `/private/var` path passed `doctor`, `demo --no-open` (exit 0, expected synthetic results) and `scripts/smoke_installed.py` outside the checkout. The README now states this path restriction. No detector behavior was weakened to make the smoke check pass.

The first GitHub CI run at the tested revision passed macOS/Python 3.12, but exposed a Python 3.11 syntax error in a preview f-string expression containing a newline escape. The translated text was moved into a separate variable, preserving output; 35 local preview/log tests passed after that change. The complete matrix then passed as recorded below.

## October 24, 2026 — remote CI passed

the recorded CI run passed for code commit the tested revision:

| Environment | OCR | Behavior tests | Packaging / installed checks |
| --- | --- | --- | --- |
| Ubuntu 24.04 / Python 3.11 | Tesseract 5.3.4, eng | 156 passed, 0 skipped | Passed |
| Ubuntu 24.04 / Python 3.12 | Tesseract 5.3.4, eng | 156 passed, 0 skipped | Passed |
| macOS 14 / Python 3.12 | Tesseract 5.5.3, eng | 156 passed, 0 skipped | Passed |

Each job built both distributions, installed the wheel into a separate environment, ran `doctor` and the CLI demo outside the checkout, and exercised the synthetic authenticated GUI / PNG-copy smoke. These hosted automated checks do not replace a fresh end-user Mac or browser interaction test. The repository remains private; publication still requires the final owner decision.

## October 24, 2026 — stop acknowledgement ordering

The documentation-only follow-up at the tested revision exposed an intermittent lifecycle failure on Ubuntu/Python 3.12: `/api/stop` sent its success response before clearing the session and token. The handler now closes the session before acknowledging success. The existing end-to-end stop test requires cleared state and rejected subsequent unauthenticated access; it is retained without sleeps or retries. After the fix, all 156 local tests passed. the recorded CI run passed for the tested revision on all three matrix environments, including distribution builds and installed-wheel checks. The earlier successful matrix above remains historical evidence for its named commit.

## Earlier local checks

October 6, 2026: **93 tests passed, zero skipped** on the reference Mac, including authenticated loopback requests, malformed/oversized selection, visible coverage failures, missing OCR, masking, real OCR, clear/rescan and shutdown. Browser checks exercised the file chooser, invalid domain settings, original files (4 HIGH / 2 WARN), reviewed files (0 HIGH / 1 WARN), image highlighting and refresh recovery. The actual GUI screenshot in the README contains fictional data. Native LaunchServices startup was verified with a loopback-only listening process. Some later browser-tool button dispatches timed out; drag/drop and small-screen layout have not been fully exercised. No clean-machine/platform or independent usability claim follows.

October 7, 2026: **122 tests passed, zero skipped** on the reference Mac. New cases cover configured phrases without domains, Chinese log text, literal punctuation/regex-like text, English word boundaries, masking, configuration/resource failures and OCR phrase boxes/confidence. The fictional business image/log produced 2 + 3 HIGH findings. Browser verification exercised the new sample, image click/highlight, user-selected files with three explicit phrases, invalid-term/stale-result feedback, and rechecking the same files with empty settings (0 findings) and restored terms (5 HIGH). Installation and the development launcher were rebuilt from this source; native launch served the new interface on a loopback-only listener. This remains synthetic evidence; clean-machine distribution and wider UI testing are pending.

October 7, 2026, masked-log follow-up: **137 tests passed, zero skipped**. Added tests cover auth/cookie/term/domain/email masking, overlapping spans, malformed cookie context, placeholders, HTML/control escaping, long-line windows, default-off preview capture, unchanged snapshot/originals and no partial excerpts after failures. Browser checks verified original (4 HIGH / 2 WARN), reviewed (0 HIGH / 1 WARN) and business (5 HIGH / 0 WARN) samples, clicks moving highlight/focus between lines and Chinese text masking. No browser warnings/errors were observed in that run. The screenshots in the README contain fictional data only; broader responsive, clean-machine and independent-user validation remain pending.

October 7, 2026, manual-copy and favicon follow-up: **156 tests passed, zero skipped**. Export tests inspect real opaque RGB pixels, exclusive rectangle edges, metadata/alpha removal and unchanged originals; HTTP tests cover stale review IDs, wrong file types/rectangles, authentication, size limits, missing OCR, session cleanup and packaged icon assets. A real browser run verified three favicon choices, detected-region selection, manual pixel coordinates, undo, a two-region copy recheck (one image, 0 HIGH / 0 WARN) and its exact PNG download link. The original term policy was retained. Pointer-drag ergonomics, clean-machine installation and the preferred-browser download experience still need usability review.
