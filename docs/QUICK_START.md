# Quick Start — local, synthetic, read-only

Current state: local `v0.1.0-rc.1`, unpublished, NO-GO. No public download URL or accepted agent-host claim is made. Use an existing Python 3.12+ interpreter; no pip packages, API keys or agent subscription are needed for these two tool demos. If your `python` command is a Store alias or unavailable, stop and choose an existing approved interpreter. Choose an already-approved interpreter; this guide does not authorize installation.

From the reviewed project folder:

```powershell
python --version
python -B tools/regression_guard.py --input examples/regression-before-review.json
```

Expected: `REVIEW_REQUIRED`, `RAISING_GUARD_CHANGED`, exit **1**. This exit is an intentional review signal, not a crash. The report cites `demo/price.py`, the before snapshot and line 2. No supplied code or tests run.

```powershell
python -B tools/regression_guard.py --input examples/regression-after-review.json
```

Expected: `NO_RULE_MATCH`, exit **0**. The synthetic proposed fix retains the original guard. This is a static before/after demonstration, not proof of runtime correctness.

```powershell
python -B tools/safe_github_publisher.py --input examples/publication-blocked.json
```

Expected: `BLOCKED`, `can_publish: false`, exit **1** because approval/acceptance evidence is absent. Do not change statuses merely to get exit 0. A second synthetic fixture, publication-recorded-review.json, demonstrates only how caller-supplied records can reach human review; it is not a real license, ownership or release approval.

On a POSIX shell, use an existing Python 3.12+ command such as `python3` with the same arguments. Linux/macOS execution and their shell examples remain NOT TESTED here. No remote installer is provided.

Run the reviewed repository tests:

```powershell
python -B -m unittest discover -s tests -v
python -B tools/audit.py
```

For data contracts and limits, read [tool reference](TOOLS.md). For the three advisory skills, see [installation](INSTALLATION.md) and [manual host acceptance](HOST_ACCEPTANCE.md). A skill copy test does not establish host support.

ภาษาไทย: เริ่มจากตัวอย่างจำลองด้านบน รหัสจบการทำงาน 1 หมายถึงต้องตรวจต่อหรือยังปล่อยไม่ได้ ไม่ใช่ให้ลบข้อเตือนเพื่อให้คำสั่งผ่าน เครื่องมือไม่แก้ไฟล์ ไม่รันโค้ดที่ส่งเข้าไป และไม่เชื่อม GitHub
