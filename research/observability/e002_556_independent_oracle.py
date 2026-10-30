#!/usr/bin/env python3
"""Independent direct-moment oracle for E002-556; synthetic instrument only."""
import random


def run(seed=556, trials=2000):
    rng = random.Random(seed)
    worst_slack = 0.0
    for _ in range(trials):
        n = rng.randint(8, 16)
        width = rng.uniform(100, 1500)
        clock = rng.uniform(0, 10)
        q = [rng.uniform(0.05, 5) for _ in range(n)]
        eps = rng.uniform(0.001, 0.03)
        lo = [max(0.0, v-eps)/(1.001) for v in q]
        hi = [(v+eps)/0.999 for v in q]
        L, U = sum(lo), sum(hi)
        lower = upper = 0.0
        for i in range(n):
            ai, zi = i*width-clock, (i+1)*width+clock
            upper += 0.5*hi[i]**2*(zi-ai)**2/L**2
            for j in range(i+1, n):
                aj, zj = j*width-clock, (j+1)*width+clock
                lower += lo[i]*lo[j]*max(0, aj-zi)**2/U**2
                upper += hi[i]*hi[j]*(zj-ai)**2/L**2
        total = sum(q)
        mu = sum(v*(i+0.5)*width for i, v in enumerate(q))/total
        m2 = sum(v*(((i+0.5)*width)**2 + width**2/12) for i,v in enumerate(q))/total
        truth = m2-mu**2
        assert lower <= truth + 1e-7, (lower, truth)
        assert truth <= upper + 1e-7, (truth, upper)
        worst_slack = max(worst_slack, (upper-lower)/truth)
    print(f"E002-556 independent Python PASS: {trials} seeded random piecewise-uniform shutters; maximum relative interval width {worst_slack:.6f}; no real captures")


if __name__ == "__main__":
    run()
