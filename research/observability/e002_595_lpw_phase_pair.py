#!/usr/bin/env python3
"""E002-595: source-bound 95->30 fps paired rater packets. No human labels."""
import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

import e002_575_lpw_packet as packet
import e002_577_lpw_range_probe as source
import e002_578_real_lpw_packet as base

WINDOW = 19
PHASES = 3

def phase_indices(p):
    """Exact nearest-frame point decimation; NOT physical shutter integration."""
    if type(p) is not int or p not in range(PHASES):
        raise ValueError("INVALID_PHASE")
    indices = []
    for k in range(WINDOW):
        n = 30*p + 95*k
        i = (2*n+30)//60
        if i >= WINDOW:
            break
        indices.append(i)
    assert len(indices) == 6 and len(set(indices)) == 6
    return indices

def missed_pulses(indices, width):
    if type(width) is not int or not 1 <= width <= WINDOW:
        raise ValueError("INVALID_WIDTH")
    return sum(not any(start <= i < start+width for i in indices)
               for start in range(WINDOW-width+1))

def law():
    grids = [phase_indices(p) for p in range(PHASES)]
    union = sorted(set().union(*map(set, grids)))
    return {
        "phase_native_indices": grids,
        "union_native_indices": union,
        "all_phase_unobserved_indices": sorted(set(range(WINDOW))-set(union)),
        "missed_discrete_pulses_by_width": {
            str(w): [missed_pulses(g,w) for g in grids] for w in (1,2,3,4)
        }
    }

def self_test():
    x = law()
    assert x["phase_native_indices"] == [
        [0,3,6,10,13,16], [1,4,7,11,14,17], [2,5,8,12,15,18]]
    assert x["all_phase_unobserved_indices"] == [9]
    assert x["missed_discrete_pulses_by_width"] == {
        "1":[13,13,13], "2":[7,6,7], "3":[1,1,1], "4":[0,0,0]}
    for bad in (-1,3,0.5,None,"1",True):
        try: phase_indices(bad)
        except ValueError: pass
        else: raise AssertionError("BAD_PHASE_ACCEPTED")
    for bad in (-1,0,20,0.5,True):
        try: missed_pulses(phase_indices(0),bad)
        except ValueError: pass
        else: raise AssertionError("BAD_WIDTH_ACCEPTED")
    owner, a, b, candidates = base.make_plan()
    assert len(owner["owner_mapping"]) == 10 and candidates == 105
    assert all(len(g)==6 for g in x["phase_native_indices"])
    print(json.dumps({"experiment":"E002-595","self_test":"PASS",
                      "evidence_tier":"SYNTHETIC_INDEX_ONLY",
                      "phase_index_law":x,"anatomical_labels":0,
                      "product":"ABSTAIN_UNCALIBRATED"},sort_keys=True))

def build_arms(root, owner):
    counts={}
    for r in ("A","B"):
        for p in range(PHASES):
            arm=root/f"RATER_{r}"/f"ARM_{p}"
            grid=phase_indices(p)
            blank={}
            for row in owner["owner_mapping"]:
                clip=row["blind_clip"]
                dst=arm/"clips"/clip
                dst.mkdir(parents=True,exist_ok=False)
                blank[clip]=[]
                for k,i in enumerate(grid):
                    src=root/f"RATER_{r}"/"clips"/clip/f"frame_{i:02d}.png"
                    target=dst/f"frame_{k:02d}.png"
                    shutil.copyfile(src,target)
                    if (not src.is_file() or target.is_symlink() or
                            packet.sha256(src)!=packet.sha256(target) or
                            packet.png_dimensions(target)!=(640,480)):
                        raise RuntimeError("PHASE_SOURCE_BINDING_FAILED")
                    blank[clip].append({
                        "frame":k,"upper_y":None,"lower_y":None,
                        "iris_diameter":None,"uncertainty_px":None,
                        "flags":["UNREVIEWED"]})
            template={"experiment":"E002-595","rater":r,
                      "arm":f"ARM_{p}","clips":blank}
            encoded=json.dumps(template,sort_keys=True)
            if any(s in encoded for s in (
                    "participant_id","video_sha256","start_native_frame",
                    "native_offset","owner_mapping")):
                raise RuntimeError("REVIEWER_BLINDING_FAILURE")
            (arm/"BLANK_ANATOMICAL_RATINGS.json").write_text(encoded)
            counts[f"{r}_{p}"]=sum(map(len,blank.values()))
    if set(counts.values())!={60} or len(counts)!=6:
        raise RuntimeError("INCOMPLETE_PHASE_PACKET")
    return counts

def execute():
    owner,a,b,_=base.make_plan()
    total=source.remote_size(source.URL)
    get=source.remote_getter(source.URL,total)
    entry,eligible=source.archive_entries(total,get)
    if entry["name"]!=base.VIDEO or eligible!=66:
        raise RuntimeError("SOURCE_MEMBER_MISMATCH")
    data=source.extract_member(total,get,entry)
    if hashlib.sha256(data).hexdigest()!=base.VIDEO_SHA:
        raise RuntimeError("SOURCE_SHA_MISMATCH")
    with tempfile.TemporaryDirectory(prefix="lucent-e002-595-private-") as tmp:
        folder=Path(tmp)
        video=folder/"source.avi"
        video.write_bytes(data)
        del data
        base.probe_stream(video)
        sources={"videos":[{
            "participant_id":"1","video_id":"1",
            "video_sha256":base.VIDEO_SHA,
            "native_frame_count":base.NATIVE_FRAMES,
            "absolute_path":str(video)}]}
        root=folder/"private_review_packets"
        packet.build_packet(owner,sources,a,b,root)
        if base.verify_packet(root,owner,a,b)!=190:
            raise RuntimeError("NATIVE_PACKET_FAILED")
        counts=build_arms(root,owner)
        if packet.sha256(video)!=base.VIDEO_SHA:
            raise RuntimeError("SOURCE_MUTATED")
    return {
        "experiment":"E002-595",
        "status":"REAL_HUMAN_SOURCE_PHASE_PACKET_VERIFIED",
        "evidence_tier":"REAL_HUMAN_SOURCE_INSTRUMENT_ONLY",
        "source_sha256":base.VIDEO_SHA,
        "reported_native_fps":95,"nominal_point_sample_fps":30,
        "development_windows":10,
        "native_frames_per_reviewer":190,
        "phase_frames_per_reviewer":sum(v for k,v in counts.items()
                                         if k.startswith("A_")),
        "six_phase_arms_source_hash_verified":True,
        "private_packets_retained":False,
        "independent_human_raters":0,"anatomical_labels":0,
        "physical_shutter_calibrated":False,
        "continuous_velocity_ceiling_certified":False,
        "held_out_physical_predictions":0,
        "product":"ABSTAIN_UNCALIBRATED","release":"BLOCKED",
        "phase_index_only":law()
    }

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:
        self_test()
    else:
        print(json.dumps(execute(), sort_keys=True))
