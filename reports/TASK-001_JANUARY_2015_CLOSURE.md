# TASK-001 — January 2015 Formal Closure Record

**Project:** QUANT FX / CFD Research
**Task:** TASK-001 — January 2015 Controlled Research Window
**Closure date:** 2026-10-01
**Status:** FORMALLY CLOSED
**Research branch:** `multi-ai-research`

---

## 1. Closure Decision

TASK-001 January 2015 is formally closed.

The January research sample, execution rules, cost model, random-direction generation, and authoritative H0 result are frozen.

No observations were removed, no execution rule was changed, and no parameter was retuned as a consequence of the January outcome.

The next controlled research window is **February 2015**.

---

## 2. Authoritative January H0 Result

January contains **403 executed trades** under the locked executable random-direction null benchmark.

- N = 403
- Mean net = -8.096774 pips/trade
- Median net = -8.000000 pips/trade
- SE = 9.523807 pips
- 95% CI = [-26.763435, +10.569887] pips/trade
- Win rate = 46.898263%
- Gross P&L = -1682.5 pips
- Net P&L = -3263.0 pips
- Cost drag = 1580.5 pips
- Profit factor = 0.878685355

This is an **executable random null benchmark**, not a trading strategy and not evidence of a trading edge.

---

## 3. Reproduction / Determinism

The January result was independently reproduced.

- Reference trades: 403
- Reproduction trades: 403
- Trade-for-trade match: PASS
- Byte-identical report: PASS
- Report SHA-256:
  `747f3d7c10b013e39cdcf8a46b1daadca2aff8f7640dd3e381c6b724b9c95284`

The seeded random-direction sequence was independently reconstructed.

- Complete ordered January signal universe: 2005 signal bars
- Actual executed January trades: 403
- Direction mismatches: 0
- Result: PASS

The H0 generation logic therefore remains frozen and reproducible.

---

## 4. Locked Execution / Cost Model

The following rules remain unchanged:

- Signals use information available only at the completed signal-bar close.
- Entry is the next available tick.
- Exit is the first available tick at or after the holding horizon.
- LONG entry = ASK.
- LONG exit = BID.
- SHORT entry = BID.
- SHORT exit = ASK.
- Gross P&L and net P&L are kept separate.
- Transaction/execution costs are explicitly accounted for.
- Trades are subject to the existing non-overlap / execution rules.
- If the target occurs during a market closure, the trade remains open until the first eligible reopening tick under the locked rule.

H0's midpoint calculations use the exact bid/ask values rather than the rounded normalized `mid` field.

---

## 5. January Validation and Audit Results

### 5.1 Statistical audit
**PASS**

Verified:

- sample size
- mean
- median
- standard error
- 95% confidence interval
- win/loss/zero accounting
- gross total
- net total
- cost total
- gross - net = cost drag
- profit factor

### 5.2 Trade-log execution/cost audit
**PASS**

The saved trade log is internally consistent with the locked execution and cost model.

### 5.3 Raw-tick execution audit V2
**PASS**

- Required execution ticks: 806
- Found: 806
- Errors: 0

This confirms the entry and exit prices against the underlying tick data under the corrected audit procedure.

### 5.4 Structural / timestamp / ordering audit
**PASS**

- Structural errors: 0
- Timestamp/order checks: PASS
- Trade timing constraints: PASS

### 5.5 Look-ahead audit
**PASS**

No report-level timing violations were found.

Verified conditions include:

- entry timestamp > signal close
- exit timestamp >= entry
- valid direction
- later signal closes occur after the preceding trade's exit

Source-code inspection found no obvious feedback path from the final report into trade generation.

---

## 6. Adversarial Falsification Diagnostics

These diagnostics were performed after the core H0 benchmark and registered validation work. They are documented as adversarial/falsification checks, not as independent confirmatory hypothesis tests.

### 6.1 Outcome concentration

The January result is not attributable solely to a tiny number of losses.

Largest losses were highly concentrated in several trades, but gains were also concentrated.

Five largest losses totaled 4047 pips, exceeding the overall January net loss of 3263 pips; removing them counterfactually makes the remainder positive.

Conversely, removing the largest gains makes the result materially more negative.

Therefore the diagnostic conclusion is:

**Both winning and losing outcomes exhibit heavy-tail concentration. The January result should not be explained as simply “a few bad trades.”**

No observations were removed.

### 6.2 Abnormal-spread concentration

Fixed spread thresholds:

- >0.7 pip = 95th-percentile threshold
- >1.4 pips = 99th-percentile threshold

Results:

- 403 trades
- 806 unique execution timestamps
- 12 tick files scanned
- 806/806 required timestamps found
- maximum execution spread observed = 7.6 pips
- median of trade-level maximum spreads = 0.4 pips

Subgroups:

- >95th percentile: 53/403 = 13.151%, net +2193 pips
- >99th percentile: 18/403 = 4.467%, net +1255 pips
- >99th-percentile trades accounted for 4.502% of all absolute losing pips
- >99th-percentile trades represented 1 of the 10 largest losses
- >99th-percentile trades represented 3 of the 10 largest gains

