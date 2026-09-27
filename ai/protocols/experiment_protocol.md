# Experiment Protocol

## Purpose

Define the controlled specification required before executing any quantitative
FX experiment.

An experiment is a measurement procedure, not an optimization loop.

## Experiment Freeze

Before execution record:

- experiment ID
- hypothesis
- mechanism
- predictor
- target
- market
- timeframe
- date range
- session
- signal timing
- entry rule
- exit rule
- holding horizon
- trade-selection rule
- cost model
- statistical method
- random seed where applicable
- acceptance/failure criteria

After execution begins, do not change these items because of observed results.

## Hypothesis

State the hypothesis in falsifiable form.

Include:

- measurable input
- expected relationship
- direction if applicable
- target horizon
- expected economic mechanism
- conditions under which the hypothesis would fail

Avoid vague claims such as "the market is predictable."

## Measurement

Define precisely:

- units
- sampling interval
- feature formula
- thresholds
- lookback
- target-return formula
- treatment of missing observations
- treatment of partial bars

All transformations must be deterministic.

## Information Boundary

The experiment may use only information available at signal time.

The completed signal bar is the default signal boundary.

Any data generated after that boundary must be excluded from the signal.

## Trade Construction

Default execution:

- signal at completed bar close
- entry at next available tick
- exit at first tick at or after target horizon

Long:

- ask entry
- bid exit

Short:

- bid entry
- ask exit

Record whether trades overlap.

## Data Selection

Record:

- exact source
- file/version
- date range
- instrument
- timeframe
- data-quality filters
- excluded observations
- exclusion rationale

Do not silently remove difficult observations.

## Costs

Calculate separately:

gross return
net return
cost drag

Include applicable:

- spread
- commission
- slippage
- delay
- impact
- financing

Use frozen base/adverse/stress assumptions where defined.

## Baseline

Every experiment requires an appropriate baseline.

The baseline must use compatible:

- data
- timing
- execution
- costs
- trade-selection structure

The baseline should answer whether the proposed feature adds information beyond
the underlying executable process.

## Non-Overlap

Prefer non-overlapping trades for primary inference.

If overlapping trades are necessary:

- document the overlap
- account for dependence
- use appropriate inference

## Statistical Outputs

At minimum report:

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

Also inspect:

- return distribution
- skew
- tails
- temporal concentration
- dependence

## Multiple Testing Record

Record all variants tested.

Variants include:

- thresholds
- lookbacks
- holding periods
- sessions
- instruments
- timeframes
- cost assumptions
- feature transformations

Exploratory searches must not be presented as pre-specified confirmation.

## Robustness

If an experiment produces a potentially interesting result, test pre-defined
robustness dimensions.

Do not redesign the hypothesis after seeing the result.

## OOS

An experiment must state whether its data belong to:

- development
- validation
- untouched OOS
- paper/live research

Untouched OOS data must not be used for tuning.

## Failure Conditions

Flag the experiment if:

- look-ahead bias is detected
- execution is unrealistic
- costs are omitted or understated
- data exclusions are unexplained
- parameters changed after results
- only favorable variants are reported
- OOS data were used for tuning
- the result cannot be reproduced

## Required Experiment Output

Return:

1. experiment ID
2. hypothesis
3. mechanism
4. dataset
5. measurement
6. execution
7. costs
8. baseline
9. sample
10. results
11. inference
12. robustness
13. multiple-testing record
14. OOS status
15. reproducibility status
16. limitations
17. conclusion
