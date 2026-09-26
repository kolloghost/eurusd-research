import csv
import glob
import os
from datetime import datetime, timezone

files = sorted(glob.glob("data/eurusd/2015/*.csv"))

for path in files:
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        first = next(reader)
        last = first

        for row in reader:
            last = row

    first_dt = datetime.fromtimestamp(
        int(first["timestamp"]) / 1000,
        tz=timezone.utc
    )
    last_dt = datetime.fromtimestamp(
        int(last["timestamp"]) / 1000,
        tz=timezone.utc
    )

    print(
        f"{os.path.basename(path)}"
        f"\n  first: {first_dt.isoformat()}"
        f"\n  last:  {last_dt.isoformat()}"
    )
