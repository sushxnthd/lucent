#!/usr/bin/env python3
"""E002-748 regression: an adversarial condition label must not corrupt the ALL denominator."""
from e002_747_prospective_scorer import evaluate

def row(condition, truth, interval):
    return dict(participant="synthetic_only", condition=condition,
                interval_id=interval, lower0="1", lower1="1",
                velocity_ceiling="1", gap_upper="1", truth=truth)

def test_reserved_condition():
    result=evaluate([row("ALL","OPEN","a"), row("glasses","CLOSED","b"),
                     row("blur","UNCERTAIN","c")])
    assert result["ALL"]["total"]==3, result
    assert result["ALL"]["adjudicated_exclusions"]==2, result
    assert result["ALL"]["false_exclusions"]==1, result
    assert result["ALL"]["uncertain_exclusions"]==1, result
    assert result["ALL"]["release_blocked"] is True, result
    assert result["glasses"]["total"]==1
    assert result["blur"]["total"]==1

if __name__=="__main__":
    test_reserved_condition()
    print("E002-748 PASS: reserved ALL label does not duplicate evidence")
