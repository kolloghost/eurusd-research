import csv
from pathlib import Path

input_path = Path("/data/data/com.termux/files/home/eurusd-research/reports/h0_random_15m_60m_2015.csv")
output_path = Path("/data/data/com.termux/files/home/eurusd-research/reports/h0_random_15m_60m_2015_01.csv")

jan_trades = []
with input_path.open(newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["month"] == "2015-01":
            jan_trades.append(row)
        elif row["month"] > "2015-01":
            break

print(f"January trades: {len(jan_trades)}")

with output_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=jan_trades[0].keys())
    writer.writeheader()
    writer.writerows(jan_trades)

print(f"Written to {output_path}")

PYEOF