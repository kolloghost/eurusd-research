import csv
import glob
import os
from datetime import datetime, timezone

files = sorted(glob.glob("data/eurusd/2015/*.csv"))

def read_first_last(path):
    first = None
    last = None

    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            ts = int(row["timestamp"])

            if first is None:
                first = ts
            last = ts

    return first, last

def fmt(ts):
    return datetime.fromtimestamp(
        ts / 1000,
        tz=timezone.utc
    ).isoformat()

boundaries = []

for path in files:
    first, last = read_first_last(path)
    boundaries.append((path, first, last))

print("MONTHLY FILE CONTINUITY")
print("=" * 80)

for i, (path, first, last) in enumerate(boundaries):
    print(f"\n{os.path.basename(path)}")
    print(f"  first: {fmt(first)}")
    print(f"  last:  {fmt(last)}")

    if i > 0:
        previous_last = boundaries[i - 1][2]
        gap_seconds = (first - previous_last) / 1000

        print(f"  gap from previous file: {gap_seconds:,.1f} seconds")
