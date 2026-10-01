import csv
from datetime import datetime, timezone

REPORT = "reports/h0_random_15m_60m_2015_01.csv"

with open(REPORT, newline="") as f:
    rows = list(csv.DictReader(f))

errors = []

for i, r in enumerate(rows, 1):
    signal = int(r["signal_close"])
    entry = int(r["entry_timestamp"])
    exit_ts = int(r["exit_timestamp"])

    direction = r["direction"]
    entry_price = float(r["entry_price"])
    exit_price = float(r["exit_price"])
    gross = float(r["gross_pips"])
    net = float(r["net_pips"])
    cost = float(r["cost_drag_pips"])

    if entry <= signal:
        errors.append((i, "entry_not_strictly_after_signal_close"))

    if exit_ts < signal + 60 * 60 * 1000:
        errors.append((i, "exit_before_60m_target"))

    if direction not in ("LONG", "SHORT"):
        errors.append((i, "invalid_direction"))

    if entry_price <= 0 or exit_price <= 0:
        errors.append((i, "nonpositive_execution_price"))

    if abs((gross - net) - cost) > 1e-9:
        errors.append((i, "cost_identity_failure"))

    if i > 1:
        previous_exit = int(rows[i - 2]["exit_timestamp"])
        if signal <= previous_exit:
            errors.append((i, "overlapping_trade"))

    if r["month"] != "2015-01":
        errors.append((i, "wrong_month"))

print("TASK-001 EXECUTION/COST AUDIT")
print("=" * 60)
print(f"Trades audited:             {len(rows)}")
print(f"Execution-rule violations:  {len(errors)}")

if errors:
    print()
    print("FIRST 20 ERRORS:")
    for error in errors[:20]:
        print(error)
else:
    print("RESULT: ALL LOCKED EXECUTION CHECKS PASSED")

first_signal = int(rows[0]["signal_close"])
last_signal = int(rows[-1]["signal_close"])

print()
print("Boundary:")
print("First signal:", datetime.fromtimestamp(first_signal / 1000, tz=timezone.utc).isoformat())
print("Last signal: ", datetime.fromtimestamp(last_signal / 1000, tz=timezone.utc).isoformat())