Conclusion:

**The January H0 loss is not explained by a small cluster of abnormal spreads.**

No observations were removed and no execution rule was changed.

### 6.3 Weekend / closure concentration

Weekend closures were derived from the actual January + February normalized tick streams rather than relying on hard-coded closure timestamps.

Observed weekend gaps:

- Jan 2 -> Jan 4
- Jan 9 -> Jan 11
- Jan 16 -> Jan 18
- Jan 23 -> Jan 25
- Jan 30 -> Feb 1
- Feb 6 -> Feb 8
- Feb 13 -> Feb 15
- Feb 20 -> Feb 22

January classification:

**NO_WEEKEND_CROSSING**
- N = 398
- Gross = -2354.0 pips
- Net = -3839.0 pips
- Cost = 1485.0 pips
- Mean = -9.645729 pips/trade
- Win rate = 46.984925%

**WEEKEND_CROSSING**
- N = 5
- Gross = +671.5 pips
- Net = +576.0 pips
- Cost = 95.5 pips
- Mean = +115.2 pips/trade
- Win rate = 40%

Weekend-crossing trades:

- Trade 19: net +525
- Trade 115: net -81
- Trade 211: net -151
- Trade 307: net +535
- Trade 403: net -252

Trade 403 remained in the official H0 because its 60-minute target occurred during the Friday/weekend closure and execution resumed at the first reopening tick under the locked rule.

Conclusion:

**The five weekend-crossing trades offset part of the January loss, but their small sample size does not establish weekend holding as a profitable mechanism.**

No observations were removed and no execution rule was changed.

---

## 7. Audit-Method Errors Corrected During January

Several errors occurred in adversarial audit methods. These were corrected and explicitly distinguished from errors in the underlying H0 experiment.

### Initial executable-price audit issue
Cause: use of the rounded normalized `mid` field.

Correction: authoritative H0 midpoint is recomputed exactly from bid and ask.

Status after correction: raw-tick execution audit V2 PASS, 806/806 ticks, 0 errors.

### Initial weekend classifier issue
Cause: hard-coded closure timestamps were one hour early.

Correction: closure intervals were derived from the actual January + February tick streams.

### Initial derived-gap filtering issue
Cause: gap filter used milliseconds as though they were seconds.

Correction: filtering was performed in the correct millisecond scale.

These were **audit-method errors**, not failures of the January H0 experiment.

---

## 8. Multiple-Testing / Search-History Classification

Git history establishes the project audit trail but does not, by itself, prove detailed pre-registration timing for every later diagnostic.

The following were established/registered before the January adversarial phase:

- H0 random executable baseline
- statistical audit
- execution/cost audit
- raw-tick execution audit
- structural audit
- January TASK-001 framework

The following were subsequently performed as adversarial/falsification diagnostics:

- concentration
- abnormal-spread concentration
- weekend/closure concentration
- random-direction integrity
- source-code/look-ahead inspection
- trade-level look-ahead timing
- search-history / multiple-testing documentation

Later diagnostics are therefore retained as **audit evidence**, not relabeled as pre-registered hypothesis tests.

---

## 9. January Task Interpretation

TASK-001 demonstrates:

1. The January executable random benchmark is reproducible.
2. The trade-generation process is deterministic under the locked seed and signal universe.
3. Execution timestamps and executable bid/ask pricing are auditable.
4. The January negative result survives the completed adversarial checks.
5. The observed loss is not explained by a small abnormal-spread cluster.
6. Weekend-crossing trades do not justify changing the locked execution rule.
7. No evidence from January establishes a robust directional trading edge.

This conclusion is limited to the January TASK-001 benchmark and its stated research purpose.

---

## 10. Frozen Decisions

The following are frozen at January closure:

- January H0 trade set
- random seed
- signal-bar universe
- entry/exit rules
- bid/ask execution convention
- cost model
- weekend/closure handling
- treatment of extreme observations
- no post-hoc deletion of trades
- no January parameter retuning

January evidence must be preserved unchanged for cumulative and historical comparison.

---

## 11. Next Research Window

The next controlled research window is:

**February 2015**

Before expanding hypotheses:

1. obtain/verify the February underlying data required for the next window;
2. preserve January as historical evidence;
3. keep January rules fixed;
4. document any cross-month execution-data dependency separately from research-sample membership;
5. rerun the registered H0 baseline for February/cumulative analysis before expanding hypothesis testing.

The research must continue through falsification rather than optimizing rules around January.

---

## 12. Current Project-Level Status at January Closure

- H0: established executable null benchmark
- H1: inconclusive
- H2: inconclusive / mostly negative
- H3: mostly negative
- H4: volatility conditioning remains a potentially interesting mechanism, but no directional trading edge established
- Robust edge: **NOT ESTABLISHED**

January TASK-001 is closed for the current research stage.
