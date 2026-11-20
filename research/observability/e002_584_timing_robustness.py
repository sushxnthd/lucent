#!/usr/bin/env python3
"""E002-584: timing-uncertainty robustness of Silesian5 human FC index alias witnesses.

Frozen E002_584_FROZEN.md before source replay. Point-index perturbation only:
NOT a shutter, eyelid-velocity, fatigue or physiological validation.
No human images, names, raw annotation rows, or landmarks are emitted.
"""
import bisect
import collections
import hashlib
import json
import sys

from e002_582_source_probe import retrieve
from e002_582_silesian5_fc import parse_archive, retained_indices
from e002_583_binocular_alias import candidate_runs, analyze as prior_analyze

EXPECTED = {
    "both": {"eligible": 279, "nominal": 105, "j1": 4, "j2": 0},
    "either": {"eligible": 288, "nominal": 97, "j1": 3, "j2": 0},
}
RADII = (0, 1, 2)


def intersects_sorted(sorted_indices, lo, hi):
    if lo > hi:
        return False
    i = bisect.bisect_left(sorted_indices, lo)
    return i < len(sorted_indices) and sorted_indices[i] <= hi


def classify(kept, a, b, j):
    """Return robust-miss and permissive possible-miss, not physical outcomes."""
    if j < 0 or a > b:
        raise ValueError("INVALID_INTERVAL_OR_JITTER")
    robust = not intersects_sorted(kept, a-j, b+j)
    possible = not intersects_sorted(kept, a+j, b-j)
    if robust and not possible:
        raise AssertionError("CERTIFICATE_ORDER_VIOLATION")
    return robust, possible


def eligible_intervals(rows, kind):
    if not rows or any(rows[i+1][0] <= rows[i][0] for i in range(len(rows)-1)):
        raise ValueError("BAD_SOURCE_INDICES")
    first, last = rows[0][0], rows[-1][0]
    intervals = []
    abst = collections.Counter()
    for i, k in candidate_runs(rows, kind):
        if i == 0 or k == len(rows)-1 or rows[i][0] < first+10 or rows[k][0] > last-10:
            abst["boundary"] += 1
            continue
        seg = rows[i-1:k+2]
        if any(seg[t+1][0] != seg[t][0]+1 for t in range(len(seg)-1)):
            abst["missing_index"] += 1
            continue
        if any(r[1] == "N" or r[3] == "N" or r[5] == "N" for r in seg):
            abst["nuisance"] += 1
            continue
        intervals.append((rows[i][0], rows[k][0]))
    return intervals, abst


def sequence_result(rows, kind):
    first, last = rows[0][0], rows[-1][0]
    kept = [sorted(retained_indices(first, last, p)) for p in range(10)]
    intervals, abst = eligible_intervals(rows, kind)
    robust = {str(j): [0]*10 for j in RADII}
    possible = {str(j): [0]*10 for j in RADII}
    lens = collections.Counter()
    for a,b in intervals:
        lens[str(min(4, b-a+1))] += 1
        for phase in range(10):
            for j in RADII:
                rm, pm = classify(kept[phase], a, b, j)
                robust[str(j)][phase] += int(rm)
                possible[str(j)][phase] += int(pm)
    for phase in range(10):
        for j in RADII:
            if robust[str(j)][phase] > possible[str(j)][phase]:
                raise AssertionError("ROBUST_GT_POSSIBLE")
        if robust["0"][phase] != possible["0"][phase]:
            raise AssertionError("ZERO_JITTER_NOT_IDENTICAL")
        if not (robust["2"][phase] <= robust["1"][phase] <= robust["0"][phase]):
            raise AssertionError("ROBUST_NONMONOTONIC")
        if not (possible["0"][phase] <= possible["1"][phase] <= possible["2"][phase]):
            raise AssertionError("POSSIBLE_NONMONOTONIC")
    return {"eligible":len(intervals), "abstain":dict(abst), "lengths":dict(lens),
            "robust":robust, "possible":possible, "rows":len(rows)}


