import csv
import glob
import os
from datetime import datetime, timezone

DATA_DIR = "data/normalized/eurusd/2015"
OUT_DIR = "data/bars/eurusd/2015"
TIMEFRAME_SECONDS = 60

os.makedirs(OUT_DIR, exist_ok=True)

files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))

total_ticks = 0
total_bars = 0

for i, src in enumerate(files, 1):
    filename = os.path.basename(src).replace(".csv", "_1m.csv")
    dst = os.path.join(OUT_DIR, filename)

    print(f"[{i}/{len(files)}] {src}")
    print(f"        -> {dst}")

    current_bucket = None
    bar = None
    bars_written = 0

    with open(src, "r", newline="") as fin, \
         open(dst, "w", newline="") as fout:

        reader = csv.DictReader(fin)
        writer = csv.writer(fout)

        writer.writerow([
            "timestamp_utc",
            "open",
            "high",
            "low",
            "close",
            "tick_count",
        ])

        for row in reader:
            ts_ms = int(row["timestamp_utc"])
            mid = float(row["mid"])

            total_ticks += 1

            bucket = (ts_ms // (TIMEFRAME_SECONDS * 1000)) * (
                TIMEFRAME_SECONDS * 1000
            )

            if current_bucket is None:
                current_bucket = bucket
                bar = {
                    "open": mid,
                    "high": mid,
                    "low": mid,
                    "close": mid,
                    "ticks": 1,
                }

            elif bucket == current_bucket:
                bar["high"] = max(bar["high"], mid)
                bar["low"] = min(bar["low"], mid)
                bar["close"] = mid
                bar["ticks"] += 1

            else:
                writer.writerow([
                    current_bucket,
                    f"{bar['open']:.5f}",
                    f"{bar['high']:.5f}",
                    f"{bar['low']:.5f}",
                    f"{bar['close']:.5f}",
                    bar["ticks"],
                ])

                bars_written += 1
                total_bars += 1

                current_bucket = bucket
                bar = {
                    "open": mid,
                    "high": mid,
                    "low": mid,
                    "close": mid,
                    "ticks": 1,
                }

        if bar is not None:
            writer.writerow([
                current_bucket,
                f"{bar['open']:.5f}",
                f"{bar['high']:.5f}",
                f"{bar['low']:.5f}",
                f"{bar['close']:.5f}",
                bar["ticks"],
            ])

            bars_written += 1
            total_bars += 1

    print(f"        {bars_written:,} bars written")

print()
print("=" * 70)
print("1-MINUTE BAR CONSTRUCTION COMPLETE")
print("=" * 70)
print(f"Total ticks: {total_ticks:,}")
print(f"Total bars:  {total_bars:,}")
print(f"Output:      {OUT_DIR}")
