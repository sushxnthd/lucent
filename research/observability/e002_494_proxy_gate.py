#!/usr/bin/env python3
"""E002-494: fail-closed claim gate for E002-493 authentic S01 proxy evidence.

Research-only gate. It cannot certify anatomical closure, timing, or fatigue.
"""
import argparse
import json
from pathlib import Path

EXPECTED = (
    "baseline", "brightness_plus8", "contrast_90pct", "blur_3x3",
    "alternating_jitter_1px", "stride2",
)

def assess(report):
    """Validate the frozen aggregate, always abstaining on physical claims."""
    decision = {
        "experiment": "E002-494", "source": "E002-493",
        "proxy_for_robust_event_selection": "REJECT",
        "anatomical_closure": "ABSTAIN_UNCALIBRATED",
        "blink_duration": "ABSTAIN_UNCALIBRATED",
        "PERCLOS": "ABSTAIN_UNCALIBRATED",
        "fatigue": "ABSTAIN_UNCALIBRATED",
        "medical": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
        "reason": "INVALID_OR_INCOMPLETE_EVIDENCE",
    }
    if not isinstance(report, dict):
        return decision
    if (report.get("experiment") != "E002-493" or
        report.get("evidence_tier") != "AUTHENTIC_HUMAN_IMAGE_PROXY_NUISANCE_TEST_ONLY" or
        report.get("subject") != "S01_CALIBRATION_ONLY" or
        report.get("frozen_review_clips") != 20 or
        report.get("native_frame_positions") != 260 or
        report.get("anatomical_closure_labels") != 0 or
        report.get("human_reference_validated") is not False or
        report.get("acquisition_fps_authenticated") is not False or
        report.get("physical_hidden_closure_certified") is not False or
        report.get("product") != "ABSTAIN_UNCALIBRATED" or
        report.get("release") != "BLOCKED"):
        return decision
    conditions = report.get("conditions")
    if not isinstance(conditions, dict) or set(conditions) != set(EXPECTED):
        return decision
    base = conditions["baseline"]
    if not isinstance(base, dict):
        return decision
    baseline_ok = (base.get("candidate_clip_positive") is True and
                   base.get("control_clip_candidates") == 0)
    for name in EXPECTED:
        c = conditions[name]
        if not isinstance(c, dict):
            return decision
        count = c.get("analyzed_pairs")
        if type(count) is not int or count != (120 if name == "stride2" else 240):
            return decision
        nums = [c.get(k) for k in (
            "eligible_pairs", "nuisance_abstentions", "duplicate_pairs",
            "proxy_candidates", "candidate_clip_candidates",
            "control_clip_candidates")]
        if any(type(n) is not int or n < 0 for n in nums):
            return decision
        eligible, nuisance, duplicate, candidates, candidate_clip, controls = nums
        if (eligible + nuisance + duplicate != count or
            candidates != candidate_clip + controls or
            candidates > eligible or
            c.get("candidate_clip_positive") is not (candidate_clip > 0)):
            return decision
        fraction = c.get("eligible_fraction")
        if (type(fraction) not in (int, float) or
            abs(fraction - eligible / count) > 1e-5):
            return decision
        if not baseline_ok:
            verdict = "BASELINE_NOT_REPRODUCED"
        else:
            fail = (not c["candidate_clip_positive"] or
                    controls > 0 or eligible / count < .8)
            verdict = ("FAIL" if fail else
                       ("REPRODUCED" if name == "baseline"
                        else "SURVIVES_THIS_FIXTURE_ONLY"))
        if c.get("verdict") != verdict:
            return decision
    if report.get("baseline_reproduced") is not True:
        return decision
    failed = [n for n in EXPECTED if conditions[n]["verdict"] == "FAIL"]
    decision["reason"] = ("AUTHENTIC_NUISANCE_FALSIFICATION" if failed
                          else "UNVALIDATED_SINGLE_SUBJECT_PROXY")
    if failed:
        decision["failed_conditions"] = failed
    return decision

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aggregate", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        report = json.loads(Path(args.aggregate).read_text())
        decision = assess(report)
    except (OSError, ValueError, TypeError):
        decision = assess(None)
    Path(args.output).write_text(json.dumps(decision, indent=2, sort_keys=True) + "\n")
    print(json.dumps(decision, sort_keys=True))
    return 0 if decision["reason"] != "INVALID_OR_INCOMPLETE_EVIDENCE" else 2

if __name__ == "__main__":
    raise SystemExit(main())
