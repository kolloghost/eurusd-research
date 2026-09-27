# Research Protocol

## Purpose

Define the controlled workflow for investigating whether a measurable variable
contains incremental information about subsequent EURUSD returns and whether
any observed relationship survives realistic costs, robustness testing,
replication, and untouched out-of-sample evaluation.

The research process must distinguish:

- observation
- mechanism
- hypothesis
- measurement
- baseline
- backtest
- cost adjustment
- robustness
- replication
- out-of-sample validation
- paper trading
- falsification
- conclusion

Do not skip stages.

## Research Objective

The objective is not to maximize backtest performance.

The objective is to determine whether evidence supports a reproducible,
economically meaningful, executable relationship.

A result must survive:

1. correct information timing
2. realistic execution
3. realistic costs
4. statistical scrutiny
5. robustness testing
6. multiple-testing controls
7. independent replication where applicable
8. untouched out-of-sample evaluation

## Market Scope

Primary instrument:

- EURUSD

Replication instruments:

- GBPUSD
- AUDUSD

Primary timeframe:

- 15m

Replication timeframes:

- 30m
- 1h

Internal timezone:

- UTC

Primary session:

- London/New York overlap

Session boundary definitions remain an explicit research question until
formally specified.

Do not silently change the market, timeframe, session, or sample.

## Data Hierarchy

Preferred sources:

1. same-broker CFD bid/ask data
2. independent OTC tick data
3. CME centralized FX data

Broker-specific datasets remain separate.

Record:

- provider
- instrument
- dataset version
- date coverage
- timestamp convention
- bid/ask availability
- transformation process
- quality limitations

## Data Quality

Check:

- duplicate timestamps
- out-of-order timestamps
- missing values
- invalid prices
- bid greater than ask
- nonpositive spreads
- abnormal spreads
- stale quotes
- weekend and holiday gaps
- rollover effects
- timestamp consistency
- cross-source consistency

Use UTC internally.

Do not interpolate missing market observations.

Do not silently delete extreme observations.

Document every exclusion.

## Signal Integrity

A signal may use only information available at or before the completed
signal bar.

No future price, future bar, future spread, future volume, or future label may
enter the signal definition.

Signal construction must be deterministic and reproducible.

## Execution

Unless an experiment explicitly documents an approved variation:

Signal:
- completed signal bar close

Entry:
- next available tick

Exit:
- first tick at or after holding horizon

Long:
- ASK entry
- BID exit

Short:
- BID entry
- ASK exit

Avoid overlapping trades unless overlap is explicitly part of the experiment.

## Cost Model

Separate:

- gross return
- net return
- cost drag

Where applicable include:

- spread
- commission
- slippage
- delay
- market impact
- financing

Use documented:

- base
- adverse
- stress

cost scenarios where data permit.

## Baselines

Every strategy experiment must have an appropriate baseline.

At minimum consider:

- random executable baseline
- unconditional return baseline
- simple directional baseline where relevant
- placebo or permutation baseline where appropriate

A strategy must demonstrate incremental information rather than merely positive
returns.

## Statistical Requirements

Report:

- N
- mean
- median
- standard error
- confidence interval
- hit rate
- expectancy
- profit factor where meaningful
- drawdown
- turnover
- exposure
- gross return
- net return
- cost drag
- return distribution
- skew
- dependence

Use dependence-aware inference where observations overlap or are otherwise
non-independent.

Possible methods include:

- robust standard errors
- clustered standard errors
- block bootstrap
- permutation tests

The statistical method must be documented before interpreting the result.

## Multiple Testing

Record:

- hypotheses tested
- features tested
- thresholds tested
- holding periods tested
- sessions tested
- instruments tested
- timeframes tested
- cost variants tested

Do not repeatedly modify an experiment until a favorable result appears.

Exploratory variants must be explicitly labeled exploratory.

## Robustness

Promising results must be tested across relevant dimensions without selecting
only successful variants.

Examples:

- adjacent thresholds
- adjacent holding periods
- different years
- different sessions
- alternative but justified measurements
- independent instruments
- independent data sources
- adverse cost assumptions

Robustness testing is not an invitation to optimize.

## Out-of-Sample Protection

Use the provisional temporal design:

- 2015-2020 development
- 2021-2023 validation
- 2024-2025 untouched OOS
- 2026 onward paper/live research

Do not inspect or tune against untouched OOS observations.

If OOS contamination occurs, document it.

## Reproducibility

Every experiment must have:

- unique experiment ID
- frozen specification
- input dataset
- code version
- parameters
- random seed where applicable
- output report
- execution model
- cost model
- statistical method

A result that cannot be reproduced is not considered complete evidence.

## Evidence Classification

Results must be reported descriptively.

Use distinctions such as:

- positive observation
- negative observation
- inconclusive
- statistically significant
- economically significant
- cost-sensitive
- fragile
- robust
- replicated
- failed replication

Do not collapse statistical significance and economic significance into one
claim.

## Required Research Record

Each completed experiment must preserve:

1. hypothesis
2. rationale/mechanism
3. data
4. measurement
5. execution
6. costs
7. baseline
8. results
9. statistical inference
10. robustness
11. multiple-testing status
12. replication status
13. OOS status
14. limitations
15. conclusion
