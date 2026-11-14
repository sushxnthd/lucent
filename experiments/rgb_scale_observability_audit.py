"""RGB scale-confound audit for Lucent.

Uses the public scale-stress outputs from CondadosAI's independent
PupilSense/EyeDentify reproduction. No human-subject images are downloaded;
the script fetches only derived CSV outputs already published in that repo.

This audit does NOT validate phone RGB pupillometry or fatigue prediction.
It asks a narrower engineering question: are released PupilSense millimetre
predictions stable enough to apparent-scale changes to serve as Lucent's
relative response observable?
"""

from __future__ import annotations

import argparse
import io
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import requests

BASE = "https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/main/output"
FILES = [
    "scale_All_Smiles_Ahead.csv",
    "scale_And_it_was_all_Yellow.csv",
    "scale_Blink_It_Like_Brian.csv",
    "scale_Funny_Talks.csv",
    "scale_I_like_to_move_it_move_it.csv",
    "scale_Infinite_Blue.csv",
    "scale_Red_Ross.csv",
    "scale_focus_pocus.csv",
]
EYES = ("left_mm", "right_mm")
TIGHT_SCALES = (0.9, 1.0, 1.1)


def fetch_csv(name: str) -> pd.DataFrame:
    url = f"{BASE}/{name}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    frame = pd.read_csv(io.StringIO(response.text))
    required = {
        "scale", "frame", "left_mm", "right_mm", "eye_box_w_px", "fill_w_pct"
    }
    missing = required.difference(frame.columns)
    if missing:
        raise RuntimeError(f"{name}: missing columns {sorted(missing)}")
    return frame


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(a - b))))


def paired_by_frame(df: pd.DataFrame) -> dict[float, pd.DataFrame]:
    out: dict[float, pd.DataFrame] = {}
    for scale, part in df.groupby("scale"):
        out[float(scale)] = part.sort_values("frame").reset_index(drop=True)
    if 1.0 not in out:
        raise RuntimeError("scale=1.0 reference is missing")
    n = len(out[1.0])
    if any(len(v) != n for v in out.values()):
        raise RuntimeError("scale rows are not frame-aligned")
    return out


def binocular_tight_confound(df: pd.DataFrame) -> dict[str, float]:
    by = paired_by_frame(df)
    missing = set(TIGHT_SCALES).difference(by)
    if missing:
        raise RuntimeError(f"tight scales missing: {sorted(missing)}")

    ref = ((by[1.0]["left_mm"] + by[1.0]["right_mm"]) / 2.0).to_numpy()
    temporal_ptp = float(np.ptp(ref))

    matrix = np.vstack(
        [((by[s]["left_mm"] + by[s]["right_mm"]) / 2.0).to_numpy()
         for s in TIGHT_SCALES]
    )
    mean_false_range = float(np.mean(np.ptp(matrix, axis=0)))
    ratio = math.inf if temporal_ptp == 0 else mean_false_range / temporal_ptp
    return {
        "reference_temporal_peak_to_peak_mm": temporal_ptp,
        "mean_false_range_0p9_to_1p1_mm": mean_false_range,
        "false_range_to_signal_ratio": ratio,
    }


def build_pairs(df: pd.DataFrame, eye: str, alpha: float, tight_only: bool) -> tuple[np.ndarray, np.ndarray]:
    by = paired_by_frame(df)
    ref = by[1.0]
    ref_width = float(ref["eye_box_w_px"].median())
    pred: list[float] = []
    target: list[float] = []

    for scale, part in by.items():
        if scale == 1.0:
            continue
        if tight_only and not (0.9 <= scale <= 1.1):
            continue
        widths = part["eye_box_w_px"].to_numpy(dtype=float)
        values = part[eye].to_numpy(dtype=float)
        corrected = values * np.power(ref_width / widths, alpha)
        pred.extend(corrected.tolist())
        target.extend(ref[eye].to_numpy(dtype=float).tolist())

    return np.asarray(pred), np.asarray(target)


def select_alpha(train: list[pd.DataFrame], eye: str) -> float:
    best_alpha = 0.0
    best_mse = math.inf
    for alpha in np.round(np.arange(-2.0, 2.0001, 0.05), 2):
        ps: list[np.ndarray] = []
        ys: list[np.ndarray] = []
        for df in train:
            p, y = build_pairs(df, eye, float(alpha), tight_only=False)
            ps.append(p)
            ys.append(y)
        p_all = np.concatenate(ps)
        y_all = np.concatenate(ys)
        mse = float(np.mean(np.square(p_all - y_all)))
        if mse < best_mse:
            best_mse = mse
            best_alpha = float(alpha)
    return best_alpha


def power_law_loco(clips: list[tuple[str, pd.DataFrame]]) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for held_idx, (held_name, held_df) in enumerate(clips):
        train = [df for i, (_, df) in enumerate(clips) if i != held_idx]
        for eye in EYES:
            alpha = select_alpha(train, eye)

            p0, y0 = build_pairs(held_df, eye, 0.0, tight_only=False)
            pc, yc = build_pairs(held_df, eye, alpha, tight_only=False)
            p0t, y0t = build_pairs(held_df, eye, 0.0, tight_only=True)
            pct, yct = build_pairs(held_df, eye, alpha, tight_only=True)

            rows.append({
                "clip": held_name,
                "eye": eye,
                "alpha": alpha,
                "rmse_raw_mm": rmse(p0, y0),
                "rmse_corrected_mm": rmse(pc, yc),
                "tight_rmse_raw_mm": rmse(p0t, y0t),
                "tight_rmse_corrected_mm": rmse(pct, yct),
            })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    clips = [(name.removeprefix("scale_").removesuffix(".csv"), fetch_csv(name))
             for name in FILES]

    clip_metrics = []
    for name, df in clips:
        metric = {"clip": name, **binocular_tight_confound(df)}
        clip_metrics.append(metric)

    ratios = np.asarray([m["false_range_to_signal_ratio"] for m in clip_metrics], dtype=float)
    loco = power_law_loco(clips)

    raw = np.asarray([r["rmse_raw_mm"] for r in loco], dtype=float)
    corr = np.asarray([r["rmse_corrected_mm"] for r in loco], dtype=float)
    raw_tight = np.asarray([r["tight_rmse_raw_mm"] for r in loco], dtype=float)
    corr_tight = np.asarray([r["tight_rmse_corrected_mm"] for r in loco], dtype=float)

    result = {
        "source": "CondadosAI/pupil-diameter-webcam scale-stress outputs",
        "n_clips": len(clips),
        "clip_metrics": clip_metrics,
        "tight_scale_summary": {
            "mean_false_range_to_signal_ratio": float(np.mean(ratios)),
            "median_false_range_to_signal_ratio": float(np.median(ratios)),
            "clips_false_range_exceeds_reference_signal": int(np.sum(ratios > 1.0)),
        },
        "leave_one_clip_out_power_law_correction": {
            "mean_rmse_raw_mm": float(np.mean(raw)),
            "mean_rmse_corrected_mm": float(np.mean(corr)),
            "mean_tight_rmse_raw_mm": float(np.mean(raw_tight)),
            "mean_tight_rmse_corrected_mm": float(np.mean(corr_tight)),
            "holdouts_improved_all_scales": int(np.sum(corr < raw)),
            "holdouts_improved_tight_scales": int(np.sum(corr_tight < raw_tight)),
            "n_eye_clip_holdouts": len(loco),
            "per_holdout": loco,
        },
        "interpretation_boundary": (
            "Derived scale-confound audit only. It does not establish biological "
            "phone observability, active-probe validity, or fatigue/state prediction."
        ),
    }

    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
