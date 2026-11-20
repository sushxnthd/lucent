#!/usr/bin/env python3
"""E002-585: local-only, privacy-minimizing human anatomical rating gate.

NO human data included. Validates metadata and two blinded framewise rating
sets. Never emits raw rows, clip IDs, participant IDs, or physical certificates.
Does NOT establish sensor shutter metrology or a physiological velocity bound.
"""
from __future__ import annotations
import argparse
import collections
import copy
import hashlib
import json
import math
import re
from pathlib import Path

TAU = 0.2
DISAGREEMENT = 0.15
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SPLITS = {"calibration", "holdout"}
CLASSES = ("CLOSED", "OPEN", "UNCERTAIN")


def reject(reason):
    raise ValueError(reason)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def interval(x):
    if x is None:
        return None
    if (not isinstance(x, list) or len(x) != 2
            or any(type(v) not in (int, float) or not math.isfinite(v) for v in x)):
        reject("BAD_APERTURE_INTERVAL")
    lo, hi = x
    if not (0 <= lo <= hi <= 1):
        reject("BAD_APERTURE_INTERVAL")
    return lo, hi


def anatomical_class(a, b, *, nuisance=False):
    if nuisance or a is None or b is None:
        return "UNCERTAIN"
    a, b = interval(a), interval(b)
    if a is None or b is None:
        return "UNCERTAIN"
    if abs((a[0]+a[1]-b[0]-b[1])/2) > DISAGREEMENT + 1e-12:
        return "UNCERTAIN"
    lo, hi = min(a[0], b[0]), max(a[1], b[1])
    if hi <= TAU:
        return "CLOSED"
    if lo > TAU:
        return "OPEN"
    return "UNCERTAIN"


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or manifest.get("protocol_id") != "E002-585":
        reject("PROTOCOL_MISMATCH")
    if manifest.get("tau") != TAU:
        reject("THRESHOLD_NOT_FROZEN")
    clips = manifest.get("clips")
    if not isinstance(clips, list) or not clips:
        reject("EMPTY_CLIPS")
    seen, participants, splits = set(), {}, set()
    for clip in clips:
        if not isinstance(clip, dict):
            reject("BAD_CLIP")
        cid, pid, split = (clip.get(x) for x in ("clip_id", "participant_id", "split"))
        if not isinstance(cid, str) or not cid or not isinstance(pid, str) or not pid:
            reject("MISSING_PSEUDONYM")
        if cid in seen or split not in SPLITS:
            reject("DUPLICATE_CLIP_OR_BAD_SPLIT")
        seen.add(cid)
        splits.add(split)
        if pid in participants and participants[pid] != split:
            reject("PARTICIPANT_SPLIT_LEAKAGE")
        participants[pid] = split
        n = clip.get("frames")
        if type(n) is not int or n < 1 or n > 100000:
            reject("BAD_FRAME_COUNT")
        flags = clip.get("nuisance_flags")
        if not isinstance(flags, list) or any(not isinstance(x, str) or not x for x in flags):
            reject("BAD_NUISANCE_FLAGS")
        times = clip.get("frame_time_bounds_ms")
        if times is not None:
            if not isinstance(times, list) or len(times) != n:
                reject("BAD_TIME_BOUNDS")
            previous_hi = float("-inf")
            for t in times:
                if (not isinstance(t, list) or len(t) != 2 or
                        any(type(x) not in (int, float) or not math.isfinite(x) for x in t)):
                    reject("BAD_TIME_BOUNDS")
                lo, hi = t
                if lo > hi or lo <= previous_hi:
                    reject("BAD_TIME_BOUNDS")
                previous_hi = hi
        for field in ("clock_sha256", "shutter_sha256", "geometry_sha256"):
            val = clip.get(field)
            if val is not None and (not isinstance(val, str) or not HEX64.fullmatch(val)):
                reject("BAD_PROVENANCE_DIGEST")
    if splits != SPLITS:
        reject("MISSING_PARTICIPANT_DISJOINT_HOLDOUT")
    return clips


def validate_rater(rater, clip_map):
    if not isinstance(rater, dict) or not isinstance(rater.get("rater_id"), str) or not rater["rater_id"]:
        reject("BAD_RATER_ID")
    ratings = rater.get("ratings")
    if not isinstance(ratings, dict) or set(ratings) != set(clip_map):
        reject("MISSING_OR_EXTRA_RATER_CLIPS")
    for cid, values in ratings.items():
        if not isinstance(values, list) or len(values) != clip_map[cid]["frames"]:
            reject("BAD_RATING_FRAME_COUNT")
        for x in values:
            interval(x)


