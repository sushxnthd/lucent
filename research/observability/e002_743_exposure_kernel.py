"""E002-743: exact rational nonuniform-exposure counterexample.
Run: python research/observability/e002_743_exposure_kernel.py
No third-party dependencies; synthetic mathematical evidence only.
"""
from fractions import Fraction as Q

def integral_poly(p):
    return sum((v / Q(i + 1) for i, v in enumerate(p)), Q(0))

def mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out

def pow_poly(a, n):
    p = [Q(1)]
    for _ in range(n):
        p = mul(p, a)
    return p

def main():
    checks = 0
    # k(t)=(n+1)(1-t)^n, a(t)=1-t, L=w=1.
    # Endpoint s=1: M = (n+1)/(n+2), true a(1)=0.
    for n in range(0, 101):
        k = [Q(n + 1) * c for c in pow_poly([Q(1), Q(-1)], n)]
        a = [Q(1), Q(-1)]
        assert integral_poly(k) == 1
        mean = integral_poly(mul(k, a))
        moment = integral_poly(mul(k, [Q(1), Q(-1)]))
        assert mean == moment == Q(n + 1, n + 2)
        assert mean - moment == 0  # sharp corrected endpoint lower bound
        if n >= 1:
            assert mean - Q(1, 2) > 0  # false positive with uniform-kernel assumption
        checks += 1
    print(f"PASS {checks} exact kernel/trajectory cases; "
          "100 nonuniform cases invalidate uniform-shutter substitution.")

if __name__ == "__main__":
    main()
