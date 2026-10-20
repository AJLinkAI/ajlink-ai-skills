# Architecture / สถาปัตยกรรม

Propose a NEW independent repository: `AJLinkAI/ajlink-ai-skills`. Keep the local candidate outside existing Git histories. Canonical sources live under `skills/<name>/SKILL.md`; installation copies complete directories into the host's documented discovery root. No duplicate generated skill trees, agent-specific frontmatter, hooks, APIs, inference service, billing or production adapters.

Use the portable Agent Skills subset: YAML frontmatter with name matching the directory and a concise description, followed by Markdown instructions. A license field is intentionally absent while licensing is pending. English entrypoints support cross-agent discovery; Thai guides explain usage and boundaries. At least six JSON evaluations per skill are data, never executable commands. Python standard-library tooling validates structure and audits text, filenames, history and workflow policy.

`docs/` contains sanitized findings, provenance, security assessment, release readiness, roadmap and launch plan. `examples/` contains fake inputs and expected behavior. `tests/` contains deterministic checks of packaging, injection fixtures and scanner behavior. `.github/workflows/` contains manually triggered validation only. No workflow publishes artifacts or deploys.

ภาษาไทย: แยก repository ใหม่ ใช้ SKILL.md เป็นแหล่งหลัก คัดลอกทั้งโฟลเดอร์ตามเส้นทางของแต่ละ agent ไม่เชื่อมระบบจริง ตัวอย่างและข้อมูลประเมินเป็นข้อมูลจำลองทั้งหมด เครื่องมือตรวจใช้ Python มาตรฐาน และ workflow ต้องสั่งรันเอง
