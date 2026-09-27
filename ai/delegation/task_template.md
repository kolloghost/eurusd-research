# Multi-AI Task Template

## Task identity

- Task ID:
- Experiment ID:
- Assigned role:
- Agent/model:
- Branch:
- Starting commit:
- Date/time started (UTC):

## Objective

Describe the single research question or engineering task to be answered.

## Source of authority

Primary documents:

- `QUANT_FX_CFD_MASTER_AI_HANDOFF_UPDATED.md`
- `research/research_rules.yaml`
- Role:
- Protocol:
- Experiment specification:

## Scope

- Instrument:
- Data source/type:
- Timeframe:
- Date range:
- Session:
- Holding horizon:
- Development / validation / OOS status:
- Relevant broker/CFD scope, if any:

## Locked constraints

State the specific execution, cost, data-quality, and information-boundary rules that must not be changed.

## Allowed work

Describe exactly what the agent is allowed to inspect, calculate, code, test, or modify.

## Prohibited work

Examples:

- No result-driven parameter tuning
- No changing the hypothesis
- No OOS inspection when OOS is protected
- No mixing OTC and CFD results
- No silent data cleaning
- No fabricated or guessed values
- No committing unrelated changes

## Deliverables

Specify the exact files, report, statistics, tests, or audit findings expected.

## Reproducibility requirements

Record:

- Exact command(s)
- Python version
- Platform
- Random seed
- Input files
- Code commit/hash
- Output files
- Validation checks

## Completion criteria

The task is complete only when:

- [ ] Correct source files were used
- [ ] Locked rules were preserved
- [ ] Calculations were executed reproducibly
- [ ] Outputs were saved
- [ ] Validation checks passed or failures were documented
- [ ] Result submission was completed
- [ ] No unsupported conclusion was presented