def analyze(sequences, source_sha):
    prior = prior_analyze(sequences, source_sha)
    result = {
        "experiment":"E002-584",
        "evidence_tier":"HUMAN_INVESTIGATOR_FC_INDEX_TIMING_SENSITIVITY_ONLY",
        "source_archive_sha256":source_sha,
        "nominal_source_fps":100,
        "nominal_target_fps":30,
        "jitter_radii_native_frames":list(RADII),
        "physical_shutter_verified":False,
        "continuous_human_velocity_bound_verified":False,
        "independent_anatomical_rater_pair":False,
        "heldout_physical_predictions":False,
        "product":"ABSTAIN_UNCALIBRATED",
        "release":"BLOCKED",
        "source_sequences":len(sequences),
        "source_rows":sum(map(len,sequences)),
    }
    for kind in ("both","either"):
        pieces = [sequence_result(rows,kind) for rows in sequences]
        sums = lambda key,j: [sum(p[key][str(j)][ph] for p in pieces) for ph in range(10)]
        robust = {str(j):sums("robust",j) for j in RADII}
        possible = {str(j):sums("possible",j) for j in RADII}
        eligible = sum(p["eligible"] for p in pieces)
        baseline = sum(robust["0"])
        if eligible != EXPECTED[kind]["eligible"] or baseline != EXPECTED[kind]["nominal"]:
            raise ValueError("E002_583_BASELINE_REPLAY_MISMATCH")
        if baseline != sum(prior[kind]["omitted_by_phase"]):
            raise ValueError("INDEPENDENT_PRIOR_BASELINE_MISMATCH")
        for j in (1,2):
            if sum(robust[str(j)]) != EXPECTED[kind]["j"+str(j)]:
                raise ValueError("FROZEN_JITTER_PREDICTION_FALSIFIED")
        abst = collections.Counter()
        for p in pieces:
            abst.update(p["abstain"])
        result[kind] = {
            "eligible_runs":eligible,
            "abstentions":dict(sorted(abst.items())),
            "robust_missed_by_phase":robust,
            "possible_missed_by_phase":possible,
            "robust_event_phase_totals":{str(j):sum(robust[str(j)]) for j in RADII},
            "possible_event_phase_totals":{str(j):sum(possible[str(j)]) for j in RADII},
            "nominal_witnesses_losing_j1_guarantee":baseline-sum(robust["1"]),
            "nominal_witness_loss_fraction_j1":(baseline-sum(robust["1"]))/baseline,
            "anonymized_sequence_counts":sorted(
                [{"rows":p["rows"],"eligible":p["eligible"],
                  "nominal_omissions":sum(p["robust"]["0"]),
                  "j1_robust_omissions":sum(p["robust"]["1"])} for p in pieces],
                key=lambda x:x["rows"]),
        }
    return result


def fixtures():
    def make(n=90, l=(), r=(), missing=None, nuisance=None):
        l,r=set(l),set(r)
        return [(i, "N" if i==nuisance else "X",
                 "C" if i in l else "X","X",
                 "C" if i in r else "X","X")
                for i in range(n) if i != missing]
    a=make(l=[35],r=[35])
    z=sequence_result(a,"both")
    assert z["eligible"]==1 and sum(z["robust"]["0"])==7
    assert sum(z["robust"]["1"])==1 and sum(z["robust"]["2"])==0
    assert z["robust"]["0"]==z["possible"]["0"]
    assert sum(z["possible"]["1"])==10
    b=make(l=[35,36],r=[35,36])
    z=sequence_result(b,"both")
    assert sum(z["robust"]["0"])==4 and sum(z["robust"]["1"])==0
    c=make(l=range(35,45),r=range(35,45))
    z=sequence_result(c,"both")
    assert sum(z["robust"]["0"])==0
    assert sum(z["possible"]["1"])==0
    assert sequence_result(make(l=[35],r=[35],missing=34),"both")["abstain"]["missing_index"]==1
    assert sequence_result(make(l=[35],r=[35],nuisance=35),"both")["abstain"]["nuisance"]==1
    assert sequence_result(make(l=[1],r=[1]),"both")["abstain"]["boundary"]==1
    assert sequence_result(make(l=[35],r=[40]),"both")["eligible"]==0
    try:
        classify([1,4],4,3,1)
    except ValueError:
        pass
    else:
        raise AssertionError("INVALID_INTERVAL_ACCEPTED")
    for j in RADII:
        assert classify([30,33,36,40],38,38,j)[0] <= classify([30,33,36,40],38,38,j)[1]
    print(json.dumps({"experiment":"E002-584","fixtures":"PASS","fixture_groups":10},sort_keys=True))


if __name__=="__main__":
    fixtures()
    if "--source" in sys.argv:
        raw=retrieve()
        print(json.dumps(analyze(parse_archive(raw),hashlib.sha256(raw).hexdigest()),sort_keys=True))
