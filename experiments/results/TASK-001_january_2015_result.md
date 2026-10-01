# TASK-001 — January 2015 H0 Result

## Status

COMPLETED — January reproducibility stage

## Experiment

- Task: TASK-001
- Experiment: EXP-2015-001
- Instrument: EURUSD
- Research window: January 2015
- Signal timeframe: 15m
- Holding horizon: 60m
- Random seed: 20150101

## Locked execution methodology

- Signal information available only at completed 15m bar close.
- Entry is the next available tick strictly after signal close.
- Exit is the first available tick at or after the 60m target.
- LONG entry uses ASK and exit uses BID.
- SHORT entry uses BID and exit uses ASK.
- Gross P&L is calculated from mid prices.
- Net P&L is calculated using executable bid/ask prices.
- Trades are non-overlapping.
- No synthetic gap interpolation was used.
- Partial 15m bars were excluded.
- The existing full-year seeded RNG sequence was preserved; January trades were taken as the January slice of that authoritative run.

## January 2015 result

- N: 403
- Mean net P&L: -8.096774 pips/trade
- Median net P&L: -8.000000 pips/trade
- Standard error: 9.523807
- 95% CI: [-26.763435, 10.569887] pips/trade
- Hit rate: 46.8983%
- Gross P&L: -1682.500000 pips
- Net P&L: -3263.000000 pips
- Cost drag: 1580.500000 pips
- Profit factor: 0.878685

## Reproducibility verification

The January reference report:

`reports/h0_random_15m_60m_2015_01.csv`

was independently reproduced from the full-year H0 execution:

`src/h0_random_january_2015.py`

The independently generated January reproduction:

`reports/h0_random_15m_60m_2015_01_reproduction.csv`

contained exactly 403 trades.

Trade-by-trade comparison result:

`EXACT TRADE-FOR-TRADE MATCH`

The two January files were also verified byte-for-byte identical.

SHA-256:

`747f3d7c10b013e39cdcf8a46b1daadca2aff8f7640dd3e381c6b724b9c95284`

for both files.

## Interpretation

This result is a reproducibility result for the January 2015 slice of EXP-2015-001. It is not evidence of a predictive trading edge.

The January net result was negative under the locked executable bid/ask methodology. The 95% confidence interval includes zero.

No research rule, execution rule, cost rule, random seed, or information boundary was changed for this reproduction.

## Remaining TASK-001 audit stages

The January result should be independently reviewed by:

1. Statistical Auditor
2. Execution/Cost Auditor
3. Adversarial Falsifier

Only after those audits should the research lead close TASK-001 and proceed to subsequent hypotheses.
