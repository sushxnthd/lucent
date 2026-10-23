#!/usr/bin/env python3
"""E002-397 independent rank oracle. Does not import the primary experiment."""
import argparse
import json
import math
from pathlib import Path

VARIANTS = ("clean", "gain_070", "gain_130", "blur_sigma2",
            "translation_8_6", "glare")


def independent_auc(p, n):
    wins = 0
    for x in p:
        for y in n:
            wins += 2 if x > y else 1 if x == y else 0
    return wins / (2 * len(p) * len(n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    path = Path(args.output)
    summary = json.loads((path / "summary.json").read_text())
    rows = json.loads((path / "anonymous_scores.json").read_text())
    assert len(rows) == summary["pairs"] and len(rows) >= 15
    computed = {}
    for v in VARIANTS:
        p = [float(row[v]["positive"]) for row in rows]
        n = [float(row[v]["control"]) for row in rows]
        assert all(math.isfinite(x) and x >= 0 for x in p+n)
        computed[v] = independent_auc(p, n)
        assert abs(computed[v] - summary["auc"][v]) < 1e-12
    clean = computed["clean"]
    expected = {
        "H1_clean_auc_ge_070": clean >= .70,
        "H2_clean_auc_ge_050": clean >= .50,
        "H3_brightness_drop_le_010": all(
            clean - computed[v] <= .10 for v in ("gain_070", "gain_130")),
        "H4_translation_drop_le_010":
            clean - computed["translation_8_6"] <= .10,
        "H5_glare_drop_le_010": clean - computed["glare"] <= .10}
    assert expected == summary["hypotheses"]
    assert summary["previously_used_participants"] is True
    assert summary["physical_aperture_validated"] is False
    assert summary["actual_exposure_known"] is False
    assert summary["independent_velocity_bound"] is False
    assert summary["product"] == "ABSTAIN_UNCALIBRATED"
    print(json.dumps({"independent_oracle": "PASS",
                      "participant": summary["participant"],
                      "pairs": len(rows), "auc": computed,
                      "frozen_predictions": expected}, indent=2))


if __name__ == "__main__":
    main()
