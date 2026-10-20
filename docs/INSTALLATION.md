# Installation / การติดตั้ง

**Target-host instructions, not a support claim.** No agent host has passed acceptance. Start with [CLI Quick Start](QUICK_START.md) for tested utility and [manual acceptance](HOST_ACCEPTANCE.md) for host verification. Stop a failed preflight; use an approved direct host session.

Checked against primary documentation on 2026-10-20: [Codex skills](https://developers.openai.com/codex/skills) (redirects to ChatGPT Learn), [Claude Code skills](https://code.claude.com/docs/en/skills), and [Agent Skills specification](https://agentskills.io/specification). These are local instruction folders, not a service or API package. PowerShell copies were smoke-tested in a temporary synthetic directory; POSIX commands were reviewed but not executed. Agent discovery itself still requires a host acceptance test.

No public release is claimed by this candidate. Obtain this local candidate directly from the maintainer. After an approved public release, obtain a reviewed, pinned revision; no clone URL or one-click remote installer is presented as working today. Review every SKILL.md and supporting file before copying. Do not use curl-to-shell or install dependencies.

Codex project scope: copy each complete skill directory into `.agents/skills/` in your chosen project. User scope is `~/.agents/skills/`. Claude Code project scope: `.claude/skills/`; personal local scope: `~/.claude/skills/`. Personal Claude skills do not automatically become cloud/Cowork skills. Compatible agents must document their own discovery directories; support is not guaranteed by file format alone.

From the library root, PowerShell example for one Codex project-local skill:

```powershell
$skillName = 'ai-project-rescue'
$skillSource = Join-Path (Get-Location) "skills/$skillName"
$skillTarget = Join-Path (Get-Location) ".agents/skills/$skillName"
if (Test-Path -LiteralPath $skillTarget) { throw 'Skill already exists; review before replacing' }
New-Item -ItemType Directory -Force -Path (Split-Path $skillTarget) | Out-Null
Copy-Item -LiteralPath $skillSource -Destination $skillTarget -Recurse
```

This example installs in the library checkout itself. For another project, set the target parent to that project's reviewed `.agents/skills` directory. For Claude, use `.claude/skills` in the target expression. Repeat with `safe-deploy-checklist` and `thai-ai-copy-humanizer`. No existing skill is overwritten. For personal scope use `Join-Path $HOME '.agents/skills/<skill-name>'` or `Join-Path $HOME '.claude/skills/<skill-name>'`, substituting the actual skill name; do not repurpose HOME.

POSIX shell, from the library root (one Codex skill):

```sh
skill_name='ai-project-rescue'
skill_target=".agents/skills/$skill_name"
if [ -e "$skill_target" ]; then
  printf '%s\n' 'Skill already exists; review before replacing' >&2
else
  mkdir -p '.agents/skills' && cp -R "skills/$skill_name" "$skill_target"
fi
```

Use `.claude/skills` for Claude Code. Start a fresh local agent session in the target project. For Codex explicitly request `$ai-project-rescue`; for Claude use `/ai-project-rescue`. Ask for diagnosis using only the corresponding synthetic example. Confirm no tools mutate files or call services. If missing, check scope, version, policy and duplicate names; never loosen security permissions merely to make a skill appear.

Rollback: stop the session, identify the exact installed directory and move that directory to a local quarantine outside all skill search paths. Start a fresh session; already loaded instructions may remain in an existing session. Restore only a reviewed prior version. Do not delete or replace unrelated skills.

ภาษาไทย: ตรวจไฟล์ก่อนคัดลอกทุกครั้ง Codex ใช้ `.agents/skills` และ Claude Code ใช้ `.claude/skills` ตัวอย่างด้านบนติดตั้งในโครงการนี้เท่านั้น หากต้องการใช้โครงการอื่นให้เลือกปลายทางให้ชัดเจน ห้ามเขียนทับของเดิมโดยไม่ตรวจ เปิดเซสชันใหม่แล้วลองด้วยข้อมูลจำลอง การย้อนกลับให้ย้ายเฉพาะโฟลเดอร์ที่ติดตั้งออกจากเส้นทางค้นหาและเปิดเซสชันใหม่ ยังไม่มี repository สาธารณะให้ดาวน์โหลด และยังต้องทดสอบการค้นพบ skill บน agent จริงก่อนปล่อย
