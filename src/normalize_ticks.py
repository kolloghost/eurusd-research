import csv
import glob
import os

DATA_DIR = "data/eurusd/2015"
OUT_DIR = "data/normalized/eurusd/2015"

os.makedirs(OUT_DIR, exist_ok=True)

files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))

total = 0

for i, src in enumerate(files, 1):
    filename = os.path.basename(src)
    dst = os.path.join(OUT_DIR, filename)

    print(f"[{i}/{len(files)}] {src}")
    print(f"        -> {dst}")

    count = 0

    with open(src, "r", newline="") as fin, \
         open(dst, "w", newline="") as fout:

        reader = csv.DictReader(fin)

        expected = {"timestamp", "askPrice", "bidPrice"}
        if set(reader.fieldnames or []) != expected:
            raise ValueError(
                f"Unexpected columns in {src}: {reader.fieldnames}"
            )

        writer = csv.writer(fout)

        writer.writerow([
            "timestamp_utc",
            "bid",
            "ask",
            "mid",
            "spread",
            "spread_pips",
        ])

        for row in reader:
            timestamp_ms = int(row["timestamp"])
            bid = float(row["bidPrice"])
            ask = float(row["askPrice"])

            mid = (bid + ask) / 2.0
            spread = ask - bid
            spread_pips = spread * 100000.0

            writer.writerow([
                timestamp_ms,
                f"{bid:.5f}",
                f"{ask:.5f}",
                f"{mid:.5f}",
                f"{spread:.5f}",
                f"{spread_pips:.4f}",
            ])

            count += 1
            total += 1

    print(f"        {count:,} ticks written")

print()
print("=" * 70)
print("NORMALIZATION COMPLETE")
print("=" * 70)
print(f"Total ticks: {total:,}")
print(f"Output:      {OUT_DIR}")
