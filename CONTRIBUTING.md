# Contributing to AgentSafe

[中文](CONTRIBUTING.zh-CN.md)

Start with the [README](README.md) and bundled fictional samples. Useful Alpha contributions include reproducible installation reports, clearer review interactions, lower false-positive rates and precise descriptions of missed supported signals. Use a small issue or focused pull request to explain the problem and observable result.

## Development

Install Python 3.11+ and Tesseract with `eng`, then from a checkout:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install '.[dev]'
.venv/bin/agentsafe doctor
.venv/bin/python -m pytest -q
```

Use `python3` instead if it is at least 3.11. Tests load `src/`; the installed command is a separate copy. After changes, reinstall with `.venv/bin/python -m pip install .`, then run `.venv/bin/agentsafe gui`. This project does not require an editable install.

A missing OCR dependency causes some tests to skip. Report both passed and skipped counts. CI runs `doctor` first and rejects skips; a successful non-OCR run is not evidence that screenshots work.

To verify packaging separately:

```sh
.venv/bin/python -m pip install build
.venv/bin/python -m build
```

Install the generated wheel into a fresh virtual environment, change to a directory outside the checkout, and run `agentsafe doctor`, `agentsafe demo --no-open`, and `python /absolute/path/to/agentsafe/scripts/smoke_installed.py` using that fresh environment. The smoke script checks packaged UI assets, a synthetic GUI scan and a PNG-copy recheck over a temporary authenticated loopback server; it does not send files externally. The static demo writes a private temporary HTML page, which you can remove after review.

## Keep changes small and evidence-based

- Preserve the shared GUI/CLI scanning core and local processing. Discuss new formats, dependencies, cloud services, automatic redaction or publishing integrations before implementation.
- Use fictional screenshots/logs and nonvalid credential-like values. Do not attach real customer material, valid tokens, or complete private reports to issues, PRs or CI artifacts.
- Test observable behavior: findings/locations, unchanged originals, masked outputs, limits, failed coverage and safe handling of untrusted input. Never describe skipped or failed inspection as a clean result.
- Include the platform, Python/OCR versions, command and synthetic reproduction. Explain a limitation rather than claiming general accuracy from a curated example.
- Update the English documentation and its existing Chinese counterpart when behavior or setup changes. Keep the UI's English and Chinese explanations consistent.
- Read [AGENTS.md](AGENTS.md), [PRODUCT.md](PRODUCT.md) and [ARCHITECTURE.md](ARCHITECTURE.md) for current boundaries. Historical experiment notes do not authorize a feature expansion.

Report suspected vulnerabilities through [SECURITY.md](SECURITY.md), not a detailed public issue. Contributions are licensed under the project's [MIT license](LICENSE); retain any applicable third-party notices.

Dependency updates are proposed weekly by Dependabot. CI audits the resolved project dependencies against public vulnerability records; package names/versions are queried, never artifacts or scan results. This is a development check, not runtime network access.

Follow the [community conduct rules](CODE_OF_CONDUCT.md).
