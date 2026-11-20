"""E002-721: synthetic clock interval replay; not human or physical data."""
from fractions import Fraction as F
from itertools import product

def verdict(a0, a1, delta_upper, velocity_upper):
    if min(a0, a1, delta_upper, velocity_upper) < 0:
        raise ValueError("negative bound")
    return "EXCLUDE" if velocity_upper * delta_upper < a0 + a1 else "ABSTAIN"

def witness(a0, a1, delta, velocity):
    return (velocity > 0 and velocity * delta >= a0 + a1) or (a0 == 0 and a1 == 0)

def run():
    grid = [F(i, 4) for i in range(1, 9)]
    jitter = [F(0), F(1, 8), F(1, 4), F(1, 2)]
    counts = {"trials": 0, "safe_exclusions": 0, "unsafe_nominal_exclusions": 0, "conservative_abstentions": 0}
    example = None
    for a0, a1, d, v, j in product(grid, grid, grid, grid, jitter):
        counts["trials"] += 1
        actual_delta = d + j
        conservative = verdict(a0, a1, actual_delta, v)
        nominal = verdict(a0, a1, d, v)
        possible = witness(a0, a1, actual_delta, v)
        assert not (conservative == "EXCLUDE" and possible)
        counts["safe_exclusions"] += conservative == "EXCLUDE"
        counts["conservative_abstentions"] += conservative == "ABSTAIN"
        if nominal == "EXCLUDE" and possible:
            counts["unsafe_nominal_exclusions"] += 1
            if example is None:
                example = (a0, a1, d, v, j)
    assert counts["unsafe_nominal_exclusions"] > 0
    print(counts)
    print("first witness (a0,a1,nominal_gap,V,unaccounted_gap)=", example)

if __name__ == "__main__":
    run()
