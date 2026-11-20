#!/usr/bin/env python3
"""E002-419: sharp finite-set bounds with unresolved reference labels; research only."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

CERTIFY = "CERTIFY_NO_HIDDEN_CLOSURE"
ABSTAIN = "ABSTAIN"
WITNESSED = "WITNESSED_CLOSURE"
EXCLUDED = "PHYSICALLY_EXCLUDED_CLOSURE"
UNRESOLVED = "UNRESOLVED"
DECISIONS = {CERTIFY, ABSTAIN}
REFERENCES = {WITNESSED, EXCLUDED, UNRESOLVED}


def evaluate(windows):
    """Count *all* proposed windows; never infer authenticated physical evidence.

    The reference classifications are operator-supplied research labels, not
    cryptographically verified camera/velocity/geometry measurements.
    """
    if not isinstance(windows, list) or not windows:
        raise ValueError("Expected a nonempty complete window list")
    ids = set()
    counts = {WITNESSED: 0, EXCLUDED: 0, UNRESOLVED: 0}
    unresolved_all = 0
    n_certified = 0
    for row in windows:
        if not isinstance(row, dict) or set(row) != {"window_id", "product_decision", "reference_state"}:
            raise ValueError("Each row requires exactly window_id, product_decision, reference_state")
        wid = row["window_id"]
        if not isinstance(wid, str) or not wid or len(wid) > 128 or wid in ids:
            raise ValueError("Missing, duplicate, or invalid window ID")
        ids.add(wid)
        decision, reference = row["product_decision"], row["reference_state"]
        if decision not in DECISIONS or reference not in REFERENCES:
            raise ValueError("Unknown decision or reference state")
        unresolved_all += int(reference == UNRESOLVED)
        if decision == CERTIFY:
            n_certified += 1
            counts[reference] += 1
    total = len(windows)
    f, u = counts[WITNESSED], counts[UNRESOLVED]
    assert n_certified == sum(counts.values())
    lower = f / n_certified if n_certified else None
    upper = (f + u) / n_certified if n_certified else None
    return {
        "experiment": "E002-419",
        "evidence_tier": "conditional finite-set partial identification; NOT physical validation",
        "total_windows": total,
        "research_certificates": n_certified,
        "research_abstentions": total - n_certified,
        "research_coverage": n_certified / total,
        "witnessed_closure_among_certificates": f,
        "operator_declared_exclusions_among_certificates": counts[EXCLUDED],
        "unresolved_among_certificates": u,
        "unresolved_all_windows": unresolved_all,
        "conditional_finite_set_false_certificate_lower": lower,
        "conditional_finite_set_false_certificate_upper": upper,
        "conditional_reference_states_authenticated": False,
        "independent_human_raters_verified": False,
        "physical_shutter_and_velocity_verified": False,
        "population_risk_estimated": False,
        "product_claim_authorized": False,
        "product": "ABSTAIN_UNCALIBRATED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.input.read_text())
    if not isinstance(raw, dict) or set(raw) != {"windows"}:
        raise ValueError("Expected JSON object containing only 'windows'")
    result = evaluate(raw["windows"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
