import csv
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev, median
from datetime import datetime, timezone

BARS_FILE = Path("data/bars15/eurusd/2015/eurusd_2015_15m.csv")
TICK_DIR = Path("data/normalized/eurusd/2015")

BAR_MINUTES = 15
HOLDING_MINUTES = 60
BAR_MS = BAR_MINUTES * 60 * 1000
HOLDING_MS = HOLDING_MINUTES * 60 * 1000

SEED = 20150101
rng = random.Random(SEED)

# ------------------------------------------------------------
# Load complete 15-minute signal bars.
# IMPORTANT:
# The timestamp is the START of the 15m bar.
# The signal is therefore available at timestamp + 15 minutes.
# ------------------------------------------------------------

signals = []

with BARS_FILE.open(newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        bar_start = int(row["timestamp_utc"])
        observed = int(row["observed_minutes"])

        if observed != BAR_MINUTES:
            continue

        signal_close = bar_start + BAR_MS

        signals.append({
            "signal_close": signal_close,
            "exit_target": signal_close + HOLDING_MS,
            "direction": 1 if rng.random() < 0.5 else -1,
        })

print(f"Complete 15m signal bars available: {len(signals):,}")

# ------------------------------------------------------------
# Stream normalized ticks.
#
# Non-overlapping rule:
# Once a trade exits, discard all signals whose signal close
# occurred at or before that exit.
#
# Entry:
#   first available tick STRICTLY after signal close
#
# Important edge case:
# If the first available tick arrives at/after the intended
# exit horizon, the signal cannot produce a valid timed trade,
# so it is skipped.
# ------------------------------------------------------------

signal_index = 0
active = None
trades = []

files = sorted(TICK_DIR.glob("*.csv"))

for file_index, path in enumerate(files, 1):
    print(f"[{file_index}/{len(files)}] {path.name}")

    with path.open(newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            ts = int(row["timestamp_utc"])
            bid = float(row["bid"])
            ask = float(row["ask"])
            mid = (bid + ask) / 2.0

            # ------------------------------------------------
            # Exit active trade.
            # ------------------------------------------------
            if active is not None and ts >= active["exit_target"]:

                direction = active["direction"]

                if direction == 1:
                    exit_price = bid
                    gross_pips = (
                        mid - active["entry_mid"]
                    ) * 100000
                    net_pips = (
                        exit_price - active["entry_price"]
                    ) * 100000
                else:
                    exit_price = ask
                    gross_pips = (
                        active["entry_mid"] - mid
                    ) * 100000
                    net_pips = (
                        active["entry_price"] - exit_price
                    ) * 100000

                cost_drag = gross_pips - net_pips

                trades.append({
                    "month": datetime.fromtimestamp(
                        active["signal_close"] / 1000,
                        tz=timezone.utc
                    ).strftime("%Y-%m"),
                    "signal_close": active["signal_close"],
                    "entry_timestamp": active["entry_timestamp"],
                    "exit_timestamp": ts,
                    "direction": "LONG" if direction == 1 else "SHORT",
                    "entry_price": active["entry_price"],
                    "exit_price": exit_price,
                    "gross_pips": gross_pips,
                    "net_pips": net_pips,
                    "cost_drag_pips": cost_drag,
                })

                last_exit = ts
                active = None

                # Skip every signal whose completed-bar close
                # happened before or at the actual exit.
                while (
                    signal_index < len(signals)
                    and signals[signal_index]["signal_close"] <= last_exit
                ):
                    signal_index += 1

            # ------------------------------------------------
            # If no trade is active, look for the next eligible
            # signal.
            # ------------------------------------------------
            if active is None:

                while signal_index < len(signals):
                    s = signals[signal_index]

                    # Signal has not closed yet.
                    if ts <= s["signal_close"]:
                        break

                    # Market did not provide an entry tick before
                    # the intended horizon elapsed.
                    if ts >= s["exit_target"]:
                        signal_index += 1
                        continue

                    direction = s["direction"]

                    if direction == 1:
                        entry_price = ask
                    else:
                        entry_price = bid

                    active = {
                        "signal_close": s["signal_close"],
                        "exit_target": s["exit_target"],
                        "direction": direction,
                        "entry_timestamp": ts,
                        "entry_price": entry_price,
                        "entry_mid": mid,
                    }

                    signal_index += 1
                    break

# ------------------------------------------------------------
# Statistics
# ------------------------------------------------------------

if not trades:
    raise SystemExit("No valid trades generated.")

def summarize(items):
    nets = [x["net_pips"] for x in items]
    gross = [x["gross_pips"] for x in items]
    costs = [x["cost_drag_pips"] for x in items]

    n = len(nets)
    avg = mean(nets)

    if n > 1:
        se = stdev(nets) / math.sqrt(n)
    else:
        se = float("nan")

    ci_low = avg - 1.96 * se
    ci_high = avg + 1.96 * se

    wins = sum(x > 0 for x in nets)
    losses = sum(x < 0 for x in nets)

    gross_profit = sum(x for x in nets if x > 0)
    gross_loss = -sum(x for x in nets if x < 0)

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else float("inf")
    )

    return {
        "N": n,
        "mean_net": avg,
        "se": se,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "median_net": median(nets),
        "win_rate": wins / n * 100,
        "gross_pips": sum(gross),
        "net_pips": sum(nets),
        "cost_drag_pips": sum(costs),
        "profit_factor": profit_factor,
    }

overall = summarize(trades)

by_month = defaultdict(list)

for trade in trades:
    by_month[trade["month"]].append(trade)

print()
print("=" * 80)
print("H0 — RANDOM EXECUTABLE BASELINE")
print("=" * 80)
print(f"Seed:                    {SEED}")
print(f"Signal timeframe:        {BAR_MINUTES} minutes")
print(f"Holding horizon:         {HOLDING_MINUTES} minutes")
print("Signal timing:           completed-bar close")
print("Entry:                   next available tick")
print("LONG execution:          ASK -> BID")
print("SHORT execution:         BID -> ASK")
print("Trade overlap:           non-overlapping")
print()

print("CUMULATIVE 2015")
print("-" * 80)
print(f"N:                       {overall['N']:,}")
print(f"Mean net P&L:            {overall['mean_net']:.4f} pips/trade")
print(f"Median net P&L:          {overall['median_net']:.4f} pips/trade")
print(f"Standard error:          {overall['se']:.4f}")
print(
    f"95% CI:                  "
    f"[{overall['ci_low']:.4f}, {overall['ci_high']:.4f}]"
)
print(f"Win rate:                {overall['win_rate']:.2f}%")
print(f"Gross P&L:               {overall['gross_pips']:.2f} pips")
print(f"Net P&L:                 {overall['net_pips']:.2f} pips")
print(f"Cost drag:               {overall['cost_drag_pips']:.2f} pips")
print(f"Profit factor:           {overall['profit_factor']:.4f}")

print()
print("MONTH-BY-MONTH")
print("-" * 80)

for month in sorted(by_month):
    s = summarize(by_month[month])

    print(
        f"{month}  "
        f"N={s['N']:4d}  "
        f"mean={s['mean_net']:8.4f}  "
        f"SE={s['se']:7.4f}  "
        f"95%CI=[{s['ci_low']:8.4f},{s['ci_high']:8.4f}]  "
        f"win={s['win_rate']:6.2f}%  "
        f"net={s['net_pips']:9.2f}"
    )

# ------------------------------------------------------------
# Save trade-level results.
# ------------------------------------------------------------

out = Path("reports/h0_random_15m_60m_2015.csv")
out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=trades[0].keys()
    )
    writer.writeheader()
    writer.writerows(trades)

print()
print(f"Trade log: {out}")
