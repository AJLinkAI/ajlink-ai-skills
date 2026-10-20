# Public release checklist — NO-GO

Content-safe staging does not authorize publication. Follow FINAL_RELEASE_GATE.md.

- [ ] Owner confirms contribution rights, holder/year and effective license; replace the LICENSE proposal only after approval. See LICENSE_REVIEW.md and PROVENANCE.md.
- [ ] Verify target ownership, effective permissions and intended public scope; do not export unrelated private inventory.
- [ ] Verify a monitored private security-reporting route and responsible recipient. Follow PRIVATE_VULNERABILITY_REPORTING.md; no public exploit details.
- [ ] Inspect every exact staged blob, manifest, workflow, fixture, hidden/untracked file and full reachable Git history. Keep owner runbooks, internal diagnostics, local evidence, credentials, backups and runtime state out of the public commit.
- [ ] Run packaged tests and audit on the exact selected snapshot; retain sanitized evidence and inspect any findings. Static checks are incomplete.
- [ ] Complete all applicable manual cases per claimed host/version/OS. No host support is currently claimed. See HOST_ACCEPTANCE.md and MANUAL_ACCEPTANCE_SUITE.md.
- [ ] Review Thai meaning, negation, numbers and claims; distinguish editorial inspection from model-host behavior.
- [ ] Verify local links in the exported allowlist, installation instructions, synthetic demos and rollback procedure.
- [ ] Review workflow permissions, runner costs and actual hosted behavior before execution; the current anonymous-fetch workflow requires a public source and has not been accepted for a private repository.
- [ ] Obtain explicit public approval for exact revision, target, visibility, initial push/tag/release and announcements. Private setup approval is insufficient.
- [ ] Only after separate authorization perform approved publication and verify the resulting public tree. Enable GitHub private vulnerability reporting when eligible and verify the reporting route.

Before publication, rollback means stop and retain the local candidate. After publication, the owner approves withdrawal/correction and notices. Never automatically delete repositories, rewrite history, change visibility or rotate credentials. Reverting source cannot retract disclosed information or undo agent side effects.

ภาษาไทย: ยังเป็น NO-GO สำหรับการเปิด Public การผ่านตรวจเนื้อหาเพื่อเตรียม Commit ไม่ทดแทนการอนุมัติ License ผลทดสอบ Host หรือคำอนุมัติให้เผยแพร่
