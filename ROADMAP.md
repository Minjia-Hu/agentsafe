# AgentSafe — Roadmap

[中文](ROADMAP.zh-CN.md)

AgentSafe starts as a local screenshot/log review tool. The current candidate is **0.1.0a1, a source Alpha**. Stages describe priorities, not permission to publish or expand scope. Independent installers are not a prerequisite for this source Alpha.

## Phase 1 — Technical demo: implemented

- Explicit PNG/JPEG and UTF-8 log/text scanning; bounded local OCR and small configured/structural rules.
- GUI and CLI share the scanning core. Fictional positive, benign and known-miss samples make the workflow reproducible without private data.
- Image locations, masked log excerpts, coverage/errors and clear no-readable-text states.
- Manual opaque image covering, a new PNG, exact-byte recheck with the original policy, and explicit download; originals preserved.
- Authenticated loopback sessions, transient GUI state, bounded inputs, output masking and privacy behavior tests.

Evidence: [fixture labels](examples/synthetic/README.md) and [validation](docs/VALIDATION.md). Synthetic success does not establish general accuracy or demand. Browser ergonomics and independent usability remain open checks.

## Phase 2 — Source Alpha: release candidate

Implemented preparation includes MIT licensing, bilingual instructions, contribution/security guidance, source/wheel installation checks and a macOS/Linux CI matrix. The intended first experience is source install → open local browser → try fictional sample → review → create/recheck a PNG copy. Terminal setup is still required; later everyday review takes place in the browser.

Before publication:

1. Review the exact candidate tree and reachable history; keep private records and real artifacts out of the repository.
2. Confirm CI for the exact candidate, including zero skipped behavior tests, distribution builds and installed-wheel checks.
3. Keep supported platforms, OCR limitations, manual sharing boundary and unresolved naming/package ownership explicit.
4. Review the public scope and release notes. Repository visibility, release tags and package publication are separate maintainer actions. Follow [the release checklist](docs/ALPHA_RELEASE.md).

Do not advertise a standalone installer, production-grade detection, automatic redaction or push interception. A completely fresh end-user Mac and Windows remain unvalidated. Public feedback should use fictional reproductions and descriptions of actual workflows, not uploads of private material.

## Phase 3 — Post-launch learning

Prioritize what actual use reveals:

1. Improve setup and review ergonomics, measure unwanted warnings and missed supported cases. Investigate a self-contained Mac installer if installation is the recurring obstacle.
2. Learn where people share files, what they remove and whether they repeat the check. Praise, stars and a handful of synthetic examples are not retention evidence.
3. Consider a mature local secret engine for extracted text only if standalone credentials are a recurring need; do not build a provider-rule catalog.
4. Evaluate one additional format, OCR language or integration at a time with labeled positive, benign and failure cases.
5. Consider Git protection only for demonstrated Git publishing workflows and the full historical-version/destination requirements in ARCHITECTURE.md. Hooks do not cover API uploads or attachments.

Cloud inference, enterprise services and adversarial enforcement are not committed. If the workflow has little recurring value, simplify rather than accumulate features.
