import csv
from pathlib import Path

INPUT_DIR = Path("data/bars/eurusd/2015")
OUTPUT_DIR = Path("data/bars15/eurusd/2015")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(INPUT_DIR.glob("*_1m.csv"))

if not files:
    raise SystemExit("No 1-minute files found.")

out_file = OUTPUT_DIR / "eurusd_2015_15m.csv"

bucket_ms = 15 * 60 * 1000

current_bucket = None
bar = None
total_1m = 0
total_15m = 0

def flush(writer):
    global bar, total_15m
    if bar is not None:
        writer.writerow([
            bar["timestamp_utc"],
            f'{bar["open"]:.5f}',
            f'{bar["high"]:.5f}',
            f'{bar["low"]:.5f}',
            f'{bar["close"]:.5f}',
            bar["tick_count"],
            bar["observed_minutes"],
        ])
        total_15m += 1

with out_file.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "timestamp_utc",
        "open",
        "high",
        "low",
        "close",
        "tick_count",
        "observed_minutes",
    ])

    for i, path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {path.name}")

        with path.open(newline="") as inp:
            reader = csv.DictReader(inp)

            for row in reader:
                total_1m += 1

                ts = int(row["timestamp_utc"])
                bucket = (ts // bucket_ms) * bucket_ms

                o = float(row["open"])
                h = float(row["high"])
                l = float(row["low"])
                c = float(row["close"])
                ticks = int(row["tick_count"])

                if current_bucket is None:
                    current_bucket = bucket
                    bar = {
                        "timestamp_utc": bucket,
                        "open": o,
                        "high": h,
                        "low": l,
                        "close": c,
                        "tick_count": ticks,
                        "observed_minutes": 1,
                    }

                elif bucket == current_bucket:
                    bar["high"] = max(bar["high"], h)
                    bar["low"] = min(bar["low"], l)
                    bar["close"] = c
                    bar["tick_count"] += ticks
                    bar["observed_minutes"] += 1

                else:
                    flush(writer)

                    current_bucket = bucket
                    bar = {
                        "timestamp_utc": bucket,
                        "open": o,
                        "high": h,
                        "low": l,
                        "close": c,
                        "tick_count": ticks,
                        "observed_minutes": 1,
                    }

    flush(writer)

print("=" * 70)
print("15-MINUTE BAR CONSTRUCTION COMPLETE")
print("=" * 70)
print(f"1-minute bars processed: {total_1m:,}")
print(f"15-minute bars created:  {total_15m:,}")
print(f"Output: {out_file}")
