#!/usr/bin/env python3

import csv
import glob
import hashlib
import os
from datetime import datetime, timezone

DATA_DIR = "data/eurusd/2015"
MANIFEST = "manifests/eurusd_2015_manifest.csv"

def sha256_file(path, chunk_size=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

def validate_file(path):
    rows = 0
    bad_rows = 0
    invalid_prices = 0
    nonpositive_spreads = 0
    duplicate_timestamps = 0
    out_of_order = 0

    first_ts = None
    last_ts = None
    min_ask = float("inf")
    max_ask = float("-inf")
    min_bid = float("inf")
    max_bid = float("-inf")
    min_spread = float("inf")
    max_spread = float("-inf")

    previous_ts = None

    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)

        expected = ["timestamp", "askPrice", "bidPrice"]
        if reader.fieldnames != expected:
            raise ValueError(
                f"{path}: unexpected columns: {reader.fieldnames}"
            )

        for row in reader:
            try:
                ts = int(row["timestamp"])
                ask = float(row["askPrice"])
                bid = float(row["bidPrice"])
            except (ValueError, TypeError):
                bad_rows += 1
                continue

            rows += 1

            if first_ts is None:
                first_ts = ts

            last_ts = ts

            if previous_ts is not None:
                if ts == previous_ts:
                    duplicate_timestamps += 1
                elif ts < previous_ts:
                    out_of_order += 1

            previous_ts = ts

            if ask <= 0 or bid <= 0 or ask < bid:
                invalid_prices += 1

            spread = ask - bid

            if spread <= 0:
                nonpositive_spreads += 1

            min_ask = min(min_ask, ask)
            max_ask = max(max_ask, ask)
            min_bid = min(min_bid, bid)
            max_bid = max(max_bid, bid)
            min_spread = min(min_spread, spread)
            max_spread = max(max_spread, spread)

    def iso(ts):
        if ts is None:
            return None
        return datetime.fromtimestamp(
            ts / 1000, tz=timezone.utc
        ).isoformat()

    return {
        "file": os.path.basename(path),
        "bytes": os.path.getsize(path),
        "rows": rows,
        "bad_rows": bad_rows,
        "invalid_prices": invalid_prices,
        "nonpositive_spreads": nonpositive_spreads,
        "duplicate_timestamps": duplicate_timestamps,
        "out_of_order": out_of_order,
        "first_timestamp_ms": first_ts,
        "first_timestamp_utc": iso(first_ts),
        "last_timestamp_ms": last_ts,
        "last_timestamp_utc": iso(last_ts),
        "min_ask": min_ask,
        "max_ask": max_ask,
        "min_bid": min_bid,
        "max_bid": max_bid,
        "min_spread": min_spread,
        "max_spread": max_spread,
    }

def main():
    files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))

    if len(files) != 12:
        raise RuntimeError(
            f"Expected 12 monthly files, found {len(files)}"
        )

    print("EURUSD 2015 tick-data validation")
    print("=" * 70)

    results = []

    for i, path in enumerate(files, 1):
        print(f"[{i}/12] Validating {os.path.basename(path)} ...")
        result = validate_file(path)
        results.append(result)

    print()
    print("RESULTS")
    print("=" * 70)

    for r in results:
        print(f"\n{r['file']}")
        print(f"  rows:                 {r['rows']:,}")
        print(f"  bytes:                {r['bytes']:,}")
        print(f"  bad rows:             {r['bad_rows']:,}")
        print(f"  invalid prices:       {r['invalid_prices']:,}")
        print(f"  nonpositive spreads:  {r['nonpositive_spreads']:,}")
        print(f"  duplicate timestamps: {r['duplicate_timestamps']:,}")
        print(f"  out-of-order ticks:   {r['out_of_order']:,}")
        print(f"  first UTC:            {r['first_timestamp_utc']}")
        print(f"  last UTC:             {r['last_timestamp_utc']}")
        print(f"  ask range:            {r['min_ask']} - {r['max_ask']}")
        print(f"  bid range:            {r['min_bid']} - {r['max_bid']}")
        print(f"  spread range:         {r['min_spread']} - {r['max_spread']}")

    total = sum(r["rows"] for r in results)

    print()
    print("=" * 70)
    print(f"TOTAL TICK RECORDS: {total:,}")
    print("=" * 70)

if __name__ == "__main__":
    main()
