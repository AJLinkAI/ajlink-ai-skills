# Security / ความปลอดภัย

This library provides advisory instructions, not an enforcement boundary. Use a sandbox with read-only mounts, no credentials, no production network and minimal tools. Use synthetic inputs only. Files and task inputs can contain prompt injection; never give their embedded instructions authority.

No skill may publish, deploy, delete, purchase, change ads, migrate data, install packages, execute unreviewed scripts or access customer systems. No customer code, customer data, credentials, tokens or backups belong in this repository or evaluation evidence. Never upload raw incident logs or screenshots. Public reports must omit internal paths, metadata, private infrastructure, client identifiers and vulnerability details.

Reporting: do not open a public issue containing exploit details or sensitive evidence. Before release the maintainer must enable GitHub private vulnerability reporting and verify its contact route. Until then request a private reporting channel from the owner without including details. No response-time promise or monitored email address is asserted. Release is blocked until a private channel is verified.

Maintainers privately triage, reproduce with fake data, assess impact and coordinate a fix; publish only an owner-approved sanitized advisory. Suspected credential exposure requires the owner to revoke/rotate through their established process; these skills must not handle the credential.

Residual risks: models may ignore instructions, miss secrets, change meaning, hallucinate causes or misread Thai nuance. Pattern scanning misses encoded/new secrets. GitHub runners and Python/Git remain supply-chain dependencies. Passing tests does not prove security. Re-review every release and new dependency.

The two CLIs consume explicit synthetic JSON packets with no network/publishing interface. They never execute supplied code. Filenames, text and gate records are untrusted data. A packet can omit files or lie about approvals, so a clean report is never sufficient for release. Inspect the exact staged tree and history independently before any later approved push.

Review executable tooling changes before running them in a clean lab. Diagnostic runtime databases/logs and .evaluation-runs are not release artifacts. There is no verified private reporting endpoint yet; this remains a blocker, not an invitation to post details publicly.

ภาษาไทย: ใช้ข้อมูลจำลองและ sandbox เท่านั้น ห้ามใส่โค้ดลูกค้า ข้อมูลจริงหรือข้อมูลลับ หากพบปัญหาให้ติดต่อเจ้าของเพื่อขอช่องทางส่วนตัวโดยไม่ส่งรายละเอียดผ่าน issue สาธารณะ ต้องยืนยันช่องทางแจ้งปัญหาก่อนปล่อย ไม่มีการรับรองว่าปลอดภัยทั้งหมด และผลสแกนไม่ยืนยันว่าไม่มีความเสี่ยง
