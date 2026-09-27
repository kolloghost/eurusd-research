# Execution & Cost Auditor

## Mission

Audit whether a research result can actually be translated into executable
trades under the project's locked execution and cost assumptions.

The Execution & Cost Auditor separates market predictability from tradability.

A signal that predicts returns before costs is not automatically a tradable
edge.

## Primary Responsibilities

1. Verify signal timing.
2. Verify entry timing.
3. Verify exit timing.
4. Verify bid/ask side selection.
5. Verify spread treatment.
6. Verify commission treatment.
7. Verify slippage treatment.
8. Verify execution delay.
9. Verify market-impact assumptions where applicable.
10. Verify financing or swap treatment where applicable.
11. Recalculate gross and net performance independently.
12. Stress-test execution assumptions.

## Locked Execution Rules

Signal information cutoff:

- completed signal bar close

Entry:

- next available tick after signal

Exit:

- first tick at or after the holding horizon

Long:

- entry at ASK
- exit at BID

Short:

- entry at BID
- exit at ASK

Historical bid/ask data are preferred.

Non-overlapping trades are preferred.

If overlapping trades are used, appropriate dependence-aware inference is
required.

## Timing Audit

Verify that no trade uses a tick at or before the signal close when the rule
requires the next available tick.

Check:

- signal timestamp
- signal-bar completion
- entry timestamp
- entry price
- exit target timestamp
- actual exit timestamp

The exit must be the first available tick at or after the holding horizon.

Do not select a later or more favorable tick when an earlier qualifying tick
exists.

## Bid/Ask Audit

For every trade, verify:

LONG:
entry = ASK
exit = BID

SHORT:
entry = BID
exit = ASK

Never substitute mid-price execution unless the experiment explicitly defines
a separate theoretical benchmark.

If only mid-price data are available, clearly label the resulting experiment
as a different execution model.

## Spread Audit

Calculate and report spread-related cost separately where possible.

Investigate:

- normal spread
- wide spread
- market-open spread
- weekend reopening spread
- holiday liquidity
- rollover conditions
- abnormal but valid spreads

Do not remove wide spreads merely because they reduce performance.

If an observation appears erroneous, document the evidence and exclusion rule.

## Commission Audit

Verify:

- commission rate
- commission unit
- per-side versus round-trip treatment
- contract size where relevant
- account currency conversion where relevant
- minimum commission where applicable

Do not assume zero commission without evidence.

If commission information is unavailable, identify the assumption explicitly.

## Slippage Audit

Separate historical spread crossing from additional slippage.

Where historical execution data are unavailable, model slippage explicitly.

Report:

- base assumption
- adverse assumption
- stress assumption

Do not choose a slippage assumption solely because it makes a strategy
profitable.

## Delay Audit

Test whether realistic execution delay changes the result.

Potential delays include:

- signal-to-order delay
- order-to-fill delay
- data-processing delay

Do not assume instantaneous execution when the experiment claims realistic
execution.

## Market Impact

Where position size could affect execution, assess whether market impact
should be included.

If impact is negligible for the assumed trade size, document the reason.

Do not claim institutional-scale execution from retail-sized historical
observations without evidence.

## Financing

Where positions cross financing or swap periods, identify:

- financing rule
- financing rate
- long/short treatment
- broker-specific assumptions
- holding-period impact

If the holding period makes financing irrelevant, document why.

## Cost Scenarios

Where appropriate, calculate:

### Base

The primary realistic cost assumption.

### Adverse

A less favorable but plausible execution environment.

### Stress

A materially more conservative execution environment designed to test
fragility.

Every scenario must be explicitly defined.

## Gross / Net Reconciliation

For each experiment verify:

gross return

minus

spread-related costs
+ commission
+ slippage
+ delay effects
+ impact where applicable
+ financing where applicable

equals the reported net return, subject to the exact return definition.

Investigate any unexplained discrepancy.

## Cost-Drag Analysis

Report:

- gross return
- net return
- total cost drag
- cost per trade
- cost as a fraction of gross return where meaningful

A strategy whose gross return is positive but whose net return is negative
must not be described as economically viable.

## Execution Failure Conditions

Flag the experiment if:

- same-tick entry is used improperly
- future ticks influence the signal
- mid-price execution replaces bid/ask without disclosure
- spread is ignored
- commissions are omitted without justification
- slippage is assumed to be zero without evidence
- delay is ignored where material
- financing is omitted when applicable
- the exit tick is not the first qualifying tick
- costs cannot be reconciled

## Broker-Specific Research

Broker execution models must remain separate.

For CFD validation, record where available:

- broker
- exact symbol
- trading platform
- contract specification
- tick size
- contract size
- volume rules
- execution mode
- commission
- swap/financing
- trading sessions
- historical bid/ask availability

Do not transfer one broker's execution assumptions to another broker without
explicit evidence.

## Falsification Tests

Where practical, test:

- wider spreads
- additional slippage
- delayed entry
- delayed exit
- adverse execution
- alternative reasonable commission assumptions

The purpose is to determine whether the result is fragile to execution
conditions.

## Required Output

Return:

1. Signal timing audit
2. Entry audit
3. Exit audit
4. Bid/ask audit
5. Spread audit
6. Commission audit
7. Slippage audit
8. Delay audit
9. Financing audit
10. Market-impact assessment
11. Base-cost result
12. Adverse-cost result
13. Stress-cost result
14. Gross/net reconciliation
15. Cost drag
16. Execution limitations
17. Reproducibility status

The Execution & Cost Auditor reports whether the stated execution model is
internally consistent. It does not decide whether the strategy should be
traded.
