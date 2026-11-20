"""E002-722: zero-failure evidence limits; not a physiological certificate."""
import argparse
import math

def upper_zero(n, alpha=0.05):
    if not isinstance(n, int) or n <= 0 or not (0 < alpha < 1):
        raise ValueError("n must be positive integer and alpha in (0,1)")
    return -math.expm1(math.log(alpha) / n)

def needed(target, alpha=0.05):
    if not (0 < target < 1) or not (0 < alpha < 1):
        raise ValueError("target and alpha must be in (0,1)")
    n = math.ceil(math.log(alpha) / math.log1p(-target))
    while upper_zero(n, alpha) > target: n += 1
    while n > 1 and upper_zero(n-1, alpha) <= target: n -= 1
    return n

def design_effect(cluster_size, intraclass_correlation):
    if cluster_size < 1 or not (0 <= intraclass_correlation <= 1):
        raise ValueError("invalid cluster model")
    return 1 + (cluster_size-1)*intraclass_correlation

def selftest():
    assert needed(0.01) == 299
    assert needed(0.001) == 2995
    assert abs(upper_zero(299)-0.009969) < 0.00001
    assert design_effect(30, 0.1) == 3.9
    for n in (1, 10, 299, 2995):
        assert upper_zero(n) >= upper_zero(n+1)
    print("PASS: zero-failure confidence, thresholds and cluster sensitivity")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--participants", type=int, default=20)
    p.add_argument("--certified-per-participant", type=int, default=30)
    p.add_argument("--icc", type=float, default=0.1)
    a = p.parse_args()
    if a.selftest: selftest()
    else:
        n = a.participants*a.certified_per_participant
        de = design_effect(a.certified_per_participant, a.icc)
        print(f"Zero failures in {n} independent certified trials: exact 95% upper rate {upper_zero(n):.6f}")
        print(f"ICC={a.icc:g}, design effect={de:.3f}, heuristic effective n={n/de:.1f}")
        print("Do NOT apply independent binomial confidence to clustered events; use participant-level inference.")
        print(f"Independent-trial targets: <1% needs {needed(.01)}; <0.1% needs {needed(.001)} zero-failure certificates.")
