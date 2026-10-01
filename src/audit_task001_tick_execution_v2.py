import csv

REPORT = "reports/h0_random_15m_60m_2015_01.csv"

TICKS = [
    "data/normalized/eurusd/2015/eurusd-tick-2015-01-01-2015-02-01.csv",
    "data/normalized/eurusd/2015/eurusd-tick-2015-02-01-2015-03-01.csv",                ]

with open(REPORT, newline="") as f:
    trades = list(csv.DictReader(f))                                                    
needed = set()                                                                          
for r in trades:
    needed.add(int(r["entry_timestamp"]))
    needed.add(int(r["exit_timestamp"]))

found = {}

for path in TICKS:
    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            ts = int(row["timestamp_utc"])

            if ts in needed:                                                                            bid = float(row["bid"])
                ask = float(row["ask"])                                                 
                found[ts] = {
                    "bid": bid,                                                                             "ask": ask,
                    "mid": (bid + ask) / 2.0,
                }                                                                       
errors = []                                                                             
for i, r in enumerate(trades, 1):                                                           signal = int(r["signal_close"])                                                         entry_ts = int(r["entry_timestamp"])
    exit_ts = int(r["exit_timestamp"])                                                  
    direction = r["direction"]

    entry_price = float(r["entry_price"])
    exit_price = float(r["exit_price"])

    recorded_gross = float(r["gross_pips"])
    recorded_net = float(r["net_pips"])
    recorded_cost = float(r["cost_drag_pips"])

    if entry_ts not in found:
        errors.append((i, "entry_tick_not_found", entry_ts))
        continue

    if exit_ts not in found:
        errors.append((i, "exit_tick_not_found", exit_ts))
        continue

    entry_tick = found[entry_ts]
    exit_tick = found[exit_ts]

    if entry_ts <= signal:
        errors.append((i, "entry_not_after_signal"))

    if exit_ts < signal + 60 * 60 * 1000:
        errors.append((i, "exit_before_60m_target"))

    if direction == "LONG":
        expected_entry = entry_tick["ask"]
        expected_exit = exit_tick["bid"]
        expected_gross = (
            exit_tick["mid"] - entry_tick["mid"]
        ) * 100000
        expected_net = (
            expected_exit - expected_entry
        ) * 100000

    elif direction == "SHORT":
        expected_entry = entry_tick["bid"]
        expected_exit = exit_tick["ask"]
        expected_gross = (
            entry_tick["mid"] - exit_tick["mid"]
        ) * 100000
        expected_net = (
            expected_entry - expected_exit
        ) * 100000

    else:
        errors.append((i, "invalid_direction"))
        continue

    expected_cost = expected_gross - expected_net

    if abs(entry_price - expected_entry) > 1e-12:
        errors.append((
            i, "entry_price_mismatch",
            entry_price, expected_entry
        ))

    if abs(exit_price - expected_exit) > 1e-12:
        errors.append((
            i, "exit_price_mismatch",
            exit_price, expected_exit
        ))

    if abs(recorded_gross - expected_gross) > 1e-8:
        errors.append((
            i, "gross_pnl_mismatch",
            recorded_gross, expected_gross
        ))

    if abs(recorded_net - expected_net) > 1e-8:
        errors.append((
            i, "net_pnl_mismatch",
            recorded_net, expected_net
        ))

    if abs(recorded_cost - expected_cost) > 1e-8:
        errors.append((
            i, "cost_drag_mismatch",
            recorded_cost, expected_cost
        ))

print("TASK-001 RAW TICK EXECUTION AUDIT V2")
print("=" * 60)
print(f"Trades audited:             {len(trades)}")
print(f"Required tick timestamps:   {len(needed)}")
print(f"Tick timestamps found:      {len(found)}")
print(f"Audit errors:               {len(errors)}")

if errors:
    print()
    print("FIRST 30 ERRORS:")
    for error in errors[:30]:
        print(error)
else:
    print()
    print("RESULT: ALL RAW TICK EXECUTION CHECKS PASSED")
    print()
    print("Verified independently:")
    print("- Entry timestamp exists")
    print("- Exit timestamp exists")
    print("- Entry is after signal close")
    print("- Exit is at/after 60m target")
    print("- LONG entry = ASK")
    print("- LONG exit = BID")
    print("- SHORT entry = BID")
    print("- SHORT exit = ASK")
    print("- Gross P&L = exact BID/ASK-derived MID")
    print("- Net P&L = executable bid/ask")
    print("- Cost drag = Gross - Net")
