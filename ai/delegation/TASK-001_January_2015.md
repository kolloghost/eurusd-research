# TASK-001 — January 2015 Controlled Research Start

## Task identity

- Task ID: `TASK-001`
- Experiment family: `EXP-2015-001` and subsequent January H0–H4 experiments
- Assigned role: Research Lead / Quant Research Coordinator
- Research window: **January 2015 only**
- Instrument: EURUSD
- Timezone: UTC
- Status: READY
- OOS status: DEVELOPMENT / REFERENCE ONLY

## Objective

Establish January 2015 as the first controlled multi-AI research window.

The agent must verify the actual January 2015 data and derived datasets in the repository, reproduce the January executable random baseline under the already locked H0 rules, and prepare the evidence required for independent statistical, execution/cost, and adversarial audits.

This task is not permission to redesign the research.

## Authoritative project documents

Read these before substantive work:

1. `QUANT_FX_CFD_MASTER_AI_HANDOFF_UPDATED.md`
2. `research/research_rules.yaml`
3. `ai/roles/research_lead.md`
4. `ai/protocols/research_protocol.md`
5. `ai/protocols/experiment_protocol.md`
6. `ai/protocols/result_protocol.md`
7. `ai/delegation/master_prompt.md`
8. `ai/delegation/result_submission_template.md`
9. `experiments/specs/EXP-2015-001_h0_random_executable.yaml`

Use the actual repository files and Git history to establish current state.

## January scope

The first research window is strictly:

- Start: `2015-01-01`
- End: `2015-02-01` exclusive
- Instrument: EURUSD
- Primary signal timeframe: 15 minutes
- H0 horizon: 60 minutes
- Full trading day unless an existing locked specification states otherwise
- UTC internally
- January data only for this task

**Do not add February 2015 to this task.**

## Locked H0 execution model

Preserve the existing H0 specification:

- Signal becomes available only at the completed 15m bar close.
- Use only complete 15m bars.
- Entry is the next available tick strictly after signal close.
- LONG entry = ASK.
- LONG exit = BID.
- SHORT entry = BID.
- SHORT exit = ASK.
- Exit = first available tick at or after the 60-minute target.
- No overlapping trades for the baseline.
- Keep gross mid-price P&L and executable net bid/ask P&L separate.
- Do not interpolate missing ticks.
- Do not silently remove extreme spreads or prices.
- Use the existing fixed random seed: `20150101`.

## Required work

### A. Establish repository state

Record:

- current branch
- current commit
- whether the branch is tracking the expected remote branch
- relevant Git history
- Python version
- platform

Do not stage or commit unrelated files.

### B. Verify January raw data

Inspect the actual January raw EURUSD file(s), expected under:

```text
data/eurusd/2015/
```

Confirm, using the repository's existing validation/manifest machinery where applicable:

- file identity
- row count
- header/schema
- timestamp range
- duplicate timestamps
- out-of-order rows
- invalid prices
- bid greater than ask
- non-positive spreads
- obvious timestamp/data-quality anomalies

Do not silently repair data.

### C. Verify January derived data

Inspect:

```text
data/normalized/eurusd/2015/
data/bars/eurusd/2015/
data/bars15/eurusd/2015/
```

where present.

Confirm that the January derived data corresponds to the January raw data and that:

- normalized timestamps are UTC
- no synthetic ticks were introduced
- 15m bars use the project's existing bar-building rules
- incomplete/partial bars are handled according to the locked rules

### D. Reproduce January H0

Use the existing H0 implementation where applicable.

Do not modify H0 semantics merely to obtain a desired result.

Produce a **January-only** trade report with at least:

```text
month
signal_close
entry_timestamp
exit_timestamp
direction
entry_price
exit_price
gross_pips
net_pips
cost_drag_pips
```

Calculate and report:

- N
- mean net P&L
- median net P&L
- sample standard error
- 95% CI using the experiment's specified method
- hit rate
- gross P&L
- net P&L
- cost drag
- profit factor, where meaningful
- maximum drawdown, if available from the established reporting framework

### E. Recalculate independently

Independently recompute the key January H0 summary from the saved January trade log rather than trusting only the script's printed output.

At minimum independently verify:

- N
- mean
- median
- standard error
- confidence interval
- hit rate
- gross P&L
- net P&L
- cost drag
- profit factor

Any mismatch must be reported, not silently reconciled.

## H0 comparison rule

The existing full-year 2015 H0 result is a separate reference checkpoint.

Do **not** replace or rewrite it.

If the January result cannot be reconciled with the full-year report through ordinary aggregation because different report scopes are involved, state that clearly.

Do not claim that January is representative of all 2015 from January alone.

## Restrictions

The agent must NOT:

- add February or later months
- change the random seed
- change signal timing
- change entry/exit bid/ask rules
- change the holding horizon
- change overlap policy
- tune parameters to January
- inspect protected OOS periods
- mix CFD data with OTC data
- invent missing provenance
- delete extreme observations without an approved rule
- declare an edge, robustness, or profitability from this task alone
- modify locked research rules
- commit unrelated files

## Deliverables

Create or update only the files needed for this January task, preferably under:

```text
reports/
experiments/results/
tests/
```

Suggested artifacts:

```text
reports/h0_random_15m_60m_2015_01.csv
experiments/results/TASK-001_january_2015_result.md
```

If an existing implementation cannot cleanly produce a January-only report without changing semantics, create the smallest dedicated wrapper/analysis needed and document it.

## Reproducibility record

The final submission must contain:

- exact command(s) executed
- branch
- commit/hash used
- Python version
- platform
- random seed
- input paths
- output paths
- validation commands and outcomes

## Required final submission

Use:

`ai/delegation/result_submission_template.md`

The final report must distinguish:

1. Observed data facts
2. Independently calculated results
3. Interpretation
4. What January 2015 does **not** establish
5. Any unresolved discrepancy
6. Exact next action

## Completion criteria

- [ ] January scope only
- [ ] Raw data verified
- [ ] Derived data verified
- [ ] H0 execution model preserved
- [ ] January H0 trade log produced
- [ ] Key statistics independently recalculated
- [ ] No unsupported strategy conclusion
- [ ] Reproducibility information recorded
- [ ] Result submission completed

## Handoff to next agents

After TASK-001 is complete, provide the resulting evidence to independent agents in this order where practical:

1. Statistical Auditor — independently audit the January numbers and inference.
2. Execution/Cost Auditor — independently challenge bid/ask and cost treatment.
3. Adversarial Falsifier — search for leakage, selection, data-quality, and stability issues.
4. Quant Research agent(s) — only after the baseline evidence is clean, run the pre-specified January H1–H4 experiments.
5. Research Lead — synthesize only independently supported evidence.

Do not give one auditor another auditor's conclusions before their independent pass where practical.