def audit(manifest, rater_a, rater_b, velocity_cert=None):
    clips = validate_manifest(manifest)
    clip_map = {x["clip_id"]: x for x in clips}
    validate_rater(rater_a, clip_map)
    validate_rater(rater_b, clip_map)
    if rater_a["rater_id"] == rater_b["rater_id"]:
        reject("NONINDEPENDENT_RATER_IDS")
    counts = {split: collections.Counter() for split in sorted(SPLITS)}
    metadata_missing = collections.Counter()
    for clip in clips:
        cid, split = clip["clip_id"], clip["split"]
        for field in ("clock_sha256", "shutter_sha256", "geometry_sha256", "frame_time_bounds_ms"):
            if not clip.get(field):
                metadata_missing[field] += 1
        nuisance = bool(clip["nuisance_flags"])
        for a, b in zip(rater_a["ratings"][cid], rater_b["ratings"][cid]):
            counts[split][anatomical_class(a, b, nuisance=nuisance)] += 1
    vel_ok = (isinstance(velocity_cert, dict)
              and velocity_cert.get("independently_justified") is True
              and type(velocity_cert.get("hard_upper_bound_per_s")) in (int, float)
              and math.isfinite(velocity_cert["hard_upper_bound_per_s"])
              and velocity_cert["hard_upper_bound_per_s"] > 0
              and isinstance(velocity_cert.get("evidence_sha256"), str)
              and bool(HEX64.fullmatch(velocity_cert["evidence_sha256"])))
    if not vel_ok:
        metadata_missing["independent_velocity_certificate"] += 1
    # This program cannot authenticate the external evidence: metadata alone
    # never upgrades a physical no-hidden-closure decision.
    return {
        "experiment": "E002-585",
        "evidence_tier": "LOCAL_ANNOTATION_INSTRUMENT_ONLY",
        "participants": len({x["participant_id"] for x in clips}),
        "clips": len(clips),
        "framewise_reference_counts": {
            split: {cls: counts[split][cls] for cls in CLASSES}
            for split in sorted(SPLITS)
        },
        "missing_or_unverified_metadata_counts": dict(sorted(metadata_missing.items())),
        "metadata_claims_present": not bool(metadata_missing),
        "external_evidence_authenticated_by_this_tool": False,
        "certified_no_hidden_closure": False,
        "physical_decision": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


def fixtures():
    h = "a" * 64
    clips = [
        {"clip_id": "A", "participant_id": "P1", "split": "calibration",
         "frames": 4, "frame_time_bounds_ms": [[0, 1], [10, 11], [20, 21], [30, 31]],
         "clock_sha256": h, "shutter_sha256": h, "geometry_sha256": h, "nuisance_flags": []},
        {"clip_id": "B", "participant_id": "P2", "split": "holdout",
         "frames": 2, "frame_time_bounds_ms": [[0, 1], [10, 11]],
         "clock_sha256": h, "shutter_sha256": h, "geometry_sha256": h, "nuisance_flags": []},
    ]
    m = {"protocol_id": "E002-585", "tau": TAU, "clips": clips}
    a = {"rater_id": "R1", "ratings": {"A": [[.05,.10],[.6,.7],[.17,.23],None],
                                     "B": [[.1,.12],[.8,.9]]}}
    b = {"rater_id": "R2", "ratings": {"A": [[.08,.12],[.62,.72],[.18,.24],[.5,.6]],
                                     "B": [[.4,.5],[.81,.91]]}}
    r = audit(m,a,b)
    assert r["framewise_reference_counts"]["calibration"] == {"CLOSED":1,"OPEN":1,"UNCERTAIN":2}
    assert r["framewise_reference_counts"]["holdout"] == {"CLOSED":0,"OPEN":1,"UNCERTAIN":1}
    assert r["physical_decision"] == "ABSTAIN_UNCALIBRATED"
    cert = {"independently_justified":True,"hard_upper_bound_per_s":10,"evidence_sha256":h}
    assert audit(m,a,b,cert)["metadata_claims_present"]
    assert not audit(m,a,b,cert)["certified_no_hidden_closure"]
    def fails(mm,aa,bb,expected):
        try:
            audit(mm,aa,bb)
        except ValueError as e:
            assert str(e) == expected, (str(e),expected)
        else:
            raise AssertionError("FAILED_TO_REJECT_"+expected)
    mm=copy.deepcopy(m);mm["clips"][1]["participant_id"]="P1"
    fails(mm,a,b,"PARTICIPANT_SPLIT_LEAKAGE")
    bb=copy.deepcopy(b);bb["rater_id"]="R1"
    fails(m,a,bb,"NONINDEPENDENT_RATER_IDS")
    bb=copy.deepcopy(b);bb["ratings"]["B"]=[[.4,.5]]
    fails(m,a,bb,"BAD_RATING_FRAME_COUNT")
    bb=copy.deepcopy(b);bb["ratings"]["B"][0]=[.9,.2]
    fails(m,a,bb,"BAD_APERTURE_INTERVAL")
    mm=copy.deepcopy(m);mm["clips"][0]["frame_time_bounds_ms"][1]=[.5,11]
    fails(mm,a,b,"BAD_TIME_BOUNDS")
    mm=copy.deepcopy(m);mm["clips"][0]["clock_sha256"]="not-a-hash"
    fails(mm,a,b,"BAD_PROVENANCE_DIGEST")
    mm=copy.deepcopy(m);mm["clips"][1]["nuisance_flags"]=["glasses_reflection"]
    rr=audit(mm,a,b)
    assert rr["framewise_reference_counts"]["holdout"]["UNCERTAIN"] == 2
    mm=copy.deepcopy(m);mm["clips"][0]["shutter_sha256"]=None
    assert audit(mm,a,b,cert)["physical_decision"] == "ABSTAIN_UNCALIBRATED"
    assert audit(mm,a,b,cert)["missing_or_unverified_metadata_counts"]["shutter_sha256"] == 1
    return {"synthetic_fixture_groups_passed": 10, "human_data": False,
            "independent_rater_pairs_obtained": 0, "physical_shutter_captures": 0,
            "product": "ABSTAIN_UNCALIBRATED", "release": "BLOCKED"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--manifest")
    p.add_argument("--rater-a")
    p.add_argument("--rater-b")
    p.add_argument("--velocity-cert")
    args=p.parse_args()
    if args.self_test:
        print(json.dumps(fixtures(),sort_keys=True))
        return
    if not (args.manifest and args.rater_a and args.rater_b):
        p.error("manifest and two independently produced rater files are required")
    def load(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    result=audit(load(args.manifest),load(args.rater_a),load(args.rater_b),
                 load(args.velocity_cert) if args.velocity_cert else None)
    result["input_sha256"]={key:sha256_file(path) for key,path in
        (("manifest",args.manifest),("rater_a",args.rater_a),("rater_b",args.rater_b))}
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
