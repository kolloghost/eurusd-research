import csv
import math
from statistics import mean, median, stdev

REPORT = "reports/h0_random_15m_60m_2015_01.csv"

with open(REPORT, newline="") as f:
    rows = list(csv.DictReader(f))

nets = [float(r["net_pips"]) for r in rows]
gross = [float(r["gross_pips"]) for r in rows]
costs = [float(r["cost_drag_pips"]) for r in rows]

n = len(nets)

if n < 2:
    raise SystemExit("Insufficient observations for statistical audit.")

avg = mean(nets)
med = median(nets)
se = stdev(nets) / math.sqrt(n)
ci_low = avg - 1.96 * se
ci_high = avg + 1.96 * se

wins = sum(x > 0 for x in nets)
ties = sum(x == 0 for x in nets)

profit = sum(x for x in nets if x > 0)
loss = -sum(x for x in nets if x < 0)

pf = profit / loss if loss > 0 else float("inf")

print("TASK-001 STATISTICAL AUDIT")
print("=" * 60)
print(f"N:                 {n}")
print(f"Mean net:          {avg:.9f}")
print(f"Median net:        {med:.9f}")
print(f"SE:                {se:.9f}")
print(f"95% CI:            [{ci_low:.9f}, {ci_high:.9f}]")
print(f"Win rate:          {wins / n * 100:.9f}%")
print(f"Zero trades:       {ties}")
print(f"Gross P&L:         {sum(gross):.9f}")
print(f"Net P&L:           {sum(nets):.9f}")
print(f"Cost drag:         {sum(costs):.9f}")
print(f"Profit factor:     {pf:.9f}")
print()
print("Internal identity checks")
print("-" * 60)
print(f"Gross - Net:       {sum(gross) - sum(nets):.9f}")
print(f"Reported cost:     {sum(costs):.9f}")
print(f"Cost identity:     {math.isclose(sum(gross) - sum(nets), sum(costs), rel_tol=0, abs_tol=1e-9)}")
print(f"Win + Loss + Zero: {wins + sum(x < 0 for x in nets) + ties}")
