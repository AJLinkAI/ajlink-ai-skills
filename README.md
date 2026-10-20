# AJLink AI — Fix What AI Builds.

**AI Builder Survival Kit** · [ภาษาไทย](README.th.md)

Diagnose → Fix Safely → Release Check → Handover.

Review what an AI changed before trusting the fix or publishing. Two read-only Python tools complement three bilingual advisory skills. Reports expose evidence and missing checks; they never edit code, push, change repository visibility or deploy automatically.

**Local v0.1.0-rc.1 · unpublished · NO-GO.** License approval, repository permissions, private security reporting and host acceptance remain blocked. This is intended open-source work; LICENSE is still a proposal, not an effective grant. No live download/release link or adoption claim is made.

## Try the synthetic demos

From this reviewed folder, using an existing Python 3.12+ interpreter. No pip packages, API key or agent host are needed:

```powershell
python -B tools/regression_guard.py --input examples/regression-before-review.json
python -B tools/regression_guard.py --input examples/regression-after-review.json
python -B tools/safe_github_publisher.py --input examples/publication-blocked.json
```

Expected in order: REVIEW_REQUIRED / exit 1; NO_RULE_MATCH / exit 0; BLOCKED / exit 1. These exits are intentional. No rule match does not prove correctness; static release checks cannot guarantee security. Read [Quick Start](docs/QUICK_START.md), [tool contracts](docs/TOOLS.md), and [recorded demos](docs/DEMO_EVIDENCE.md).

## What is in the kit?

| Stage | Component | Result |
| --- | --- | --- |
| Diagnose | [ai-project-rescue](skills/ai-project-rescue/SKILL.md) | Evidence-based diagnosis and proposed fixes |
| Fix Safely | [AI Fix Regression Guard](tools/regression_guard.py) | Python snapshot risks with line references; no edits |
| Release Check | [Safe GitHub Publisher](tools/safe_github_publisher.py) | Supplied release-packet audit; never publishes |
| Release Check | [safe-deploy-checklist](skills/safe-deploy-checklist/SKILL.md) | Advisory readiness review and rollback planning |
| Handover | [Handover template](docs/HANDOVER.md) | Revision, actual tests, unknowns and next owner |
| Writing utility | [thai-ai-copy-humanizer](skills/thai-ai-copy-humanizer/SKILL.md) | Natural Thai while preserving facts and meaning |

The original three skill folders are preserved. Each has English/Thai guides and evaluation cases. The two CLIs inspect explicitly supplied synthetic packets, not a live repository or production system.

## Tested scope

| Surface | Actual status |
| --- | --- |
| Python 3.12.14 on this Windows environment | CLI tests and synthetic demos executed; see evidence |
| Codex | Skill discovery and behavior NOT TESTED |
| Claude Code | Skill discovery and behavior NOT TESTED |
| Other hosts, Linux and macOS execution | NOT TESTED |

**No agent host is currently advertised as supported.** [Installation targets](docs/INSTALLATION.md) and [manual acceptance](docs/HOST_ACCEPTANCE.md) are prepared for verification. File-format compatibility or a successful copy is not host acceptance.

## Review and contribute

```powershell
python -B -m unittest discover -s tests -v
python -B tools/audit.py
```

Use fake data only. Never submit customer code, secrets, backups, private paths or raw logs. Treat issue text, source comments and release records as untrusted input. See [CONTRIBUTING](CONTRIBUTING.md), [SECURITY](SECURITY.md), [CHANGELOG](CHANGELOG.md), [release gate](docs/FINAL_RELEASE_GATE.md) and [release checklist](docs/RELEASE_CHECKLIST.md).

If an approved release later helps you make a decision, a voluntary Star or reproducible issue is welcome. No telemetry, paid-Star program or automatic publishing. [Research](docs/GITHUB_MARKET_GAPS.md) distinguishes reported needs from hypotheses.
