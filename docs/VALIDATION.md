# Validation record

[中文](VALIDATION.zh-CN.md)

Measured evidence on named environments does not establish general accuracy or universal platform support. All test/demo artifacts are fictional.

## Pre-publication fixes — October 25, 2026

- Added bounded recognition of quoted scalar and equals-separated authentication/cookie fields. Synthetic regressions verify standalone detection, multiple fields, escaped quotes, empty/placeholders, original offsets, masking in both review renderers and withholding ambiguous line context. Uncertain structures retain noninteractive finding locations; this is not JSON/HAR document parsing.
- Static asset requests and rejected API requests no longer renew GUI idle retention. Removed design comparison routes and unused candidate artwork from the installed package.
- Raised Pillow to `>=13,<14`; the reference installation uses 13.0.0. The [upstream PNG EXIF advisory](https://github.com/python-pillow/Pillow/security/advisories/GHSA-g4qv-2jxx-769h) affects the earlier `getexif()` path. Reviewed on October 25; not all upstream format-specific advisories apply to AgentSafe's PNG/JPEG-only path.
- 172 behavior tests passed locally with no skips. A new macOS Python 3.12.12 environment installed the source; source/wheel builds and the installed-wheel doctor, fictional demo and GUI/PNG-copy smoke passed outside the checkout. Tesseract 5.5.2 / English and Typer 0.27.3 were used in the independent environment.
- Browser checks in English and Chinese passed quoted-log masking, ambiguous-line fallback, the fictional customer/project example, two-region image covering, recheck, download and session end. No browser script errors were observed. This was Chromium on the reference Mac, not a broader browser certification.
- Audited all eight resolved runtime dependencies with pip-audit: no known vulnerabilities reported. CI now audits exact installed dependency versions; Dependabot proposes weekly Python/Actions updates. Queries concern public dependency metadata, not user artifacts.
- The audit tool's temporary copied-Python environment could not locate a dynamic library on the reference uv-managed Mac. Auditing the exact resolved versions directly passed. A normal fresh virtual environment installed and ran AgentSafe successfully. Homebrew/Python/OCR were not installed from scratch on a clean machine; that gap remains.

The new candidate still requires CI on its exact commit before publication. Earlier matrix results below remain historical evidence.

## Source Alpha checks — October 18–24, 2026

- A fresh virtual environment installed source with build isolation and normal dependency resolution on macOS, Python 3.12.12, Tesseract 5.5.2 / English, Pillow 12.3.0, Rich 14.3.4 and Typer 0.27.3. Python/OCR were already present; this was not a clean-machine setup test.
- 156 behavior tests passed with zero skipped. Source archive and wheel for `0.1.0a1` built successfully. A separate installed-wheel environment outside the checkout passed `doctor`, the bundled CLI demo and the authenticated GUI/manual-PNG smoke.
- The installed smoke checks packaged assets, session authentication, fictional phrase detection, opaque RGB pixels, original-policy recheck, exact exported bytes and clearing state.
- macOS paths under the `/var` symlink alias caused CLI demo inputs to be rejected. Installing under the resolved `/private/var` path passed; the README documents the symlink restriction. No input safeguard was weakened.
- CI exposed and helped fix Python 3.11 f-string compatibility and a stop-response race. Session state/token are now cleared before `/api/stop` acknowledges success.

The following matrix passed on the source implementation before the latest documentation cleanup. The workflow runs again on each pushed candidate; consult [CI](https://github.com/Minjia-Hu/agentsafe/actions/workflows/ci.yml) for the exact revision and result rather than assuming every later revision passed.

| Environment | OCR | Behavior tests | Distribution / installed checks |
| --- | --- | --- | --- |
| Ubuntu 24.04 / Python 3.11 | Tesseract 5.3.4, eng | 156 passed, 0 skipped | Passed |
| Ubuntu 24.04 / Python 3.12 | Tesseract 5.3.4, eng | 156 passed, 0 skipped | Passed |
| macOS 14 / Python 3.12 | Tesseract 5.5.3, eng | 156 passed, 0 skipped | Passed |

The latest local candidate check on October 24 passed all 156 tests with zero skipped (10.21 seconds). Source and wheel builds succeeded; the installed wheel passed doctor, the fictional demo and the GUI/PNG-copy smoke outside the checkout. Local Gitleaks 8.30.1 scans of reachable history, complete historical blobs and the candidate tree returned zero findings. Documentation links and English/Chinese scope consistency were also reviewed.

## Browser and scanner evidence

Earlier local checks exercised file selection, invalid context, stale-result feedback, refresh recovery, image finding selection, masked log-line highlighting, manual pixel coordinates, undo and a two-region PNG copy/recheck with a download link. Reference synthetic outcomes were 4 HIGH / 2 WARN for original samples, 0 HIGH / 1 WARN for prepared reviewed samples, and 5 HIGH for the customer/project sample. OCR versions can change individual matches.

Behavior tests cover supported positives and benign boundaries, literal terms and Chinese log phrases, masking/escaping, corrupt/unsupported/oversized inputs, missing OCR, empty OCR output, authentication, stale review IDs, unchanged originals, output pixels and session lifecycle. See [fixture labels](../examples/synthetic/README.md) for expectations and the known small/blurred-image miss.

## Publication review

The candidate tree and reachable historical file versions were reviewed with a local secret scanner and supplementary text/image checks. Fictional examples and original project artwork are retained. A zero-finding secret scan is limited evidence, not proof that no private datum or vulnerability exists. Public issues should use fictional reproductions; see [SECURITY.md](../SECURITY.md).

## Remaining gaps

- Completely fresh end-user Mac installation, including Homebrew setup.
- Windows and platforms outside the recorded matrix.
- Broader browser/responsive coverage, pointer-drag ergonomics and browser-specific download behavior.
- Independent usability, repeated use, real-world false-positive/false-negative rates and market demand.

Source Alpha preparation does not imply a published release, a standalone installer or production readiness.
