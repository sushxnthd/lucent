#!/usr/bin/env python3
"""E002-602: demonstrate a public-answer-key attack on E002-601's rater gate.

This script deliberately does NOT read any PNG or private truth before producing
the attack export. The 'reviewer' is a deterministic algorithm using public code.
Never interpret the result as human anatomical competence.
"""
import json
import os
from pathlib import Path
import secrets
import subprocess
import tempfile

from e002_600_phantom_rater_challenge import (
    build, blank_template, grade, PULSES, NUISANCE, N_CLIPS, N_FRAMES,
)

ROOT = Path(__file__).resolve().parent
ORACLE = ROOT / "e002_600_independent_replay.cjs"


def make_public_only_export():
    packet = blank_template("A")
    for c in range(N_CLIPS):
        clip = f"clip_{c:04d}"
        for i in range(N_FRAMES):
            row = packet["clips"][clip][i]
            if c in NUISANCE:
                continue  # Publicly known nuisance arm, abstain without seeing image.
            gap = 4 if i in PULSES[c] else 34
            row.update(
                upper_y=190,
                lower_y=190 + gap,
                iris_diameter=None,
                uncertainty_px=5,
                measurement_x=320,
                flags=[],
            )
    return packet


def run_one(root, seed):
    build(root, seed)
    # Crucial: construct and seal the attack export before reading private truth.
    attack = make_public_only_export()
    review_path = root / "attack.json"
    review_path.write_text(json.dumps(attack, sort_keys=True), encoding="utf-8")
    truth_path = root / "private" / "truth.json"
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    python_result = grade(truth, attack)
    node_result = json.loads(subprocess.run(
        ["node", str(ORACLE), str(truth_path), str(review_path)],
        check=True, capture_output=True, text=True,
    ).stdout)
    assert python_result == node_result, "independent replay mismatch"
    expected = {
        "clean_frames": 114, "clean_measured": 114, "clean_interval_covered": 114,
        "clean_open_frames": 103, "clean_closed_frames": 11,
        "correct_decisive_open": 103, "correct_decisive_closed": 11,
        "ambiguous_measured": 0, "clean_false_closed": 0, "clean_false_open": 0,
        "nuisance_frames": 76, "nuisance_abstentions": 76,
        "qualified_on_synthetic_challenge": True,
    }
    for k, v in expected.items():
        assert python_result[k] == v, (k, python_result[k], v)
    # Negative control: a wrong public-only response must fail.
    negative = make_public_only_export()
    for c in range(N_CLIPS):
        if c not in NUISANCE:
            for row in negative["clips"][f"clip_{c:04d}"]:
                row["lower_y"] = 224
    neg_result = grade(truth, negative)
    assert not neg_result["qualified_on_synthetic_challenge"]
    assert neg_result["clean_false_open"] == 11
    return {
        "public_only_attack_qualified": python_result["qualified_on_synthetic_challenge"],
        "correct_decisive_open": python_result["correct_decisive_open"],
        "correct_decisive_closed": python_result["correct_decisive_closed"],
        "clean_interval_covered": python_result["clean_interval_covered"],
        "nuisance_abstentions": python_result["nuisance_abstentions"],
        "negative_control_qualified": neg_result["qualified_on_synthetic_challenge"],
        "negative_control_false_open": neg_result["clean_false_open"],
        "independent_node_replay_equal": True,
        "attacker_read_images": False,
        "attacker_read_truth_before_export": False,
    }


def main():
    outputs = []
    for _ in range(2):
        with tempfile.TemporaryDirectory(prefix="e002_602_private_") as temp:
            root = Path(temp) / "packet"
            outputs.append(run_one(root, secrets.token_hex(24)))
    assert outputs[0] == outputs[1], "seed-invariance control failed"
    print(json.dumps({
        "experiment": "E002-602",
        "evidence_tier": "SYNTHETIC_INSTRUMENT_FALSIFICATION",
        "private_seed_trials": len(outputs),
        "result": outputs[0],
        "human_raters": 0,
        "physical_shutter_calibrations": 0,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
