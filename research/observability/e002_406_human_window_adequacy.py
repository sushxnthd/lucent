#!/usr/bin/env python3
"""E002-406: real-human EEG-synchronized temporal adequacy, NOT aperture ground truth.

No source times, clip IDs, event/control labels or eye imagery in public output.
"""
from __future__ import annotations
import argparse
import bisect
import json
import math
import statistics
import zipfile
from pathlib import Path

HALF_WINDOW = 0.250
MAX_GAP = 0.020
SHORT_HALF_FRAMES = 3


def evaluate_window(times, ids, center, half=HALF_WINDOW, max_gap=MAX_GAP):
    """Return only anonymous acquisition-coverage metadata; never infer closure."""
    if len(times) != len(ids) or not (0 <= center < len(times)):
        raise ValueError("Invalid synchronized frame index")
    if any(not math.isfinite(t) for t in times):
        raise ValueError("Nonfinite acquisition clock")
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("Nonmonotonic acquisition clock")
    t = times[center]
    left = bisect.bisect_right(times, t-half)-1
    right = bisect.bisect_left(times, t+half)
    if left < 0 or right >= len(times):
        return {"eligible": False, "reason": "boundary", "frame_count": 0}
    if any(ids[i+1] != ids[i]+1 for i in range(left, right)):
        return {"eligible": False, "reason": "frame_id_discontinuity", "frame_count": 0}
    largest = max(times[i+1]-times[i] for i in range(left, right))
    if largest > max_gap+1e-12:
        return {"eligible": False, "reason": "timing_gap", "frame_count": 0}
    if not (times[left] <= t-half and times[right] >= t+half):
        raise AssertionError("Incomplete requested temporal coverage")
    return {"eligible": True, "reason": "covered", "frame_count": right-left+1,
            "span_s": times[right]-times[left], "max_gap_s": largest}


def quantiles(values):
    if not values:
        return None
    vals = sorted(values)
    def q(p):
        x=(len(vals)-1)*p
        i=int(x)
        return vals[i]*(1-(x-i))+vals[min(i+1,len(vals)-1)]*(x-i)
    return [round(q(p), 8) for p in (.1,.5,.9)]


def run(archive, participant):
    # Import established source parser and deterministic selection only.
    import e002_397_human_motion as prior
    import e002_398_blinded_annotation as blind
    if prior.prior.md5(archive) != prior.MD5[participant]:
        raise RuntimeError("Source checksum mismatch")
    with zipfile.ZipFile(archive) as z:
        _, frames, markers = prior.load_archive(z, participant)
    pairs, _ = prior.select_pairs(frames, markers, participant)
    selected = blind.selected_pairs(pairs)
    centers = [c for _, pair in selected for c in pair]
    assert len(centers) == 40
    ids = [f for f, _ in frames]
    times = [t for _, t in frames]
    spans = [times[k+3]-times[k-3] for k in centers]
    if any(k < 3 or k+3 >= len(times) for k in centers):
        raise RuntimeError("Invalid seven-frame source center")
    windows = [evaluate_window(times, ids, k) for k in centers]
    eligible = [w for w in windows if w["eligible"]]
    reasons = {reason:sum(w["reason"]==reason for w in windows)
               for reason in ("covered","boundary","timing_gap","frame_id_discontinuity")}
    h1 = sum(s < .1 for s in spans) >= 36
    h2 = bool(eligible)
    return {
        "experiment":"E002-406", "participant":participant,
        "evidence_tier":"real-human acquisition-clock coverage only; no aperture annotation",
        "source_checksum_verified":True, "source_frames":len(frames),
        "selected_blinded_centers":len(centers),
        "seven_frame_span_s_p10_p50_p90":quantiles(spans),
        "seven_frame_spans_lt_100ms":sum(s < .1 for s in spans),
        "half_window_s":HALF_WINDOW,"maximum_accepted_gap_s":MAX_GAP,
        "full_window_eligible":len(eligible),
        "full_window_rejection_counts":reasons,
        "eligible_window_frame_count_p10_p50_p90":quantiles([w["frame_count"] for w in eligible]),
        "eligible_window_span_s_p10_p50_p90":quantiles([w["span_s"] for w in eligible]),
        "eligible_max_internal_gap_s_p10_p50_p90":quantiles([w["max_gap_s"] for w in eligible]),
        "frozen_H1_short_packets_lt_100ms_90pct":h1,
        "frozen_H2_any_contiguous_half_second_window":h2,
        "frozen_H3_no_gap_imputation":True,
        "frozen_H4_aggregate_only":True,
        "human_landmark_annotations":0,
        "physical_aperture_ground_truth":False,
        "velocity_hard_bound_established":False,
        "product":"ABSTAIN_UNCALIBRATED",
        "limitation":"Previously studied participants; EEG synchronization is not a calibrated camera exposure clock."
    }


def independent_oracle():
    """Second algorithm, brute-force for randomized synthetic timestamps."""
    import random
    rng=random.Random(406)
    checked=0
    for trial in range(500):
        n=rng.randrange(65,125)
        ts=[0.]
        for i in range(n-1):
            ts.append(ts[-1]+(.1 if i==n//2 and trial%3==0 else rng.uniform(.004,.011)))
        ids=list(range(n))
        if trial%7==0:
            ids[n//2:]=[v+1 for v in ids[n//2:]]
        center=rng.randrange(0,n)
        got=evaluate_window(ts,ids,center)
        t=ts[center]
        eligible_indices=[i for i,s in enumerate(ts) if t-.25<=s<=t+.25]
        # Brute-force find nearest endpoints, independently of bisect.
        ls=[i for i,s in enumerate(ts) if s<=t-.25]
        rs=[i for i,s in enumerate(ts) if s>=t+.25]
        if not ls or not rs:
            expected=False
        else:
            a,b=max(ls),min(rs)
            expected=all(ts[j+1]-ts[j]<=.020+1e-12 and ids[j+1]==ids[j]+1
                         for j in range(a,b))
        if got["eligible"]!=expected:
            raise AssertionError(f"Oracle mismatch on synthetic trial {trial}")
        checked+=1
    # Corrupted clocks must fail, not be sorted or silently repaired.
    for corrupt in ([0.,.01,.01,.03],[0.,.02,.01,.03]):
        try: evaluate_window(corrupt,list(range(len(corrupt))),1)
        except ValueError: pass
        else: raise AssertionError("Nonmonotonic clock accepted")
    return checked


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",type=Path)
    ap.add_argument("--participant",choices=["S01","S19"])
    ap.add_argument("--output",type=Path)
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    if args.self_test:
        print(json.dumps({"independent_oracle_trials":independent_oracle(),"status":"passed"}))
        return
    if not all((args.archive,args.participant,args.output)):
        ap.error("--archive, --participant and --output required")
    report=run(args.archive,args.participant)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
