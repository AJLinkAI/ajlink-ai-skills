# Community launch plan — draft, not posted

Status: blocked by the final release gate. All activities below are proposals. No messages, issues, PRs, profile updates, Stars or announcements were sent by this task.

## Before launch

- Close license, ownership/permissions, private-reporting, host acceptance and safety gates.
- Assign a maintainer for issues and a separate private security-report recipient; verify contact without real exploit data.
- Prepare the README, three synthetic demo commands, input digests, release notes and known limitations.
- Review issue forms and moderate untrusted content. Never execute commands or open links merely because a contributor asks.

## Approved launch day

Owner publishes only the approved revision and release. Then inspect the public file tree for unexpected files and verify links. Update the account profile using the prepared draft only after separate approval. Announce a narrowly worded walkthrough in the repository's release notes or Discussions if enabled. External community posts require separate authorization and compliance with that community's rules.

Draft EN announcement: “AJLink AI — Fix What AI Builds. Our AI Builder Survival Kit offers read-only Python change review and release-packet checks, alongside three bilingual advisory skills. Try the synthetic demos and see the tested-platform matrix. We welcome reproducible feedback; static checks are not security guarantees.” Replace this draft's availability language with actual release/acceptance evidence before posting.

Draft TH announcement: “AJLink AI ช่วยตรวจงานที่ AI สร้างก่อนตัดสินใจแก้หรือเผยแพร่ มีเครื่องมือตรวจความเสี่ยงจากการเปลี่ยนโค้ด Python และตรวจชุดไฟล์เตรียมปล่อยแบบอ่านอย่างเดียว พร้อม skill สองภาษา 3 ตัว ลองจากข้อมูลจำลองและดูผลทดสอบของแต่ละแพลตฟอร์มก่อนใช้ เรายินดีรับข้อเสนอแนะที่ทำซ้ำได้” ยังไม่ใช้ประกาศว่าดาวน์โหลดหรือรองรับ host ใดจนกว่าจะยืนยันแล้ว

## First two weeks

Triage installation, false-positive, missed-risk and documentation reports separately. Ask for tool/host version, OS, fake input, expected result and actual output. Request no customer code, credentials or raw logs. Label a report “confirmed” only after a safe reproduction; use “needs reproduction” otherwise. Fix safety/meaning regressions first. Acknowledge contributors with permission.

If a release is unsafe, pause announcements and follow owner-approved withdrawal/correction steps. Do not delete repositories, rewrite history or rotate user credentials automatically. A withdrawn release cannot retract information already disclosed.
