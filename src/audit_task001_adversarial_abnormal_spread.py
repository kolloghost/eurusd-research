#!/usr/bin/env python3

import csv
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPORT = Path("reports/h0_random_15m_60m_2015_01.csv")
TICK_DIR = Path("data/normalized/eurusd/2015")

PIP = 0.0001

# Fixed thresholds from the already-validated January tick distribution.
THRESH_95 = 0.7
THRESH_99 = 1.4

EXPECTED_TRADES = 403
TRADE_403 = 403


def pick_column(fieldnames, candidates, label):
    mapping = {f.strip().lower(): f for f in fieldnames}

    for candidate in candidates:
        key = candidate.strip().lower()
        if key in mapping:
            return mapping[key]

    raise SystemExit(
        f"ERROR: could not identify {label} column.\n"
        f"Available columns: {fieldnames}"
    )


def parse_timestamp_ms(value):
    s = value.strip()

    if not s:
        raise ValueError("empty timestamp")

    # Raw tick datasets may use Unix milliseconds.
    if s.isdigit():
        return int(s)

    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    dt = datetime.fromisoformat(s)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return int(round(dt.timestamp() * 1000))


def read_trades():
    if not REPORT.exists():
        raise SystemExit(f"ERROR: report not found: {REPORT}")

    with REPORT.open(newline="") as f:
        reader = csv.DictReader(f)
        trades = list(reader)
        fields = reader.fieldnames or []

    signal_col = pick_column(
        fields,
        [
            "signal_time",
            "signal_timestamp",
            "signal_close",
            "signal",
        ],
        "signal timestamp",
    )

    entry_col = pick_column(
        fields,
        [
            "entry_time",
            "entry_timestamp",
            "entry",
        ],
        "entry timestamp",
    )

    exit_col = pick_column(
        fields,
        [
            "exit_time",
            "exit_timestamp",
            "exit",
        ],
        "exit timestamp",
    )

    net_col = pick_column(
        fields,
        [
            "net_pips",
            "net",
        ],
        "net pips",
    )

    gross_col = pick_column(
        fields,
        [
            "gross_pips",
            "gross",
        ],
        "gross pips",
    )

    direction_col = pick_column(
        fields,
        [
            "direction",
            "side",
        ],
        "direction",
    )

    # Cost column is optional.
    # If absent, derive it from gross - net, which is the established
    # January H0 accounting identity.
    normalized = {f.strip().lower(): f for f in fields}
    cost_col = None

    for candidate in [
        "cost_pips",
        "cost",
        "cost_drag_pips",
        "cost_drag",
    ]:
        key = candidate.lower()
        if key in normalized:
            cost_col = normalized[key]
            break

    result = []

    for trade_no, row in enumerate(trades, 1):
        try:
            gross = float(row[gross_col])
            net = float(row[net_col])

            result.append(
                {
                    "trade_no": trade_no,
                    "signal_ms": parse_timestamp_ms(row[signal_col]),
                    "entry_ms": parse_timestamp_ms(row[entry_col]),
                    "exit_ms": parse_timestamp_ms(row[exit_col]),
                    "gross": gross,
                    "net": net,
                    "cost": (
                        float(row[cost_col])
                        if cost_col
                        else gross - net
                    ),
                    "direction": row[direction_col].strip().upper(),
                }
            )

        except Exception as exc:
            raise SystemExit(
                f"ERROR parsing trade {trade_no}: {exc}"
            )

    if len(result) != EXPECTED_TRADES:
        raise SystemExit(
            f"ERROR: expected {EXPECTED_TRADES} trades, "
            f"found {len(result)}"
        )

    return result


def locate_tick_files():
    if not TICK_DIR.exists():
        raise SystemExit(
            f"ERROR: expected tick directory not found: {TICK_DIR}\n"
            "Do not silently substitute another data source."
        )

    files = sorted(TICK_DIR.glob("*.csv"))

    if not files:
        raise SystemExit(
            f"ERROR: no CSV tick files found in {TICK_DIR}"
        )

    return files


