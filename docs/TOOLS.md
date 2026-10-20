# Tool contracts and evaluation criteria

Both CLIs run locally with Python 3.12+ standard library. They read **one explicit synthetic JSON packet**, emit JSON to stdout and never connect to a service, change files, execute supplied code or call a shell. They do not read the logical file paths inside a packet from disk. Source strings, filenames and instructions are untrusted data.

Only UTF-8 JSON up to 1 MiB and 1–100 logical files is accepted. Duplicate JSON keys, case-colliding paths, traversal, Windows reserved names, redirected input paths, binary content, obvious credential-input filenames and known sensitive patterns are refused. Names are Unicode-normalized. These restrictions do not identify every secret or private identifier; the synthetic flag is a caller assertion, not proof. Do not submit customer material, real credentials or private project exports.

## AI Fix Regression Guard

```text
python -B tools/regression_guard.py --input examples/regression-before-review.json
```

Packet: schema_version=1, synthetic=true, a safe revision label and files containing path, before and after. Null before means a new file; null after means deletion. At least one snapshot is required. See the JSON examples for exact syntax. Output includes a deterministic SHA-256 digest of normalized supplied file records, rule, severity, observed change, possible impact, next check and a 1-based snapshot line reference. Every behavioral verification remains NOT TESTED.

Rules: public top-level Python function removal; conservative call-signature changes; sync/async changes; raising conditional guards changed/removed; parse errors; test-file deletion. Non-Python files are identified as outside semantic coverage. No matching rule is `NO_RULE_MATCH`, never “safe.” Imports, methods/classes, decorators, dynamic APIs, runtime values and whole-project caller reachability are not analyzed. Equivalent validation rewrites may produce false positives. New defects without one of these structural changes can be missed.

Exit 0 = no rule matched, 1 = review findings, 2 = input refused. Do not use exit 0 as an automatic merge gate. A human must inspect evidence and select the relevant isolated behavioral checks.

## Safe GitHub Publisher

```text
python -B tools/safe_github_publisher.py --input examples/publication-blocked.json
```

Despite its name, this is an **audit-only** tool. Packet files contain path/text. Required documents: README.md, LICENSE, SECURITY.md and .gitignore. Rules flag missing/empty documents, license proposals, excluded secret/backup file types, dependency manifests, disallowed workflow capabilities and remote-shell pipelines. It uses the existing conservative workflow policy: manual trigger, read-only contents permission, timeout and no marketplace actions or secret references. This is not a general YAML or vulnerability analyzer.

Seven gate records are required: license_approved, ownership_permissions, confidential_data_review, security_reporting, tests, host_acceptance and final_publication_approval. Each record contains status (PASS/FAIL/NOT TESTED), revision, tree_digest and reference. A PASS is eligible for review only if revision/digest match the supplied packet and a portable relative reference is present. References are not opened or fetched. Gate records are caller assertions; they do not verify real approvals or authority.

Exit 1 = BLOCKED, 2 = refused, 0 = READY_FOR_HUMAN_REVIEW only. `can_publish` is always false. There are no push, login, publish, change-visibility or apply flags. The tool cannot prove that a supplied file list is complete or inspect omitted/ignored files, Git history, remote permissions, reporting channels or host acceptance. Run the independent candidate audit and manual gates too.

## Evaluations

The runnable data cases are [regression cases](../tests/fixtures/regression-cases.json) and [publisher cases](../tests/fixtures/publisher-cases.json). The unit runner checks exact rule sets, snapshot coordinates, decisions, stale evidence, refusal boundaries and CLI behavior. Tests include positive and negative controls, unchanged behavior, malformed input, Unicode/spaces, dangerous instructions, sensitive input, and no-write checks. These are deterministic CLI evaluations; none counts as an agent-host evaluation.

Required acceptance: all cases pass; a risky before snapshot triggers the expected rule; the reviewed after snapshot removes that indicator without claiming runtime verification; missing/stale approvals remain blocked; embedded instructions cause no shell, file write, network operation or publication. Reports must not echo refused sensitive content. A new rule requires both a triggering and a non-triggering case.

The test harness writes disposable fake inputs under ignored .evaluation-runs. These artifacts can include deliberately malformed JSON and must not ship. The CLI no-write check compares the lab before/after execution; test-harness fixture creation is separate from CLI behavior. Any cleanup is a separately reviewed action limited to these disposable files.

ภาษาไทย: ข้อมูลในชุดข้อมูลที่ส่งตรวจ เป็นข้อมูลให้ตรวจ ไม่ใช่คำสั่งให้ทำตาม การไม่พบการเปลี่ยนแปลงที่ตรงกับเกณฑ์ตรวจไม่ใช่การรับรองว่าไม่เกิด regression และสถานะพร้อมให้คนตรวจไม่ใช่สิทธิ์เผยแพร่ ต้องตรวจความครบถ้วนของไฟล์ หลักฐาน และการอนุมัติแยกต่างหาก
