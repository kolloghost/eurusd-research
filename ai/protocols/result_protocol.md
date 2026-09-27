# Result Protocol

## Purpose

Standardize how quantitative FX research results are recorded and interpreted.

Results must preserve negative, null, and inconclusive findings.

## Result Identity

Every result must identify:

- experiment ID
- code/version
- dataset
- instrument
- timeframe
- date range
- session
- execution model
- cost model
- statistical method
- random seed where applicable

## Core Metrics

Report:

- N
- mean return
- median return
- standard error
- confidence interval
- hit rate
- expectancy
- profit factor where meaningful
- maximum drawdown
- turnover
- exposure
- gross return
- net return
- cost drag

## Distribution

Where practical report:

- standard deviation
- skew
- tail behavior
- quantiles
- win/loss distribution
- temporal concentration

Do not rely only on average return.

## Gross Versus Net

Always separate:

Gross:
- return before trading costs

Cost drag:
- difference attributable to modeled execution costs

Net:
- gross return after modeled costs

Verify:

net = gross - cost drag

within documented rounding conventions.

## Statistical Interpretation

Distinguish:

1. statistical evidence
2. economic significance
3. practical tradability
4. robustness
5. replication

A statistically detectable relationship may still be economically unusable.

A positive average return is not sufficient evidence of a durable edge.

## Baseline Comparison

Compare the result against the appropriate executable baseline.

State whether the proposed variable adds incremental information beyond the
baseline.

Do not infer predictive skill merely because a strategy has positive gross
returns.

## Dependence

If observations overlap or otherwise exhibit serial dependence, use an
appropriate dependence-aware method.

Document the method used.

Do not treat a large trade count as automatically equivalent to a large number
of independent observations.

## Multiple Testing

State:

- number of experiments
- number of variants
- whether the result was pre-specified
- whether exploratory searches occurred
- correction or adjustment used, if applicable

Potentially favorable results discovered through broad search must be labeled
accordingly.

## Robustness

Record all pre-specified robustness tests.

Do not report only the successful variants.

Report failures explicitly.

## Replication

Record:

- replication instrument
- replication timeframe
- replication dataset
- measurement consistency
- execution consistency
- cost consistency
- statistical consistency
- replication outcome

Do not modify the original hypothesis to repair a failed replication.

## OOS Status

Every result must state:

- development
- validation
- untouched OOS
- paper/live

Untouched OOS results must remain separate from development conclusions.

## Evidence Language

Use precise descriptive language.

Examples:

- "The sample mean was positive."
- "The confidence interval included zero."
- "The result remained positive after the base cost model."
- "The effect was not reproduced on the specified replication sample."
- "The evidence is inconclusive under the tested specification."

Avoid unsupported claims about certainty, persistence, or future performance.

## Result Failure Conditions

Flag the result when:

- inputs cannot be reproduced
- execution is inconsistent
- costs are missing
- statistical inference is incompatible with dependence
- multiple testing is undisclosed
- OOS data were contaminated
- only favorable variants are reported
- negative results were discarded
