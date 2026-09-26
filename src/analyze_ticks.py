import csv
import glob
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone

DATA_DIR = "data/eurusd/2015"

# Gap thresholds in seconds
THRESHOLDS = [1, 5, 10, 30, 60, 300, 900, 3600]

def percentile(sorted_values, p):
    if not sorted_values:
        return None

    k = (len(sorted_values) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return sorted_values[int(k)]

    return (
        sorted_values[f] * (c - k)
        + sorted_values[c] * (k - f)
    )

def main():
    files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))

    total_ticks = 0
    spreads = []
    gaps = []

    daily_ticks = Counter()
    daily_spreads = defaultdict(list)

    large_gaps = []

    previous_ts = None

    for i, path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {path}")

        with open(path, newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                ts = int(row["timestamp"])
                ask = float(row["askPrice"])
                bid = float(row["bidPrice"])

                total_ticks += 1

                spread = (ask - bid) * 100000
                spreads.append(spread)

                dt = datetime.fromtimestamp(
                    ts / 1000,
                    tz=timezone.utc
                )

                day = dt.date().isoformat()
                daily_ticks[day] += 1
                daily_spreads[day].append(spread)

                if previous_ts is not None:
                    gap = (ts - previous_ts) / 1000
                    gaps.append(gap)

                    if gap >= 60:
                        large_gaps.append(
                            (gap, previous_ts, ts)
                        )

                previous_ts = ts

    spreads.sort()
    gaps.sort()

    print()
    print("=" * 80)
    print("EURUSD 2015 TICK ANALYSIS")
    print("=" * 80)

    print(f"\nTotal ticks: {total_ticks:,}")

    print("\nSPREAD (pips)")
    print("-" * 80)
    print(f"min:     {min(spreads):.4f}")
    print(f"median:  {percentile(spreads, 0.50):.4f}")
    print(f"p90:     {percentile(spreads, 0.90):.4f}")
    print(f"p95:     {percentile(spreads, 0.95):.4f}")
    print(f"p99:     {percentile(spreads, 0.99):.4f}")
    print(f"max:     {max(spreads):.4f}")

    print("\nINTER-TICK GAP (seconds)")
    print("-" * 80)
    print(f"min:     {min(gaps):.6f}")
    print(f"median:  {percentile(gaps, 0.50):.6f}")
    print(f"p90:     {percentile(gaps, 0.90):.6f}")
    print(f"p95:     {percentile(gaps, 0.95):.6f}")
    print(f"p99:     {percentile(gaps, 0.99):.6f}")
    print(f"max:     {max(gaps):.3f}")

    print("\nGAPS ABOVE THRESHOLD")
    print("-" * 80)

    for threshold in THRESHOLDS:
        count = sum(g >= threshold for g in gaps)
        print(f">= {threshold:>4} sec: {count:,}")

    print("\nLARGEST 20 GAPS")
    print("-" * 80)

    for gap, before, after in sorted(
        large_gaps,
        reverse=True
    )[:20]:

        before_dt = datetime.fromtimestamp(
            before / 1000,
            tz=timezone.utc
        )
        after_dt = datetime.fromtimestamp(
            after / 1000,
            tz=timezone.utc
        )

        print(
            f"{gap:10.1f}s  "
            f"{before_dt.isoformat()} -> "
            f"{after_dt.isoformat()}"
        )

    print("\nBUSIEST DAYS")
    print("-" * 80)

    for day, count in daily_ticks.most_common(10):
        print(f"{day}: {count:,} ticks")

    print("\nQUIETEST DAYS")
    print("-" * 80)

    for day, count in sorted(
        daily_ticks.items(),
        key=lambda x: x[1]
    )[:10]:
        print(f"{day}: {count:,} ticks")

if __name__ == "__main__":
    main()
