# Multi-AI Delegation

This directory is the operational layer for assigning controlled research tasks to independent AI agents.

## Documents

- `master_prompt.md` — shared instructions every agent receives
- `task_template.md` — task packet used to delegate one bounded task
- `result_submission_template.md` — structured return format for completed work

## Recommended orchestration

1. Research Lead — define/confirm the bounded task and experiment ID.
2. Data Engineer — verify dataset integrity, provenance, transformations, and available coverage.
3. Quant/Backtest Agent — implement or execute the specified experiment.
4. Statistical Auditor — independently recalculate and audit inference.
5. Execution/Cost Auditor — challenge executable pricing and cost treatment.
6. Adversarial Falsifier — search for leakage, selection effects, instability, and alternative explanations.
7. Replication Auditor — test the pre-specified replication scope when authorized.
8. Research Lead — synthesize only the independently supported evidence.

The order may be adapted, but independent audits should be performed before agents are shown each other's conclusions where practical.

## Governance

The AI agents do not own the research rules. Locked rules are changed only through the project's approved human-governance process.

The system is designed to make disagreement visible. Multiple agents reaching the same conclusion is supporting evidence only when their work is independently grounded in the underlying files and calculations.
