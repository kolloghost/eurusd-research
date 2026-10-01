import csv
import statistics

REPORT = "reports/h0_random_15m_60m_2015_01.csv"

with open(REPORT, newline="") as f:
    trades = list(csv.DictReader(f))

nets = [float(r["net_pips"]) for r in trades]

def summarize(values):
    n = len(values)
    total = sum(values)
    mean = total / n if n else float("nan")
    median = statistics.median(values) if values else float("nan")
    return n, total, mean, median

print("TASK-001 ADVERSARIAL CONCENTRATION AUDIT")
print("=" * 60)

n, total, mean, median = summarize(nets)

print(f"All trades:                 N={n}")
print(f"Total net:                  {total:.6f} pips")
print(f"Mean net:                   {mean:.6f} pips")
print(f"Median net:                 {median:.6f} pips")
print()

largest_losses = sorted(
    enumerate(nets, 1),
    key=lambda x: x[1]
)[:10]

largest_gains = sorted(
    enumerate(nets, 1),
    key=lambda x: x[1],
    reverse=True
)[:10]

print("10 LARGEST LOSSES:")
for i, value in largest_losses:
    print(f"Trade {i:3d}: {value:12.6f} pips")

print()
print("10 LARGEST GAINS:")
for i, value in largest_gains:
    print(f"Trade {i:3d}: {value:12.6f} pips")

print()
print("TRIMMED DIAGNOSTICS")
print("(Diagnostic only; no observations are removed from H0.)")

for k in [1, 2, 5, 10]:
    by_loss = sorted(nets)
    by_gain = sorted(nets, reverse=True)

    without_losses = by_loss[k:]
    without_gains = by_gain[k:]

    n1, t1, m1, med1 = summarize(without_losses)
    n2, t2, m2, med2 = summarize(without_gains)

    print()
    print(f"Remove {k} largest losses:")
    print(f"  N={n1}, total={t1:.6f}, mean={m1:.6f}")

    print(f"Remove {k} largest gains:")
    print(f"  N={n2}, total={t2:.6f}, mean={m2:.6f}")

print()
print("RESULT: CONCENTRATION DIAGNOSTIC COMPLETE")
print("No observations were removed from the official H0 result.")
