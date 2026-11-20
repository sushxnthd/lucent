#!/usr/bin/env python3
"""E002-601 adversarial audit of E002-600 reviewer qualification. Synthetic only."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from e002_600_phantom_rater_challenge import build, grade, blank_template

HERE = Path(__file__).resolve().parent

def make_reviews(truth):
    ideal = blank_template("A")
    wide = blank_template("A")
    selective = blank_template("A")
    clean_open = clean_closed = 0
    for clip, rows in truth["clips"].items():
        for i, g in enumerate(rows):
            if not g["clean"]:
                for review in (ideal, wide, selective):
                    review["clips"][clip][i]["flags"] = ["OTHER"]
                continue
            closed = g["gap_px"] <= 20
            clean_closed += int(closed)
            clean_open += int(not closed)
            row = dict(frame=i, upper_y=g["upper_at_x320"],
                       lower_y=g["lower_at_x320"], iris_diameter=None,
                       uncertainty_px=0.5, measurement_x=320, flags=[])
            ideal["clips"][clip][i] = dict(row)
            wide["clips"][clip][i] = dict(row, uncertainty_px=50)
            if not closed:
                selective["clips"][clip][i] = dict(row)
    if (clean_open, clean_closed) != (103, 11):
        raise AssertionError("FROZEN_CLASS_COUNTS_CHANGED")
    return {"ideal": ideal, "wide_uncertainty": wide,
            "selective_abstention": selective}

def decisive_counts(review, truth):
    counts = {"correct_open":0, "correct_closed":0, "ambiguous_measured":0}
    for clip, rows in truth["clips"].items():
        for i, g in enumerate(rows):
            if not g["clean"]:
                continue
            r = review["clips"][clip][i]
            if r["flags"]:
                continue
            gap = r["lower_y"]-r["upper_y"]
            lo = max(0, gap-2*r["uncertainty_px"])
            hi = gap+2*r["uncertainty_px"]
            verdict = "CLOSED" if hi <= 20 else ("OPEN" if lo > 20 else "ABSTAIN")
            if verdict == "ABSTAIN":
                counts["ambiguous_measured"] += 1
            elif verdict == "CLOSED" and g["gap_px"] <= 20:
                counts["correct_closed"] += 1
            elif verdict == "OPEN" and g["gap_px"] > 20:
                counts["correct_open"] += 1
    return counts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expect", choices=["vulnerable", "repaired"], required=True)
    args = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="e002-601-private-") as td:
        root = Path(td)
        build(root / "fixture", "frozen-e002-601-audit-seed")
        truth_path = root / "fixture/private/truth.json"
        truth = json.loads(truth_path.read_text())
        reviews = make_reviews(truth)
        results = {}
        for name, review in reviews.items():
            python_score = grade(truth, review)
            review_path = root / (name + ".json")
            review_path.write_text(json.dumps(review))
            replay = subprocess.run(
                ["node", str(HERE / "e002_600_independent_replay.cjs"),
                 str(truth_path), str(review_path)],
                capture_output=True, text=True, check=True)
            oracle_score = json.loads(replay.stdout)
            if python_score != oracle_score:
                raise AssertionError("INDEPENDENT_ORACLE_DISAGREEMENT_"+name)
            results[name] = {
                "qualified": python_score["qualified_on_synthetic_challenge"],
                "measured": python_score["clean_measured"],
                "covered": python_score["clean_interval_covered"],
                **decisive_counts(review, truth)}
        if not results["ideal"]["qualified"]:
            raise AssertionError("IDEAL_REVIEWER_REJECTED")
        for name in ("wide_uncertainty", "selective_abstention"):
            if results[name]["correct_closed"] != 0:
                raise AssertionError("ATTACK_NOT_ZERO_CLOSED_"+name)
            expected = args.expect == "vulnerable"
            if results[name]["qualified"] != expected:
                raise AssertionError("QUALIFICATION_GATE_UNEXPECTED_"+name)
        print(json.dumps({
            "experiment":"E002-601", "expected_gate":args.expect,
            "evidence_tier":"SYNTHETIC_INSTRUMENT_FALSIFICATION",
            "clean_open_frames":103, "clean_closed_frames":11,
            "independent_node_replay":"MATCHED", "attacks":results,
            "human_rater_pairs":0, "physical_shutter_calibrations":0,
            "product":"ABSTAIN_UNCALIBRATED", "release":"BLOCKED"
        }, sort_keys=True))

if __name__ == "__main__":
    main()
