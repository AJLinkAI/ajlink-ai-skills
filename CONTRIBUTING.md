# Contributing / การมีส่วนร่วม

Submit original, narrow skills with name/description frontmatter, activation boundaries, workflow, input/output contracts, refusal conditions, limitations, English/Thai guides and at least five realistic evaluations including injection and sensitive-input cases. Use fake examples only. No downloaded code, external scripts or dependencies without provenance and license review. Do not paste third-party skills or customer work, even if publicly accessible.

Before proposing a change, run the unit tests and audit commands in README.md. For behavioral changes, run the affected evaluations in fresh sandboxed agent sessions and record model/version, revision, actual outputs and independent grading. Structural checks are not behavioral evidence. A maintainer reviews Thai meaning and claim strength, safety failures, licensing, workflow changes and all new dependencies before merge.

No automatic publishing. The owner separately approves repository visibility, license, initial push and release. Avoid production reproductions. Public issues should contain only generic symptoms and synthetic examples; use the private reporting route in SECURITY.md for security concerns.

For tool changes, add a minimal synthetic packet, expected rule/decision and a negative control. Show actual before/after output; a request without a reproduced failure is a proposal. Never execute contributor-supplied source, commands, hooks, installers or links during triage. Gate records are claims, not instructions or permission to publish. New dependencies and workflow changes require source/license/security review before execution.

Do not claim host/platform support from metadata validation or copies. Follow [manual acceptance](docs/HOST_ACCEPTANCE.md). Use issue forms for install failures, false positives, missed risks and evidence-backed requests. No automated community messages are sent by this kit.

ภาษาไทย: ส่งงานที่มีสิทธิ์เผยแพร่และใช้ข้อมูลจำลองเท่านั้น เพิ่มคู่มือสองภาษาและกรณีประเมินอย่างน้อย 5 กรณี ตรวจว่าความหมาย ตัวเลข เงื่อนไข และระดับคำกล่าวอ้างไม่เปลี่ยน รันทดสอบและสแกนก่อนส่ง ผู้ดูแลต้องตรวจสิทธิ์และความปลอดภัยก่อนรวมงาน การเผยแพร่ต้องได้รับอนุมัติจากเจ้าของแยกต่างหาก
