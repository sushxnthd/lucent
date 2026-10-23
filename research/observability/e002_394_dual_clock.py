#!/usr/bin/env python3
"""E002-394: independently parse Phantom clock; virtual-shutter EEG-marker coverage.
Human event markers are NOT aperture labels. No hard no-closure certificates.
"""
import argparse
import csv
import hashlib
import io
import json
import math
import pathlib
import re
import statistics
import zipfile

SOURCE_MD5 = "fef02cb7ebf62e4f3efb6303284fd6cb"
THRESHOLDS = (0.015, 0.020, 0.030, 0.050)
RATES = (30, 60, 120)
EXPOSURES = (0.001, 0.005, 0.010)
PHASES = 100

def digest(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def number(raw):
    try:
        v = float(raw)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None

def phantom_seconds(raw):
    """No data-fitted unit conversion: accept explicit seconds or clock HH:MM:SS."""
    raw = (raw or "").strip()
    v = number(raw)
    if v is not None:
        return v, "numeric_seconds"
    m = re.fullmatch(r"(\d{1,2}):(\d{2}):(\d{2})(?:[.,](\d+))?", raw)
    if m:
        hh, mm, ss = map(int, m.group(1, 2, 3))
        if mm >= 60 or ss >= 60:
            return None, "unparseable"
        fraction = float("0." + m.group(4)) if m.group(4) else 0.0
        return hh * 3600 + mm * 60 + ss + fraction, "clock_hhmmss"
    return None, "unparseable"

def percentile(values, p):
    if not values:
        return None
    s = sorted(values)
    return s[min(len(s) - 1, int(p * (len(s) - 1)))]

def analyze(archive, verified):
    with zipfile.ZipFile(archive) as z:
        names = sorted(n for n in z.namelist() if n.endswith("_sync.csv"))
        if len(names) != 1:
            raise RuntimeError("Expected exactly one sync sidecar")
        with z.open(names[0]) as f:
            reader = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig"))
            required = {"Time", "PhanFrame", "PhanTime", "Blinks"}
            if not required.issubset(set(reader.fieldnames or [])):
                raise RuntimeError("Missing required synchronization fields")
            frames = []
            markers = []
            rows = 0
            parse_modes = {}
            for row in reader:
                rows += 1
                t, fid = number(row.get("Time")), number(row.get("PhanFrame"))
                b = number(row.get("Blinks"))
                if t is not None and b is not None and b > 0:
                    markers.append(t)
                if t is None or fid is None:
                    continue
                p, mode = phantom_seconds(row.get("PhanTime"))
                parse_modes[mode] = parse_modes.get(mode, 0) + 1
                frames.append((int(fid), t, p))
    if len(frames) < 100:
        raise RuntimeError("Insufficient human camera synchronization")
    if len({f[0] for f in frames}) != len(frames):
        raise RuntimeError("Repeated Phantom frame IDs; explicit resolution required")
    frame_steps = [(b[0]-a[0], b[1]-a[1], None if a[2] is None or b[2] is None else b[2]-a[2])
                   for a, b in zip(frames, frames[1:])]
    if any(df <= 0 or dt <= 0 for df, dt, dp in frame_steps):
        raise RuntimeError("Nonmonotonic Phantom IDs or EEG times")
    rates = {}
    for threshold in THRESHOLDS:
        active = [(df, dt) for df, dt, dp in frame_steps if dt <= threshold]
        gap = [dt for df, dt, dp in frame_steps if dt > threshold]
        rates[str(int(threshold*1000))+"ms"] = {
            "active_fps": sum(df for df, dt in active) / sum(dt for df, dt in active),
            "gap_count": len(gap),
            "gap_total_s": sum(gap),
            "active_frame_steps": sum(df for df, dt in active),
            "active_elapsed_s": sum(dt for df, dt in active)
        }
    rate_spread = max(v["active_fps"] for v in rates.values()) - min(v["active_fps"] for v in rates.values())
    parsed = [f for f in frames if f[2] is not None]
    parse_fraction = len(parsed)/len(frames)
    modes = sorted((mode, n) for mode, n in parse_modes.items() if mode != "unparseable")
    phantom = {"parse_modes": parse_modes, "parse_fraction": parse_fraction,
               "qualified": False, "reason": "insufficient_or_ambiguous_clock"}
    if parse_fraction >= 0.99 and len(modes) == 1:
        # A long-baseline ratio only if the camera clock has plausible seconds units.
        pp = [(df, dt, dp) for df, dt, dp in frame_steps if dp is not None]
        nonmonotonic = sum(dp <= 0 for df, dt, dp in pp)
        active = [(df, dt, dp) for df, dt, dp in pp if dt <= .020 and dp > 0]
        residuals = [abs(dp-dt) for df, dt, dp in active]
        med_dp = statistics.median([dp/df for df, dt, dp in active]) if active else None
        plausible = med_dp is not None and 0.002 <= med_dp <= 0.020
        phantom.update({
            "nonmonotonic_steps": nonmonotonic,
            "median_phantom_step_s": med_dp,
            "active_phantom_fps": sum(df for df, dt, dp in active)/sum(dp for df, dt, dp in active) if active else None,
            "interclock_abs_step_residual_p95_s": percentile(residuals, .95),
            "interclock_step_fraction_le_2ms": sum(r <= .002000001 for r in residuals)/len(residuals) if residuals else None,
            "qualified": bool(plausible and nonmonotonic == 0),
            "reason": "independent_seconds_clock" if plausible and nonmonotonic == 0 else "implausible_or_nonmonotonic_phantom_clock"
        })
    gaps = [(a[1], b[1]) for a,b in zip(frames, frames[1:]) if b[1]-a[1] > .020]
    start, end = frames[0][1], frames[-1][1]
    eligible = [t for t in markers if start <= t <= end and
                not any(a < t < b for a,b in gaps)]
    capture = {}
    for hz in RATES:
        period = 1.0/hz
        for exposure in EXPOSURES:
            per_phase = []
            for k in range(PHASES):
                phi = (k+0.5)*period/PHASES
                n = sum(1 for t in eligible if ((t-phi) % period) < exposure)
                per_phase.append(n)
            observed = sum(per_phase)/(PHASES*len(eligible)) if eligible else None
            expected = min(1.0, exposure/period)
            capture[f"{hz}Hz_{int(exposure*1000)}ms"] = {
                "eligible_event_markers": len(eligible),
                "mean_phase_capture_fraction": observed,
                "expected_uniform_phase_fraction": expected,
                "abs_error": abs(observed-expected) if observed is not None else None,
                "min_markers_captured_per_phase": min(per_phase),
                "max_markers_captured_per_phase": max(per_phase),
                "passes_duty_cycle_prediction": observed is not None and abs(observed-expected) <= .03,
                "measurement": "EEG marker timestamp within hypothetical shutter; NOT physical blink detection"
            }
    return {
        "experiment": "E002-394", "source_verified": verified, "source_md5": digest(archive),
        "sync_rows": rows, "distinct_phantom_frames": len(frames),
        "avi_reported_fps_from_previous_verified_run": 1,
        "primary_publication_nominal_fps": 150,
        "EEG_clock_1ms_quantized": True,
        "EEG_gap_sensitivity": rates, "active_rate_spread_fps": rate_spread,
        "active_rate_stable_within_1fps": rate_spread <= 1,
        "PhanTime_independent_clock": phantom,
        "frozen_interclock_prediction_passed": bool(phantom.get("qualified") and
             phantom.get("interclock_step_fraction_le_2ms", 0) >= .95),
        "marker_count": len(markers), "eligible_markers": len(eligible),
        "excluded_markers": len(markers)-len(eligible),
        "hypothetical_shutter_marker_coverage": capture,
        "all_phase_duty_cycle_predictions_passed": all(v["passes_duty_cycle_prediction"] for v in capture.values()),
        "physical_aperture_reference": False,
        "actual_shutter_exposure_known": False,
        "product_decision": "ABSTAIN_UNCALIBRATED"
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--archive", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--fixture", action="store_true", help="Explicit unverified fixture; never human evidence")
    args = p.parse_args()
    verified = digest(args.archive) == SOURCE_MD5
    if not args.fixture and not verified:
        raise RuntimeError("Source archive MD5 mismatch")
    out = pathlib.Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    result = analyze(args.archive, verified)
    (out/"e002_394_dual_clock.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({
        "source_verified": verified, "frames": result["distinct_phantom_frames"],
        "rate_spread_fps": result["active_rate_spread_fps"],
        "phantom_clock": result["PhanTime_independent_clock"],
        "markers_eligible": result["eligible_markers"],
        "all_phase_predictions_passed": result["all_phase_duty_cycle_predictions_passed"],
        "product_decision": result["product_decision"]
    }, indent=2))

if __name__ == "__main__":
    main()
