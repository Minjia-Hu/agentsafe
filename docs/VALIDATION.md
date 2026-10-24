# Validation record

[中文](VALIDATION.zh-CN.md)

Measured evidence on named environments does not establish general accuracy or universal platform support. All test/demo artifacts are fictional.

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
