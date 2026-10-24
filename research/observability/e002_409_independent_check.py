#!/usr/bin/env python3
"""Independent E002-409 rank oracle. Does not import primary evaluator or OpenCV."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

VARIANTS = ("clean", "gain_070", "gain_130", "blur_sigma2",
            "translation_8_6", "glare")
MD5 = "8217203472f7393b03aa56102dbc9adc"


def rank_auc(rows, variant):
    # Independent pairwise-comparison oracle; not the primary NumPy implementation.
    positives = [r[variant]["positive"] for r in rows]
    controls = [r[variant]["control"] for r in rows]
    wins = 0
    ties = 0
    for p in positives:
        for n in controls:
            wins += int(p > n)
            ties += int(p == n)
    return (2*wins + ties) / (2*len(positives)*len(controls))


def verify(summary, rows, *, min_pairs=15):
    if (summary.get("experiment") != "E002-409"
            or summary.get("participant") != "S06"
            or summary.get("source_md5") != MD5
            or summary.get("product") != "ABSTAIN_UNCALIBRATED"
            or summary.get("physical_aperture_validated") is not False
            or summary.get("independent_camera_clock") is not False
            or summary.get("hard_velocity_bound") is not False
            or summary.get("previously_evaluated_participant") is not False):
        raise ValueError("Incorrect evidence provenance or product gate")
    if not isinstance(rows, list) or len(rows) < min_pairs:
        raise ValueError("Insufficient held-out event/control pairs")
    if summary.get("paired_windows") != len(rows):
        raise ValueError("Pair-count disagreement")
    if not isinstance(summary.get("session"), str) or not summary["session"].endswith("_phantom.avi"):
        raise ValueError("Invalid source session")
    if (type(summary.get("source_frame_count")) is not int or
            summary["source_frame_count"] < 1000 or
            type(summary.get("eeg_marker_count")) is not int or
            summary["eeg_marker_count"] < len(rows)):
        raise ValueError("Invalid acquisition counts")
    rejected = summary.get("rejected")
    if (not isinstance(rejected, dict)
            or set(rejected) != {"event_uncovered_or_gap", "no_clean_control"}
            or any(type(v) is not int or v < 0 for v in rejected.values())):
        raise ValueError("Invalid exclusion accounting")
    if summary["eeg_marker_count"] != len(rows) + sum(rejected.values()):
        raise ValueError("Event accounting disagreement")
    for r in rows:
        if not isinstance(r, dict) or set(r) != set(VARIANTS):
            raise ValueError("Unexpected variant or leaked private metadata")
        for v in VARIANTS:
            pair = r[v]
            if not isinstance(pair, dict) or set(pair) != {"positive", "control"}:
                raise ValueError("Unexpected score keys or leaked private metadata")
            for value in pair.values():
                if type(value) not in (float, int) or not math.isfinite(value) or value < 0:
                    raise ValueError("Invalid image-motion score")
    auc = {v: rank_auc(rows, v) for v in VARIANTS}
    claimed = summary.get("auc")
    if not isinstance(claimed, dict) or set(claimed) != set(VARIANTS):
        raise ValueError("Missing AUC")
    if any(type(claimed[v]) not in (float, int) or
           not math.isfinite(claimed[v]) or abs(auc[v] - claimed[v]) > 1e-12
           for v in VARIANTS):
        raise ValueError("Independent AUC disagreement")
    baseline = auc["clean"]
    h = {
        "H1_clean_auc_ge_070": baseline >= .70,
        "H2_blur_auc_loss_le_010": baseline - auc["blur_sigma2"] <= .10,
        "H3_glare_auc_loss_le_010": baseline - auc["glare"] <= .10,
        "H4_gains_auc_loss_le_010": all(
            baseline - auc[v] <= .10 for v in ("gain_070", "gain_130")),
        "H5_translation_auc_loss_le_010": baseline - auc["translation_8_6"] <= .10
    }
    if summary.get("hypotheses") != h or summary.get("all_hypotheses_pass") is not all(h.values()):
        raise ValueError("Frozen hypothesis decision mismatch")
    return {"independent_check": "PASS", "pairs": len(rows), "auc": auc,
            "hypotheses": h, "product": "ABSTAIN_UNCALIBRATED"}


def self_test():
    # 16 independently constructed synthetic paired rows; no source video.
    rows = [{v: {"positive": float(i+2), "control": float(i)}
             for v in VARIANTS} for i in range(16)]
    # Each set of positives is shifted by two positions; rank AUC ~0.617.
    auc = {v: rank_auc(rows, v) for v in VARIANTS}
    h = {
        "H1_clean_auc_ge_070": auc["clean"] >= .70,
        "H2_blur_auc_loss_le_010": True,
        "H3_glare_auc_loss_le_010": True,
        "H4_gains_auc_loss_le_010": True,
        "H5_translation_auc_loss_le_010": True
    }
    summary = {
        "experiment": "E002-409", "participant": "S06", "source_md5": MD5,
        "session": "Sess01/SSVEP061_phantom.avi",
        "source_frame_count": 1000, "eeg_marker_count": 16,
        "paired_windows": 16, "rejected": {
            "event_uncovered_or_gap": 0, "no_clean_control": 0},
        "auc": auc, "hypotheses": h, "all_hypotheses_pass": all(h.values()),
        "previously_evaluated_participant": False,
        "physical_aperture_validated": False,
        "independent_camera_clock": False, "hard_velocity_bound": False,
        "product": "ABSTAIN_UNCALIBRATED"
    }
    assert verify(summary, rows)["independent_check"] == "PASS"
    import copy
    for corrupt in ("auc", "hypotheses", "scores", "leak", "provenance", "nonfinite"):
        a, b = copy.deepcopy(summary), copy.deepcopy(rows)
        if corrupt == "auc":
            a["auc"]["clean"] += .1
        elif corrupt == "hypotheses":
            a["hypotheses"]["H1_clean_auc_ge_070"] = not h["H1_clean_auc_ge_070"]
        elif corrupt == "scores":
            b[0]["clean"]["positive"] += 100
        elif corrupt == "leak":
            b[0]["source_timestamp"] = 10.0
        elif corrupt == "provenance":
            a["physical_aperture_validated"] = True
        elif corrupt == "nonfinite":
            b[0]["clean"]["control"] = float("nan")
        try:
            verify(a, b)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Corruption accepted: {corrupt}")
    print("E002-409 independent synthetic oracle: PASS (1 control + 6 corruptions)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        self_test()
    else:
        if a.output is None:
            p.error("--output required without --self-test")
        summary = json.loads((a.output/"summary.json").read_text())
        rows = json.loads((a.output/"anonymous_scores.json").read_text())
        print(json.dumps(verify(summary, rows), indent=2))


if __name__ == "__main__":
    main()
