import csv
from collections import Counter

REPORT = "reports/h0_random_15m_60m_2015_01.csv"

with open(REPORT, newline="") as f:
    trades = list(csv.DictReader(f))

errors = []

entry_ts = []
exit_ts = []
signals = []

for i, r in enumerate(trades, 1):
    signal = int(r["signal_close"])
    entry = int(r["entry_timestamp"])
    exit_ = int(r["exit_timestamp"])

    signals.append(signal)
    entry_ts.append(entry)
    exit_ts.append(exit_)

    if entry <= signal:
        errors.append((i, "entry_not_after_signal"))

    if exit_ <= entry:
        errors.append((i, "exit_not_after_entry"))

    if i > 1:
        previous_exit = int(trades[i - 2]["exit_timestamp"])

        if entry <= previous_exit:
            errors.append((
                i,
                "overlap_or_reused_execution_window",
                entry,
                previous_exit
            ))

if len(entry_ts) != len(set(entry_ts)):
    errors.append(("duplicate_entry_timestamps", len(entry_ts) - len(set(entry_ts))))

if len(exit_ts) != len(set(exit_ts)):
    errors.append(("duplicate_exit_timestamps", len(exit_ts) - len(set(exit_ts))))

if len(signals) != len(set(signals)):
    errors.append(("duplicate_signal_timestamps", len(signals) - len(set(signals))))

if signals != sorted(signals):
    errors.append(("signals_not_monotonic",))

print("TASK-001 ADVERSARIAL STRUCTURAL AUDIT")
print("=" * 60)
print(f"Trades:                    {len(trades)}")
print(f"Unique signals:             {len(set(signals))}")
print(f"Unique entries:             {len(set(entry_ts))}")
print(f"Unique exits:               {len(set(exit_ts))}")
print(f"Structural errors:          {len(errors)}")

if errors:
    print()
    print("ERRORS:")
    for e in errors[:50]:
        print(e)
else:
    print()
    print("RESULT: STRUCTURAL ADVERSARIAL CHECK PASSED")
    print()
    print("- Signal timestamps strictly ordered")
    print("- Entries occur after signal close")
    print("- Exits occur after entries")
    print("- Trades do not overlap")
    print("- Entry timestamps are unique")
    print("- Exit timestamps are unique")
    print("- Signal timestamps are unique")
