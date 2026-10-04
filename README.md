# AgentSafe

### Don't accidentally publish what your AI agent saw or generated.

**A local privacy gate for screenshots and debugging artifacts headed to public Git.**

Your agent captured a browser window to prove a fix. The screenshot still contains an internal URL and an account email. A broad `git add .` puts it in the next commit.

AgentSafe is designed to stop that push and show you what needs review—before the artifact becomes public.

```text
AgentSafe Privacy Gate
Destination: github.com/example/ui-demo   Visibility: PUBLIC

HIGH    F12  screenshots/dashboard.png
        Configured internal URL + email address (local OCR)
HIGH    F13  debug/session.har
        Authorization + session-cookie values
REVIEW  F14  demo.mov
        Video content not inspected

Push stopped. Inspect the exact versions, fix, or explicitly approve.
```

**Draft concept — not released.** This is a synthetic example of the proposed CLI, not a recording of working software. The name is provisional. No executable, package or installation command is available from this repository yet.

**Design review:** The [second-pass review](PRODUCT.md#second-pass-review--october-5-2026) reconsiders mandatory review of every image and tests whether Git push is the relevant publishing path. The workflow below remains a proposal pending those decisions.

The internal domain and session-cookie name above are explicitly configured as sensitive. A generic email or preference cookie alone is not a HIGH finding.

## Why it exists

Coding agents increasingly produce screenshots, logs and browser debugging captures. Those files can reveal personal information or internal context even when they contain no recognizable API key.

AgentSafe focuses on the **artifact publishing decision**: what committed evidence is about to leave your machine, where it is going, and whether its exact contents have been reviewed. Keep your existing credential scanner; AgentSafe is intended to complement it.

The initial audience is open-source web developers who publish browser/agent-generated evidence to public GitHub. It does not require a specific coding agent.

## Proposed v0.1

- Check the actual GitHub.com push destination; unknown visibility uses public policy.
- Inspect selected artifact versions across outgoing commits, including versions deleted or replaced later.
- Use local OCR to locate readable emails and configured internal domains in PNG/JPEG screenshots.
- Inspect debugging text and HAR authentication/cookie fields with a small rule set.
- Require exact-version review for selected images and clearly mark unsupported media/documents as uninspected.
- Offer masked findings, a repository-local pre-push hook, content-bound approvals and explicit ignores.

```text
capture / debug -> git add -> git commit -> AgentSafe gate -> git push
                                               |
                                      inspect -> fix or review
```

## Intended workflow

These commands describe the proposed interface. They cannot be run against this draft repository yet. Distribution naming and installation instructions will be verified before launch; do not assume a package named `agentsafe` belongs to this project.

```text
agentsafe init
agentsafe scan --staged
git commit
git push

# After a stopped push:
agentsafe inspect F12 --open
agentsafe allow F12 --reason "Reviewed synthetic demo"
git push
```

Approval applies only to the displayed requirements for the exact artifact bytes, path, destination and policy. Changed content requires review again. Inspect all outstanding items before retrying.

If the content is sensitive, fix the unpushed commits containing it. Editing the working file or adding a later deletion does not remove an earlier Git version. AgentSafe will explain this; it will not rewrite your history.

## Local processing, honest limits

Artifact scanning stays on your machine. A visibility check sends repository destination metadata to GitHub, not artifact contents. Offline mode applies conservative public policy. No AgentSafe account, cloud vision or telemetry is planned.

OCR may miss small, blurred or unsupported-language text. The tool cannot reliably infer confidential dashboards or customer names, so selected images require a publishing review even without a rule hit. Known videos, PDFs and other opaque candidates require review without content inspection. Automatic redaction and QR decoding are outside v0.1.

A local hook covers local Git pushes from repositories where it is installed. It can be bypassed and does not protect API uploads, PR attachments, release/CI assets, LFS payload transfers or newly created repositories without the hook. It does not audit a private repository later made public. Passing a scan is not a privacy certification.

## Design documents

- [Product definition and competitive assessment](PRODUCT.md)
- [Demo, launch and post-launch roadmap](ROADMAP.md)
- [Architecture, proposed stack and repository structure](ARCHITECTURE.md)
- [Contributor and coding-agent instructions](AGENTS.md)

The next step is reviewing these drafts. Implementation starts only after explicit approval. MIT is the proposed open-source license; no license grant or package release is established yet.

## Launch visual plan

Replace the illustrative terminal block with a verified 30–45 second synthetic demo: capture → stopped push → exact-version inspection → reviewed retry. Add a side-by-side fictional screenshot and its highlighted review regions immediately below the headline. Keep raw values fictional, show that OCR runs locally, and demonstrate a historical version that survives a later deletion.

The first screen should communicate "your screenshot can leak context" in seconds. Avoid invented badges, unsupported accuracy claims or "first screenshot scanner" messaging; OCR scanning and local redaction tools already exist.
