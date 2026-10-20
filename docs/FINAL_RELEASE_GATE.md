# Public release gate — v0.1.0-rc.1

**NO-GO for public release.** Content-selection review and a local commit are not publication authority. Private upload permission does not authorize public visibility, a release or announcements.

| Required gate | Status | Required evidence |
| --- | --- | --- |
| Effective license and contribution rights | NOT APPROVED | Owner attests rights, holder/year and complete license text. Current LICENSE is only a proposal; see LICENSE_REVIEW.md and PROVENANCE.md. |
| Target ownership and effective permissions | NOT VERIFIED FOR PUBLIC RELEASE | Owner verifies the exact target and public-release scope without exposing unrelated private inventory. |
| Confidentiality review | Selected public-content review completed | Review exact index blobs and manifest again after changes; scans cannot guarantee absence of secrets or private data. Internal diagnostics and approval working records are excluded. |
| Private vulnerability reporting | NOT VERIFIED | Establish a monitored private route before public approval; follow PRIVATE_VULNERABILITY_REPORTING.md. Do not publish exploit details. |
| Automated validation | Must pass on exact selected snapshot | Run the packaged tests and audit; retain sanitized results. Passing static checks is not a security guarantee or host acceptance. |
| Agent-host acceptance | NOT TESTED | No agent host is supported. Use HOST_ACCEPTANCE.md and MANUAL_ACCEPTANCE_SUITE.md; collect actual outputs per host/version. |
| Cross-platform and hosted workflow acceptance | NOT TESTED | Local deterministic checks do not establish other OS or GitHub-hosted behavior. |
| Explicit public publication approval | NOT GIVEN | Owner approves exact revision, repository, visibility, push/tag/release and announcement scope. |

Local diagnostic evidence and approval records are intentionally not part of the public source tree. RC_MANIFEST.json is a public-content allowlist, not proof of rights, security or approval. Inspect all reachable Git history and the final staged/exported tree before any later approved push. A source change invalidates prior hashes and requires another review.

Residual risks include incomplete pattern detection, omitted input files, unverified caller assertions, prompt injection at the host boundary and untested runtime behavior. No guarantee of complete security is made.

ภาษาไทย: ชุดไฟล์ที่ผ่านการตรวจเนื้อหายังไม่ใช่การอนุมัติเปิด Public ต้องยืนยันสิทธิ์และ License ช่องทางแจ้งปัญหา ผลทดสอบจริง และคำอนุมัติสำหรับรุ่นที่จะเผยแพร่ก่อน
