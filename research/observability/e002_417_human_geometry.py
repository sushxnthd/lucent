#!/usr/bin/env python3
"""E002-417 real-human two-method pixel-gap falsification; never physical aperture."""
from __future__ import annotations
import argparse
import json
import shutil
import tempfile
from pathlib import Path
import cv2
import numpy as np

VARIANTS = ("gain070", "gain130", "blur2", "translate8_6", "white_glare")
REQUIRED_TRANSFER = VARIANTS[:-1]

def _gate(gray):
    if not isinstance(gray, np.ndarray) or gray.shape != (130, 190) or gray.dtype != np.uint8:
        raise ValueError("Expected 130x190 uint8 eye crop")
    if np.mean(gray[60:90, 75:105] >= 250) >= .75:
        return False
    return float(np.std(gray[25:105, 65:125])) >= 8.

def _profile(gray):
    return np.median(cv2.GaussianBlur(gray, (0, 0), 1.0)[:, 75:115], axis=1)

def gradient_gap(gray):
    """A: opposite-polarity horizontal intensity edges; not anatomical landmarks."""
    if not _gate(gray):
        return None
    d = np.diff(_profile(gray))
    top = int(np.argmin(d[25:65])) + 25
    bottom = int(np.argmax(d[60:105])) + 60
    gap = bottom - top
    if d[top] > -1.5 or d[bottom] < 1.5 or not 2 <= gap <= 65:
        return None
    return float(gap)

def threshold_gap(gray):
    """B: adaptive dark-region extent; not independently verified lid margins."""
    if not _gate(gray):
        return None
    profile = _profile(gray)
    skin = float(np.median(np.concatenate((profile[5:25], profile[105:125]))))
    if not 35 < skin < 245:
        return None
    dark = profile < skin - max(12., .14 * skin)
    seed = int(np.argmin(profile[40:90])) + 40
    if not dark[seed]:
        return None
    a = b = seed
    while a > 0 and dark[a - 1]:
        a -= 1
    while b < len(dark) - 1 and dark[b + 1]:
        b += 1
    gap = b - a + 1
    if not 2 <= gap <= 65 or a < 20 or b > 110:
        return None
    return float(gap)

def transform(gray, variant):
    if variant == "gain070":
        return np.clip(gray.astype(np.float32) * .70, 0, 255).astype(np.uint8)
    if variant == "gain130":
        return np.clip(gray.astype(np.float32) * 1.30, 0, 255).astype(np.uint8)
    if variant == "blur2":
        return cv2.GaussianBlur(gray, (0, 0), 2.0)
    if variant == "translate8_6":
        return cv2.warpAffine(gray, np.float32([[1, 0, 8], [0, 1, 6]]),
                              (190, 130), borderMode=cv2.BORDER_REFLECT_101)
    if variant == "white_glare":
        out = gray.copy()
        out[60:90, 75:105] = 255
        return out
    raise ValueError("Unknown transform")

def estimate(gray):
    return gradient_gap(gray), threshold_gap(gray)

def measure(gray):
    return {v: estimate(gray if v == "clean" else transform(gray, v))
            for v in ("clean",) + VARIANTS}

def idealized_control():
    img = np.full((130, 190), 180, dtype=np.uint8)
    img[50:74, :] = 40
    a, b = estimate(img)
    return a is not None and b is not None and abs(a - 24) <= 3 and abs(b - 24) <= 3

def summarize(records, clips):
    """All-frame denominators; missing or invalid nuisance outputs are failures."""
    n = len(records)
    if not n:
        raise ValueError("Empty source frames")
    clean = [r["clean"] for r in records]
    joint = [r for r in records if all(x is not None for x in r["clean"])]
    agreement = sum(abs(a - b) <= 5 for a, b in (r["clean"] for r in joint))
    nuisance = {}
    for v in VARIANTS:
        all_valid = sum(all(x is not None for x in r[v]) for r in records)
        retained = sum(all(x is not None for x in r[v]) for r in joint)
        stable = sum(all(x is not None for x in r[v]) and
                     all(abs(a - b) <= 3 for a, b in zip(r["clean"], r[v]))
                     for r in joint)
        abstain_both = sum(all(x is None for x in r[v]) for r in records)
        nuisance[v] = {
            "all_frame_joint_valid": all_valid,
            "all_frame_joint_valid_fraction": round(all_valid / n, 6),
            "clean_joint_valid_denominator": len(joint),
            "retained_joint_valid": retained,
            "retained_and_stable": stable,
            "retained_and_stable_fraction": round(stable / len(joint), 6) if joint else None,
            "both_abstain": abstain_both,
            "both_abstain_fraction": round(abstain_both / n, 6),
        }
    h = {
        "H1_source_coverage": clips == 8 and n >= 600,
        "H2_joint_coverage_and_agreement": agreement / n >= .60,
        "H3_all_four_transfer_conditions": len(joint) > 0 and all(
            nuisance[v]["retained_and_stable_fraction"] >= .95
            for v in REQUIRED_TRANSFER),
        "H4_white_glare_both_abstain": nuisance["white_glare"]["both_abstain_fraction"] >= .95,
        "H5_synthetic_control_and_no_product": idealized_control(),
    }
    return {
        "experiment": "E002-417",
        "evidence_tier": "human eye video; automated pixel-space candidate only",
        "clips": clips, "source_frame_occurrences": n,
        "clean_A_valid": sum(a is not None for a, _ in clean),
        "clean_B_valid": sum(b is not None for _, b in clean),
        "clean_joint_valid": len(joint),
        "clean_joint_agree_within_5px": agreement,
        "clean_joint_agree_all_frame_fraction": round(agreement / n, 6),
        "nuisance": nuisance, "hypotheses": h,
        "joint_transfer_gate_pass": all(h.values()),
        "human_raters": 0, "physical_aperture_validated": False,
        "independent_camera_exposure_calibrated": False,
        "independent_hard_velocity_bound": False,
        "product_claim_authorized": False, "product": "ABSTAIN_UNCALIBRATED",
    }

def evaluate_archive(archive, participant):
    import e002_412_human_proxy_aliasing as source
    z, video, _, frame_count, ranges = source.select_clips(Path(archive), participant)
    needed = {i for a, b in ranges for i in range(a, b + 1)}
    observations = {}
    try:
        with tempfile.TemporaryDirectory(prefix="lucent-e002-417-") as tmp:
            path = Path(tmp) / "source.avi"
            with z.open(video) as inp, path.open("wb") as out:
                shutil.copyfileobj(inp, out, 1 << 20)
            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened() or int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != frame_count:
                raise ValueError("Source video/synchronization mismatch")
            i = 0
            try:
                while True:
                    ok, frame = cap.read()
                    if not ok:
                        break
                    if i in needed:
                        if frame.shape[:2] != (288, 320):
                            raise ValueError("Unexpected video dimensions")
                        crop = cv2.cvtColor(frame[90:220, 70:260], cv2.COLOR_BGR2GRAY)
                        observations[i] = measure(crop)
                    i += 1
            finally:
                cap.release()
            if i != frame_count or set(observations) != needed:
                raise ValueError("Incomplete source frame decode")
    finally:
        z.close()
    return [observations[i] for a, b in ranges for i in range(a, b + 1)], len(ranges)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--s01", type=Path, required=True)
    p.add_argument("--s19", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    x, nx = evaluate_archive(a.s01, "S01")
    y, ny = evaluate_archive(a.s19, "S19")
    result = summarize(x + y, nx + ny)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
