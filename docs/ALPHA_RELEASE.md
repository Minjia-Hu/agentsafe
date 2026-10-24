# Alpha release preparation

[中文](ALPHA_RELEASE.zh-CN.md)

Prepared on October 18, 2026. Candidate package version: **0.1.0a1**. No public release/tag or package-registry upload has been made by this preparation. Repository visibility remains private pending the final publishing decision.

## Release scope

- Local browser GUI and CLI for explicitly selected PNG/JPEG screenshots and UTF-8 logs/text.
- Configured sensitive phrases/domains, structural authentication/cookie checks, masked findings and locations.
- Manual image-region covering into a new PNG, original-policy recheck and explicit download.
- Bundled fictional examples, including a known OCR miss; selected A-monogram browser icon.
- MIT-licensed source installation, English/Chinese instructions, contribution/security guidance and CI.

The Alpha does not include an independent Mac installer, cloud scanning, additional formats/languages, automatic sensitive-name discovery, automatic redaction, a Git hook or upload interception. Keep these boundaries in release notes.

## Preparation evidence

The final installation, test, package and repository-audit results are recorded in [VALIDATION.md](VALIDATION.md). Local preparation checks are recorded; remote CI verification follows the private push. A local test run is not a GitHub Actions result or a clean-machine test.

## Final publication steps

1. Finish the source/wheel checks, review repository content and history, and commit/sync the prepared changes to the existing private remote.
2. Review the exact remote commit and CI result. Do not imply Linux or additional Python versions are validated until their jobs pass.
3. Confirm the final public scope, including MIT licensing, both language versions of tracked documents, and all existing commit history. Removing a file only from the latest tree would not remove its history.
4. With the owner's explicit publishing confirmation, change repository visibility to public, enable GitHub private vulnerability reporting, and verify its report entry works before announcing security feedback instructions.
5. Create a prerelease for the reviewed commit, using tag `v0.1.0a1` and the notes below. GitHub source archives are sufficient for this source Alpha; a native installer is not promised. Publish package files only if separately selected and verified.

No history rewriting, visibility change, release creation or package publication is implied by completing the preparation documents.

## Proposed prerelease notes

AgentSafe is an experimental local privacy checker for screenshots and debugging logs, with a browser GUI and CLI. It helps locate supported sensitive signals and lets you manually cover screenshot regions into a new PNG, then recheck that same copy before saving.

Start with the README's source installation and the fictional Customer / project names example. No real private files are needed to try the workflow. Source and original project assets are MIT-licensed.

This Alpha supports readable English image text and UTF-8 logs, including configured Chinese text phrases. OCR and declared rules can miss sensitive content; zero findings are not privacy certification. The tool does not intercept Git pushes/uploads. See the validation record for tested environments and open usability/platform gaps.

Feedback is most useful when it describes a concrete installation/review problem with a small fictional reproduction. Use SECURITY.md for vulnerability reporting.