def load_required_ticks(files, required_timestamps):
    found = {}
    matched_files = defaultdict(int)

    for path in files:

        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames or []

            ts_col = pick_column(
                fields,
                ["timestamp_utc", "timestamp", "time", "datetime"],
                "tick timestamp",
            )

            bid_col = pick_column(
                fields,
                ["bid", "bidPrice", "bidprice"],
                "bid",
            )

            ask_col = pick_column(
                fields,
                ["ask", "askPrice", "askprice"],
                "ask",
            )

            for row in reader:
                try:
                    ts = parse_timestamp_ms(row[ts_col])

                except Exception:
                    continue

                if ts not in required_timestamps:
                    continue

                bid = float(row[bid_col])
                ask = float(row[ask_col])

                found[ts] = {
                    "bid": bid,
                    "ask": ask,
                    "file": path.name,
                }

                matched_files[path.name] += 1

                # We only need the 806 execution ticks.
                if len(found) == len(required_timestamps):
                    return found, matched_files

    return found, matched_files


def pct(numerator, denominator):
    if denominator == 0:
        return float("nan")

    return 100.0 * numerator / denominator


def summarize(rows, label):
    n = len(rows)

    gross = sum(r["gross"] for r in rows)
    net = sum(r["net"] for r in rows)
    cost = sum(r["cost"] for r in rows)

    flags95 = sum(bool(r["flag95"]) for r in rows)
    flags99 = sum(bool(r["flag99"]) for r in rows)

    print(
        f"{label}: "
        f"N={n}, "
        f"gross={gross:.6f}, "
        f"net={net:.6f}, "
        f"cost={cost:.6f}, "
        f">95={flags95} ({pct(flags95, n):.3f}%), "
        f">99={flags99} ({pct(flags99, n):.3f}%)"
    )


