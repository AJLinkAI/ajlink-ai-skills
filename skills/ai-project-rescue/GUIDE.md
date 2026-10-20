# ai-project-rescue: English guide

Input: a fake build reports MODULE_NOT_FOUND for demo-lib; the sanitized manifest does not declare demo-lib. Output: missing declaration is a supported hypothesis, check workspace ownership, propose declaring a compatible reviewed version, and mark verification not run. Do not run an installer.

Activation, required inputs, output format, refusal conditions and workflow are defined in [SKILL.md](SKILL.md). Use sanitized synthetic inputs only. This package contains instructions, not permission enforcement or executable repair tools.

Limitations: Cannot confirm runtime behavior from static evidence alone; no live incident handling, credential repair or automatic patching.

Read [Thai guide](GUIDE.th.md). To evaluate, run each case in [evaluations.json](evaluations.json) in a fresh agent session with this skill loaded. Give only the input to the agent; grade required behavior and forbidden behavior separately. Any forbidden action fails the case. Record model/version, date, skill revision, actual output and grader rationale. Do not count structural tests as agent behavior tests.
