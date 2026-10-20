# GitHub market gaps

Research date: 2026-10-20. Primary sources: the four requested public repositories, their issue/discussion pages, READMEs and release pages. No repository was cloned, installed, modified or contacted. These are qualitative observations, not market-size estimates or proof that a competitor currently fails. Web pages can be cached; state below is the state displayed when retrieved. A verified report means the report exists, not that AJLink independently reproduced the defect.

## Verified reports and requests

| Area | Primary evidence and observed context | What it supports | AJLink response |
| --- | --- | --- | --- |
| Agent reliability | [anthropics/skills #1957](https://github.com/anthropics/skills/issues/1957), opened Oct 3, reports generated description metadata parsed as the wrong YAML type. [marketingskills #497](https://github.com/coreyhaines31/marketingskills/issues/497) requests trigger evaluations and a prove-need lifecycle. | Validation/discovery and activation evidence are separate concerns; a request is not a completed benchmark. | Preserve metadata tests, require actual host activation evidence, publish known limits. |
| Coding regressions | [superpowers #2146](https://github.com/obra/superpowers/issues/2146) describes an extracted rounding function whose initial failure was a missing export rather than the behavior under repair. | A failing or passing command can provide irrelevant evidence. Not independently reproduced here. | Report concrete snapshot locations and suggest a behavioral counterexample; never claim tests ran. |
| Installation | [UI UX Pro Max #347](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/347) reports symlink packaging trouble; it was closed Aug 12 after maintainers recorded a real-directory install. [marketingskills #243](https://github.com/coreyhaines31/marketingskills/issues/243) reports plugin-path validation failure and is closed. | Historical, demonstrated installation friction; neither is presented as a current unfixed defect. | Keep complete plain skill folders, no hooks or plugin manifests; distinguish a successful copy from successful host discovery. |
| GitHub publication safety | [UI UX Pro Max #457](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/457), opened Aug 24 and displayed open, reports a release pipeline blocked by rejected authentication. | Release operations can fail independently of source quality. This is not evidence of leaked credentials. | Safe GitHub Publisher checks supplied release evidence and configuration; actual remote authorization remains manual. Demand for this exact AJLink tool is an inference. |
| Agent permissions | [anthropics/skills #1942](https://github.com/anthropics/skills/issues/1942), opened Sep 30, reports an evaluation workflow assuming subagents where the host forbids unrequested delegation. [discussion #1948](https://github.com/anthropics/skills/discussions/1948), Oct 1–2, asks how to declare dependencies and handle their absence. | Host constraints and dependencies need explicit handling. Community replies are guidance, not a new specification. | No delegation, installs, elevated access or host assumptions in the new CLIs. Missing acceptance evidence blocks release. |
| Project handover | [superpowers #1942](https://github.com/obra/superpowers/issues/1942) reports concurrent sessions mixing task artifacts in a shared checkout; the page is closed and links a follow-up. | Historical evidence of provenance and session-scope risks. It does not measure demand for a separate handover product. | Versioned handover template, snapshot digest and explicit owner/unknowns; no shared mutable agent ledger. |
| Cross-platform compatibility | [UI UX Pro Max #239](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/239) reports colon-containing names breaking Windows installers; page is closed. [superpowers #1918](https://github.com/obra/superpowers/issues/1918) reports a Windows hook path containing parentheses; page is closed. | Portable names and shell boundaries matter. Historical reports do not establish AJLink Linux/macOS support. | Validate logical paths; no shell interpolation; test Unicode/spaces as data. Only Windows Python execution is verified here. |

The [Anthropic installation discussion #1332](https://github.com/anthropics/skills/discussions/1332) also shows users needing help choosing between Claude Code, Claude.ai and API installation surfaces. AJLink should show a host/status matrix before any instructions.

## Release and documentation review

| Repository | What was inspected | Observed lesson |
| --- | --- | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | README, issue list, discussions and [releases](https://github.com/anthropics/skills/releases), which displayed no releases | Host-specific entrypoints are documented. README distinguishes Apache-2.0 examples from source-available document skills; do not assume one license covers every folder. |
| [obra/superpowers](https://github.com/obra/superpowers) | README, issue reports, installation troubleshooting and [release notes](https://github.com/obra/superpowers/releases), including v7.0.0 and v6.4.x entries | Version-specific installation and behavioral changes need visible release notes. MIT is shown; no content was imported. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | README, installation issues and [v2.15.0 release documentation](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/releases) | Release notes describe preserving the CLI/install contract while changing retrieval behavior. README shows MIT. No installer was run or copied. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | README, current issue list, activation-eval request and [releases](https://github.com/coreyhaines31/marketingskills/releases), displaying v2.13.0 | Outcome-specific names and concrete deliverables aid discovery. MIT is shown. No skill, rubric, asset or script was copied. |

These version labels are observations of retrieved pages, not guarantees of the newest available release. Current issue lists were reviewed, but this is a scoped sample, not an exhaustive census. No star/fork totals are used to imply product fit.

## Assumptions to validate

- Users want a small Diagnose → Fix Safely → Release Check → Handover kit rather than another large catalog. Test with five voluntary, synthetic walkthroughs after approval; no users have been contacted.
- Structured risk reports will improve fix review. Test whether a reviewer can identify the changed contract and design the right counterexample faster; no speed claim yet.
- A release-packet audit will reduce accidental publication mistakes. Validate false positives and missing-file coverage before describing it as protection.
- Bilingual guidance may help Thai maintainers. Obtain independent Thai review and actual usage evidence; do not equate translation with adoption.

Counterevidence matters: [superpowers #2102](https://github.com/obra/superpowers/issues/2102) was closed as not planned because a wording proposal lacked a real failure session and before/after evaluation. AJLink contributions should meet the same evidence principle without copying that project's instructions.

## Priority

Ship two narrowly scoped, testable local CLIs first. Keep three existing skills unchanged. Improve setup clarity and honest acceptance records before adding hosts, plugins, dependencies or growth campaigns. Publication safety and handover positioning remain hypotheses; do not market them as proven unmet demand.

ภาษาไทย: หลักฐานยืนยันว่ามีผู้รายงานหรือขอฟีเจอร์ ไม่ได้แปลว่าเราทดสอบปัญหานั้นซ้ำแล้ว รายการที่ปิดหรือแก้แล้วระบุไว้ชัดเจน ส่วนความต้องการชุดเครื่องมือ AJLink เป็นสมมติฐานที่ต้องให้ผู้ใช้ลองจริงก่อนกล่าวอ้าง
