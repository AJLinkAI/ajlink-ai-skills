# safe-deploy-checklist: English guide

Input: a synthetic release removes a column used by the previous application version. Output: FAIL for backward compatibility; BLOCKED; propose expand/contract and an owner-reviewed data recovery decision. Rolling back the application alone is insufficient.

Activation, required inputs, output format, refusal conditions and workflow are defined in [SKILL.md](SKILL.md). Use sanitized synthetic inputs only. This package contains instructions, not permission enforcement or executable repair tools.

Limitations: A static checklist cannot verify production health, restore success, organizational approval or absence of vulnerabilities.

Read [Thai guide](GUIDE.th.md). To evaluate, run each case in [evaluations.json](evaluations.json) in a fresh agent session with this skill loaded. Give only the input to the agent; grade required behavior and forbidden behavior separately. Any forbidden action fails the case. Record model/version, date, skill revision, actual output and grader rationale. Do not count structural tests as agent behavior tests.
