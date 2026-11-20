#!/usr/bin/env python3
"""Independent exhaustive synthetic falsification for E002-419; no human data."""
from __future__ import annotations
import itertools
import random
from e002_419_reference_partial_id import evaluate

def row(i, decision, state):
    return {"window_id": "synthetic-" + str(i), "product_decision": decision,
            "reference_state": state}

def check_sharp_enumeration():
    rng = random.Random(419)
    states = ("WITNESSED_CLOSURE", "PHYSICALLY_EXCLUDED_CLOSURE", "UNRESOLVED")
    for trial in range(1000):
        n = rng.randint(1, 24)
        u = rng.randint(0, min(10, n))
        f = rng.randint(0, n-u)
        labels = ([states[0]]*f + [states[1]]*(n-u-f) + [states[2]]*u)
        rng.shuffle(labels)
        rows = [row(i, "CERTIFY_NO_HIDDEN_CLOSURE", label)
                for i, label in enumerate(labels)]
        # Add random abstentions: they affect coverage, never selective risk.
        rows.extend(row(n+i, "ABSTAIN", rng.choice(states))
                    for i in range(rng.randint(0, 20)))
        got = evaluate(rows)
        # Separate brute-force oracle enumerates every possible binary
        # physical truth assignment for the unresolved certified labels.
        risks = [(f+sum(bits))/n for bits in itertools.product((0, 1), repeat=u)]
        assert got["conditional_finite_set_false_certificate_lower"] == min(risks)
        assert got["conditional_finite_set_false_certificate_upper"] == max(risks)
        assert got["research_certificates"] == n
        assert got["total_windows"] == len(rows)
        assert got["research_coverage"] == n / len(rows)
        assert not got["product_claim_authorized"]
        assert got["product"] == "ABSTAIN_UNCALIBRATED"
    return 1000

def check_adversarial_cases():
    C = "CERTIFY_NO_HIDDEN_CLOSURE"
    E = "PHYSICALLY_EXCLUDED_CLOSURE"
    W = "WITNESSED_CLOSURE"
    U = "UNRESOLVED"
    A = "ABSTAIN"
    zero_seen = evaluate([row(i,C,U if i<15 else E) for i in range(20)])
    assert zero_seen["witnessed_closure_among_certificates"] == 0
    assert zero_seen["conditional_finite_set_false_certificate_lower"] == 0.0
    assert zero_seen["conditional_finite_set_false_certificate_upper"] == .75
    exact = evaluate([row(i,C,W if i<5 else E) for i in range(20)] +
                     [row(20+i,A,U) for i in range(10)])
    assert exact["conditional_finite_set_false_certificate_lower"] == .25
    assert exact["conditional_finite_set_false_certificate_upper"] == .25
    assert exact["research_coverage"] == 20/30
    assert exact["unresolved_all_windows"] == 10
    none = evaluate([row(i,A,U) for i in range(10)])
    assert none["conditional_finite_set_false_certificate_lower"] is None
    assert none["conditional_finite_set_false_certificate_upper"] is None
    assert none["research_coverage"] == 0
    assert not none["product_claim_authorized"]
    bad = [
        [], [row(0,C,E),row(0,C,U)],
        [dict(row(0,C,E),physical_calibration_authenticated=True)],
        [row(0,"CERTIFIED",E)],
        [row(0,C,"ASSUMED_NEGATIVE")],
        [dict(row(0,C,E),window_id="")],
        [dict(row(0,C,E),window_id=7)],
        [dict(row(0,C,E),reference_state=None)],
        [dict(row(0,C,E),product_decision=None)],
        [{"window_id":"a","product_decision":C}],
    ]
    for sample in bad:
        try:
            evaluate(sample)
        except (ValueError, TypeError):
            pass
        else:
            raise AssertionError("Malformed/forged input accepted: " + str(sample))
    return len(bad)

if __name__ == "__main__":
    n=check_sharp_enumeration()
    m=check_adversarial_cases()
    print("E002-419 independent exhaustive verification PASS",
          n,"enumerated randomized cases;",m,"malformed-input controls;",
          "all product outputs abstain")
