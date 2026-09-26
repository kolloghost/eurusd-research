import csv
import glob
from datetime import datetime, timezone

DATA_DIR = "data/eurusd/2015"

# Ignore gaps >= 6 hours for the initial intraday analysis.
# These are overwhelmingly market-closure/weekend candidates.
INTRADAY_MAX = 6 * 3600

gap_counts = {
    1: 0,
    5: 0,
    10: 0,
    30: 0,
    60: 0,
    120: 0,
    300: 0,
    600: 0,
    1800: 0,
}

largest = []
previous_ts = None
total_gaps = 0
intraday_gaps = 0

def add_largest(item):
    largest.append(item)
    largest.sort(reverse=True)
    if len(largest) > 50:
        largest.pop()

files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))

for i, path in enumerate(files, 1):
    print(f"[{i}/{len(files)}] {path}")

    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            ts = int(row["timestamp"])

            if previous_ts is not None:
                gap = (ts - previous_ts) / 1000
                total_gaps += 1

                if 0 < gap < INTRADAY_MAX:
                    intraday_gaps += 1

                    for threshold in gap_counts:
                        if gap >= threshold:
                            gap_counts[threshold] += 1

                    add_largest((gap, previous_ts, ts))

            previous_ts = ts

print()
print("=" * 80)
print("EURUSD 2015 INTRADAY GAP ANALYSIS")
print("=" * 80)

print(f"\nTotal gaps examined: {total_gaps:,}")
print(f"Gaps < 6 hours:     {intraday_gaps:,}")

print("\nINTRADAY GAP COUNTS")
print("-" * 80)

for threshold, count in gap_counts.items():
    print(f">= {threshold:>4} sec and < 6h: {count:,}")

print("\nLARGEST 50 GAPS BELOW 6 HOURS")
print("-" * 80)

for gap, before, after in largest:
    before_dt = datetime.fromtimestamp(
        before / 1000, tz=timezone.utc
    )
    after_dt = datetime.fromtimestamp(
        after / 1000, tz=timezone.utc
    )

    print(
        f"{gap:10.3f}s  "
        f"{before_dt.isoformat()} -> "
        f"{after_dt.isoformat()}"
    )
