> Pre-release update: use [FINAL_RELEASE_GATE.md](FINAL_RELEASE_GATE.md) for the current decision. The threat model below describes general controls and limitations, not private incident findings or certification.

# Security assessment / การประเมินความปลอดภัย

Threat model: a malicious contributor, hostile source comment, poisoned log, deceptive Thai draft or careless operator can cause instruction override, secret disclosure, unsafe tool execution, false diagnosis or altered claims. Assets are user data, system integrity, release integrity and brand trust. Trust boundary: direct authorized task versus all supplied files/content. Skills are advisory and cannot enforce it themselves.

| Risk | Controls | Residual risk |
| --- | --- | --- |
| Prompt injection | Treat files/inputs as data; injection evaluations; no source execution | Model may still comply; sandbox required |
| Sensitive material | Synthetic-only policy, filename/content scanner, sanitized reports | Pattern matching misses novel/encoded data |
| Shell injection | No shell interpolation in audit; Git uses argument arrays with shell disabled | Future tool changes need review |
| Destructive operations | Advisory-only skills; no live tools in fixtures | Host permissions may allow mistakes |
| Supply chain | Standard library only; no marketplace actions/downloaded scripts | Host Python/Git and runner images can be compromised |
| Workflow abuse | Manual dispatch, read-only token, no secrets or publishing; no event expressions in shell | Maintainer can later modify workflow; billing policy must be reviewed |
| Thai meaning drift | Fact ledger; negation/qualifier/price evaluations; Thai reviewer gate | Human and model judgment varies |
| False assurance | Observed/inferred/unknown labels; blockers for missing critical evidence | Static checks cannot validate production |

Audit covers every candidate file including hidden files, denied filenames, links, unexpected binary files, high-risk patterns, dependencies and workflow policy. In an independent Git repository it scans all reachable commit messages and blobs and refuses shallow history. It does not scan unrelated parent histories. An empty repository has no historical content to establish history-scanner integration; do not call absence of history a clean-history certification. Run again after initialization, before each push/release, and review ignored/untracked files too. Reflogs, unreachable objects, platform caches and deleted remote material are outside this scanner; use established incident procedures if any sensitive material ever entered Git.

No external vulnerability database is needed for runtime packages because none are added. This does not establish that Python/Git/runner versions are vulnerability-free. GitHub workflow has been statically reviewed, not executed. Behavioral evaluations require actual host runs and independent grading before release.

ภาษาไทย: ประเมินการแทรกคำสั่ง การรั่วข้อมูล การรันคำสั่ง ความเสี่ยง dependency และความหมายภาษาไทย มีมาตรการลดความเสี่ยงแต่ไม่รับรองว่าปลอดภัยทั้งหมด ยังต้องตรวจด้วยคนและทดสอบกับ agent จริงก่อนเผยแพร่