def main():

    print("TASK-001 JANUARY ABNORMAL-SPREAD CONCENTRATION AUDIT")
    print("=" * 72)
    print(
        "DIAGNOSTIC ONLY — no observations are removed "
        "from official H0."
    )
    print(
        f"Fixed reference thresholds: "
        f">{THRESH_95:.1f} pip (95th), "
        f">{THRESH_99:.1f} pips (99th)"
    )
    print()

    trades = read_trades()

    required_timestamps = set()

    for trade in trades:
        required_timestamps.add(trade["entry_ms"])
        required_timestamps.add(trade["exit_ms"])

    print(f"Trades read: {len(trades)}")
    print(
        "Unique execution timestamps required: "
        f"{len(required_timestamps)}"
    )

    files = locate_tick_files()

    print(
        f"Tick files scanned: {len(files)} "
        f"in {TICK_DIR}"
    )

    found, matched_files = load_required_ticks(
        files,
        required_timestamps,
    )

    print(
        "Required execution timestamps found: "
        f"{len(found)}/{len(required_timestamps)}"
    )

    if len(found) != len(required_timestamps):

        missing = sorted(
            required_timestamps - set(found)
        )

        print(f"MISSING TIMESTAMPS: {len(missing)}")

        for ts in missing[:20]:
            print(f"  {ts}")

        raise SystemExit(
            "ERROR: incomplete execution-tick coverage; "
            "audit not completed."
        )

    print("Execution-tick coverage: PASS")
    print()

    rows = []

    for trade in trades:

        entry_tick = found[trade["entry_ms"]]
        exit_tick = found[trade["exit_ms"]]

        entry_spread = (
            (entry_tick["ask"] - entry_tick["bid"]) / PIP
        )

        exit_spread = (
            (exit_tick["ask"] - exit_tick["bid"]) / PIP
        )

        max_spread = max(
            entry_spread,
            exit_spread,
        )

        rows.append(
            {
                **trade,
                "entry_spread": entry_spread,
                "exit_spread": exit_spread,
                "max_spread": max_spread,
                "flag95": max_spread > THRESH_95,
                "flag99": max_spread > THRESH_99,
            }
        )

    max_observed = max(
        r["max_spread"] for r in rows
    )

    sorted_max = sorted(
        r["max_spread"] for r in rows
    )

    median_max = sorted_max[len(sorted_max) // 2]

    print(
        f"Maximum execution spread across trades: "
        f"{max_observed:.6f} pips"
    )

    print(
        f"Median maximum execution spread per trade: "
        f"{median_max:.6f} pips"
    )

    print()

    summarize(rows, "ALL TRADES")
    summarize(
        [r for r in rows if not r["flag95"]],
        "<= 95th threshold",
    )
    summarize(
        [r for r in rows if r["flag95"]],
        "> 95th threshold",
    )
    summarize(
        [r for r in rows if not r["flag99"]],
        "<= 99th threshold",
    )
    summarize(
        [r for r in rows if r["flag99"]],
        "> 99th threshold",
    )

    print()
    print("10 LARGEST LOSSES — SPREAD ASSOCIATION")

    largest_losses = sorted(
        rows,
        key=lambda r: r["net"],
    )[:10]

    for r in largest_losses:
        print(
            f"Trade {r['trade_no']:3d}: "
            f"net={r['net']:10.3f} | "
            f"entry_spread={r['entry_spread']:7.3f} | "
            f"exit_spread={r['exit_spread']:7.3f} | "
            f"max={r['max_spread']:7.3f} | "
            f">95={int(r['flag95'])} | "
            f">99={int(r['flag99'])}"
        )

    print()
    print("10 LARGEST GAINS — SPREAD ASSOCIATION")

    largest_gains = sorted(
        rows,
        key=lambda r: r["net"],
        reverse=True,
    )[:10]

    for r in largest_gains:
        print(
            f"Trade {r['trade_no']:3d}: "
            f"net={r['net']:10.3f} | "
            f"entry_spread={r['entry_spread']:7.3f} | "
            f"exit_spread={r['exit_spread']:7.3f} | "
            f"max={r['max_spread']:7.3f} | "
            f">95={int(r['flag95'])} | "
            f">99={int(r['flag99'])}"
        )

    print()
    print("TRADE 403 — KNOWN WEEKEND/CLOSURE CASE")

    r = rows[TRADE_403 - 1]

    print(
        f"net={r['net']:.6f} pips | "
        f"gross={r['gross']:.6f} | "
        f"cost={r['cost']:.6f}"
    )

    print(
        f"entry spread={r['entry_spread']:.6f} pips | "
        f"exit spread={r['exit_spread']:.6f} pips | "
        f"max={r['max_spread']:.6f} pips"
    )

    print(
        f">95={int(r['flag95'])} | "
        f">99={int(r['flag99'])}"
    )

    print()
    print("99TH-PERCENTILE CONCENTRATION METRICS")

    flagged99 = [
        r for r in rows
        if r["flag99"]
    ]

    top10_losses = sorted(
        rows,
        key=lambda r: r["net"],
    )[:10]

    top10_gains = sorted(
        rows,
        key=lambda r: r["net"],
        reverse=True,
    )[:10]

    flagged_top10_losses = [
        r for r in top10_losses
        if r["flag99"]
    ]

    flagged_top10_gains = [
        r for r in top10_gains
        if r["flag99"]
    ]

    total_absolute_losses = -sum(
        r["net"]
        for r in rows
        if r["net"] < 0
    )

    flagged_absolute_losses = -sum(
        r["net"]
        for r in flagged99
        if r["net"] < 0
    )

    print(
        f">99th trades: "
        f"{len(flagged99)}/{len(rows)} "
        f"({pct(len(flagged99), len(rows)):.3f}%)"
    )

    print(
        f">99th total net: "
        f"{sum(r['net'] for r in flagged99):.6f} pips"
    )

    print(
        f">99th total cost drag: "
        f"{sum(r['cost'] for r in flagged99):.6f} pips"
    )

    print(
        f">99th share of all absolute losing pips: "
        f"{pct(flagged_absolute_losses, total_absolute_losses):.3f}%"
    )

    print(
        f">99th count among top-10 losses: "
        f"{len(flagged_top10_losses)}/10"
    )

    print(
        f">99th count among top-10 gains: "
        f"{len(flagged_top10_gains)}/10"
    )

    print()
    print("CONSISTENCY CHECK")

    audit_net = sum(
        r["net"] for r in rows
    )

    audit_cost = sum(
        r["cost"] for r in rows
    )

    print(
        "Official H0 net (expected): "
        "-3263.000000 pips"
    )

    print(
        f"Audit net: {audit_net:.6f} pips"
    )

    print(
        "Official H0 cost drag (expected): "
        "1580.500000 pips"
    )

    print(
        f"Audit cost: {audit_cost:.6f} pips"
    )

    print()
    print(
        "RESULT: ABNORMAL-SPREAD CONCENTRATION "
        "DIAGNOSTIC COMPLETE"
    )

    print(
        "No observations were removed from "
        "the official H0 result."
    )

    print(
        "No execution rule was changed."
    )


if __name__ == "__main__":
    main()
