# Alpha release checklist

[中文](ALPHA_RELEASE.zh-CN.md)

Candidate: **0.1.0a1**, MIT-licensed source Alpha. Preparation does not create a tag, publish a release/package or change repository visibility.

## Candidate scope

Local browser GUI and CLI for explicit PNG/JPEG screenshots and UTF-8 logs/text; configured phrases/domains and structural authentication/cookie checks; masked locations; manual opaque PNG copies with original-policy recheck and explicit download; fictional examples and the A-monogram icon.

No standalone installer, cloud inference, automatic redaction, automatic confidential-name discovery, additional formats/languages, Git hook or upload interception. These limits belong in the release notes.

## Before publication

1. Review the exact candidate tree, reachable history, license and both documentation languages. Review every newly added artifact as well as source changes.
2. Require CI on that exact revision: all three matrix jobs plus dependency security, zero skipped behavior tests, distribution builds and installed-wheel smoke. Use [validation](VALIDATION.md) for evidence and gaps, not as a substitute for the current run.
3. Confirm the maintainer's publication decision. Verify naming/distribution clarity; do not direct installation to an unowned package name.
4. If changing visibility, enable GitHub private vulnerability reporting and verify the entry before announcing that channel. Follow SECURITY.md; do not invite real sensitive attachments in public issues.
5. Create prerelease tag `v0.1.0a1` only for the reviewed revision after release approval. GitHub source archives suffice for this source Alpha. Registry publication and uploaded packages require separate verification and approval.

## Draft prerelease notes

AgentSafe is an experimental local privacy checker for screenshots and debugging logs, with a browser GUI and CLI. Locate supported sensitive signals, manually cover image regions in a new PNG, and recheck that same copy before saving.

Install from source using README and try the fictional Customer / project names example. No real private files are needed. Source and original project assets are MIT-licensed.

The Alpha supports readable English image text and UTF-8 logs, including configured Chinese text phrases. OCR and rules can miss private content; zero findings are not privacy certification. It does not intercept Git pushes/uploads. See validation for tested environments and unresolved platform/usability gaps.

Feedback is most useful as a concrete installation/review problem with a small fictional reproduction. Report vulnerabilities through SECURITY.md.
