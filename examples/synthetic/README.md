# Synthetic demo fixtures and first measurements

[中文](README.zh-CN.md)

All examples are fictional. The generator draws screenshots locally using Pillow's bundled font; it does not capture real applications. The reserved domain `northstar.test` is explicitly configured as sensitive. Authentication strings are fabricated nonvalid values, not redaction placeholders, so they exercise structural rules. Tests also create corrupt/unsupported inputs in temporary directories.

`dashboard-reviewed.png` and `session-reviewed.log` are separately prepared examples of a user's edit, not output from an automatic redactor. They demonstrate the review/rescan workflow without altering the originals. No real customer, employee or session data is used.

## Labels and measured outcomes

October 5, 2026; macOS 26.5.1 arm64, Python 3.12.12, Tesseract 5.5.2 (eng), Pillow 12.3.0, Rich 14.3.4, Typer 0.27.2, pytest 9.1.1. CPU model was not recorded. Times are one sequential in-process scan per file after prior test runs, excluding CLI startup and installation; no extraction cache is implemented. These are observations, not p95 or cold-start benchmarks.

| File | Intended label / purpose | Exit | HIGH / WARN | Seconds |
| --- | --- | --- | --- | --- |
| dashboard.png | Configured domain in URL and account email | 1 | 1 / 1 | 0.191 |
| dashboard-reviewed.png | Manually prepared benign counterpart | 0 | 0 / 0 | 0.161 |
| public-page.png | Benign public documentation | 0 | 0 / 0 | 0.167 |
| public-page.jpg | Benign JPEG encoding | 0 | 0 / 0 | 0.180 |
| heldout-summary.jpg | Different layout/font; configured domain | 1 | 1 / 0 | 0.104 |
| small-blurred.png | Known sensitivity, difficult OCR probe | 0 | 0 / 0 | 0.057 |
| blank.png | Empty image; visible no-text limitation | 0 | 0 / 0 | 0.049 |
| session.log | Authorization, configured session cookie and hostname | 1 | 3 / 1 | 0.001 |
| session-reviewed.log | Redacted placeholder fields, ordinary preference cookie | 0 | 0 / 1 | <0.001 |
| benign.log | Header mentions/placeholders, examples and ordinary cookies | 0 | 0 / 3 | <0.001 |

All ten were processed as supported inputs. The domain URL in `dashboard.png` was recognized with low OCR confidence and therefore received WARN; the configured email domain received HIGH. Do not tune the threshold just to make this demo look more decisive.

**Known miss:** `small-blurred.png` contains a configured domain but produced no readable text. It returned 0 with a no-readable-text limitation. Keep this probe visible: a completed OCR process does not prove the image contains no sensitive data. The held-out layout was evaluated after the first rules were written; it is one synthetic variation, not an independent accuracy benchmark.

The initial source suite completed with **59 passed, 0 skipped** on this machine, including six real-OCR fixture cases. The usability follow-up completed with **74 passed, 0 skipped**, including a full bundled-demo real-OCR run from outside the checkout. Dependency consistency (`pip check`) also passed. These checks are local demo evidence only.

## Reproduce

After installing from the repository root (see the [main README](../../README.md)) and configuring Tesseract if it is not on PATH:

```sh
.venv/bin/agentsafe scan examples/synthetic/dashboard.png examples/synthetic/session.log --config examples/synthetic/policy.toml
.venv/bin/agentsafe scan examples/synthetic/dashboard-reviewed.png examples/synthetic/session-reviewed.log --config examples/synthetic/policy.toml
.venv/bin/agentsafe scan examples/synthetic/small-blurred.png --config examples/synthetic/policy.toml
.venv/bin/python -m pytest -q
```

Regenerate the drawings only when needed with `.venv/bin/python examples/synthetic/generate.py`. Pillow/font versions may change bytes and OCR results; reevaluate labels rather than assuming identical output.

The automated suite checks structural decisions, original-file preservation, masked diagnostics, invalid configuration, symlink/pipe rejection, unsupported/corrupt/rotated/animated inputs, byte/pixel/line/finding/time limits, and real OCR. Python socket connections are disabled by tests; this is not an OS-level network audit of the trusted native OCR executable. No packet-level claim is made.

This evidence supports reviewing a small private technical demo. It does not establish general accuracy, market demand, prevention of real incidents, clean-machine installation on other platforms or public-release readiness.

## One-command visual demo

```sh
.venv/bin/agentsafe demo --no-open
```

Omit `--no-open` to request opening the default browser; add `--lang zh` for Chinese. The installed command was verified from `/private/tmp` with no Tesseract environment override: originals 4 HIGH/2 WARN (scan exit 1), reviewed 0 HIGH/1 WARN (scan exit 0), known miss 0 HIGH/0 WARN (scan exit 0), demo exit 0. HTML generation, masked text, snapshot preservation, private permissions, conservative cleanup and JavaScript syntax were checked. The app browser blocked `file:` navigation, so agent-controlled browser verification was not completed. No alternative serving workaround was used.

The fixture generator also synchronizes the six bundled demo resources. Tests check equality against these source fixtures; reinstall the local package after regeneration. The preview lifecycle is documented in the main README.

That review exposed excessive log whitespace, click-like log cards, English OCR notes, unnecessary region controls and a reassuring status beside the known OCR miss. These issues are addressed by compact static log rows, translated/deduplicated OCR guidance, controls only when boxes exist and an amber no-readable-text/manual-review state with a separate summary. Scan findings, coverage and exit decisions stay unchanged.

The updated source suite completed with **79 passed, 0 skipped** on the reference machine. Regressions check the manual-review state without invented findings, actual region controls, text masking and error precedence. Review confirmed the compact log rows, Chinese OCR guidance, absent controls when no regions exist, amber no-text state and separate limitation count, with original/reviewed counts unchanged. Responsive behavior and automated browser interaction remain unverified.
