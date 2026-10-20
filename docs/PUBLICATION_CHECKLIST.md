# Publication and rollback gate / ด่านก่อนเผยแพร่

Use the current [GitHub-first checklist](RELEASE_CHECKLIST.md). Older entries do not authorize website work or imply host support. There are 19 preserved skill cases; consult their current evaluation files.

- [ ] Verify AJLinkAI identity, paginated repository coverage, target-name availability and effective create/push/admin rights.
- [ ] Owner confirms copyright, contribution rights and final license; replace LICENSE proposal with complete approved text.
- [ ] Review every file, hidden/untracked/ignored files, proposed Git history and workflow diff. Exclude local build helper and evaluation transcripts from publication.
- [ ] Run tests and audit on exact release revision; after Git initialization scan full reachable history and review the staged tree. Obtain an independently reviewed secret scan before initial push.
- [ ] Run all 19 behavioral cases on every host to be claimed using fresh read-only sandbox sessions; record actual outputs and grading. Have a Thai reviewer verify fidelity and fluency.
- [ ] Smoke-test local installation, invocation, duplicate-name behavior and removal on each claimed host/version.
- [ ] Recheck official docs and all external links, including KlangPrompt.com; verify private vulnerability reporting route.
- [ ] Configure branch protection/rules, review requirements and no-secret Actions policy; review hosted runner cost and leave Actions disabled until approved.
- [ ] Owner gives explicit FINAL approval for the exact repository name, public visibility, revision, initial push and release. Website modifications require separate explicit approval.
- [ ] Only after approval create/push/publish; inspect the public tree and links without exposing private evidence.

Rollback before publication: stop and retain this local candidate; no remote state exists to undo. After an approved release: stop announcements, mark the release withdrawn through an owner-approved action, advise users to move the exact installed directories outside discovery paths, and prepare a reviewed corrective release. Do not automatically delete repositories, rewrite history or change visibility. Disclosure cannot be reversed by deletion; suspected exposure requires private owner-led response and credential rotation outside this project. Reverting a skill does not undo actions an agent already performed.

ภาษาไทย: ต้องยืนยันบัญชี สิทธิ์ สัญญาอนุญาต ผลทดสอบ ช่องทางแจ้งปัญหา และอนุมัติรุ่นที่จะปล่อยก่อนทำงานภายนอก หากต้องถอนรุ่นให้หยุดการประชาสัมพันธ์และประสานเจ้าของ การลบภายหลังไม่ทำให้ข้อมูลที่เผยแพร่แล้วกลับเป็นส่วนตัว
