# Before/after demo evidence

All examples are synthetic. The table states synthetic fixture expectations. Reproduce them using the packaged commands and record your own actual outputs and exits; private execution transcripts are not distributed. No model host, application code or tests supplied inside a packet are executed by either review tool.

| Scenario | Before review | After a human's proposed revision | Scope of evidence |
| --- | --- | --- | --- |
| Negative amount guard | Python price function loses its negative-input rejection guard; tool reports RAISING_GUARD_CHANGED at before line 2 | The second packet retains the original guard; tool reports NO_RULE_MATCH | Static indicator changes as expected; does not demonstrate application runtime correctness |
| Missing release approvals | Synthetic gate records are NOT TESTED; tool reports BLOCKED and can_publish=false | Fully populated fake matching records reach READY_FOR_HUMAN_REVIEW; can_publish stays false | Demonstrates record freshness checks, not real approvals, ownership or a valid license |

The synthetic packet's file reference is demo/price.py; it is a logical snapshot name, not a real project or customer path. No source patch was applied by a tool. The human-selected after fixture already contains the reviewed state.

Reproduce with the commands in [Quick Start](QUICK_START.md). The first and blocked-publication commands intentionally return exit 1; the unchanged-control and recorded-review commands return exit 0. Input refusal returns 2. Do not treat those codes as permission to merge, publish or deploy.

Regression-rule positive and negative controls plus publisher blocked/recorded/stale controls are checked by the unit suite. Unsupported-language coverage is explicitly marked NOT TESTED in the regression report. No made-up client testimonial, saved-time statistic or supported-host claim is used.

ภาษาไทย: ตารางนี้แสดงว่าผลตรวจเปลี่ยนตามข้อมูลจำลองที่ตั้งใจเปลี่ยน ไม่ได้พิสูจน์ว่าโปรแกรมจริงไม่มีบั๊กหรือพร้อมปล่อยงาน แม้ชุดข้อมูลตัวอย่างจะระบุ PASS ครบทุกข้อ เครื่องมือก็ยังไม่ให้สิทธิ์เผยแพร่
