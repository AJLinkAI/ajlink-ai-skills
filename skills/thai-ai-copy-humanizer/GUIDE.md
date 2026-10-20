# thai-ai-copy-humanizer: English guide

Input: ทางเรามีความยินดีที่จะทำการแจ้งให้ท่านทราบว่า เวิร์กช็อปใช้เวลาประมาณ 2 ชั่วโมง และอาจช่วยลดเวลาเตรียมงานได้. Rewrite: เวิร์กช็อปใช้เวลาประมาณ 2 ชั่วโมง และอาจช่วยลดเวลาเตรียมงานได้. Preserve อาจ and ประมาณ 2 ชั่วโมง; add no guarantee. The input explicitly attaches the duration to the workshop to avoid silently resolving an ambiguous sentence.

Activation, required inputs, output format, refusal conditions and workflow are defined in [SKILL.md](SKILL.md). Use sanitized synthetic inputs only. This package contains instructions, not permission enforcement or executable repair tools.

Limitations: Naturalness is subjective and dialect-dependent. Does not establish factual accuracy, legal suitability or human authorship. Specialist claims require specialist review.

Read [Thai guide](GUIDE.th.md). To evaluate, run each case in [evaluations.json](evaluations.json) in a fresh agent session with this skill loaded. Give only the input to the agent; grade required behavior and forbidden behavior separately. Any forbidden action fails the case. Record model/version, date, skill revision, actual output and grader rationale. Do not count structural tests as agent behavior tests.
