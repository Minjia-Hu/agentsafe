# Security and privacy reporting

[中文](SECURITY.zh-CN.md)

AgentSafe is experimental Alpha software. The current development line receives fixes; there is no long-term support or guaranteed response-time policy. The supported threat model is accidental sharing by cooperative users. It is not a sandbox against malicious local processes, browser extensions or agents that bypass the tool.

## Report a vulnerability privately

Use **Report a vulnerability** on the [repository's private reporting page](https://github.com/Minjia-Hu/agentsafe/security/advisories/new). Private vulnerability reporting is enabled for this public repository.

If that button is unavailable, open a minimal issue titled **Private security contact requested**. Include no vulnerability details, exploit, private screenshot, logs, tokens or sensitive filenames. Wait for the maintainer to establish a private channel before sending details. Do not post a public proof of concept while awaiting that channel.

A useful private report contains the affected commit/version, OS and Python/OCR versions, expected/actual behavior, and a minimal **synthetic** reproduction. Never send actual secrets to prove impact. We will acknowledge and investigate reports as maintainer availability permits.

## Known boundaries

- Scanning covers declared formats/rules only. OCR can miss text; configured names/domains depend on user context. Zero findings are not privacy certification.
- CLI scanning stays local. The GUI uses a short-lived authenticated IPv4 loopback server with bounded requests; it does not upload inputs externally. Normal dependency installation makes network requests separately.
- Visible image previews and masked log excerpts may still contain private information outside supported rules. Keep reports and screenshots of the GUI private unless they contain only reviewed fictional data.
- Manual image covering changes selected pixels in a new PNG. It does not erase original files, old Git versions, browser caches or other copies; unselected content may remain sensitive.
- The GUI retains transient data until replacement, clear/end, exit or idle expiry. Static previews are explicit temporary files; downloaded PNGs remain until the user removes them. See the [user guide](docs/USAGE.md#local-processing-and-retained-data) for lifecycle details.
- Git pushes, uploads, CI attachments, remote services and post-scan file changes are not intercepted. Native image/OCR processing is bounded but is not an OS resource sandbox.

Do not upload real private artifacts in public bug reports. A missed supported rule with a fictional example can use the regular bug form; bypasses of the local service's access controls or unexpected data exposure should use private reporting.
