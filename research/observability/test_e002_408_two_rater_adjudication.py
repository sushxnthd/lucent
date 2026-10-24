#!/usr/bin/env python3
"""E002-408 independent synthetic fixtures: privacy, nuisance and timing gates."""
import csv
import json
import tempfile
from pathlib import Path
from e002_407_full_event_pilot import COLUMNS
from e002_408_two_rater_adjudication import adjudicate, _external_timing

def fixtures(root):
    clips = []
    for j in range(4):
        cid = f"{j+1:020x}"
        clips.append({"clip_id": cid, "frames": [
            {"frame_in_clip": i, "file": f"{cid}_{i:03d}.png",
             "sha256": "a"*64} for i in range(30)]})
    manifest = {"experiment": "E002-407", "public_linkage_present": False,
                "crop_width": 190, "crop_height": 130, "clip_count": 4,
                "frame_count": 120, "clips": clips}
    mp = root/"manifest.json"
    mp.write_text(json.dumps(manifest))
    paths = []
    for rater in ("rater-A", "rater-B"):
        p = root/f"{rater}.csv"
        with p.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            for c in clips:
                for frame in c["frames"]:
                    i = frame["frame_in_clip"]
                    row = {k: "" for k in COLUMNS}
                    row.update(clip_id=c["clip_id"], frame_in_clip=str(i), rater_id=rater)
                    for part in ("left", "center", "right"):
                        row[f"{part}_upper_x"] = "90"
                        row[f"{part}_lower_x"] = "90"
                        row[f"{part}_upper_y"] = "30"
                        row[f"{part}_lower_y"] = "52" if rater=="rater-B" else "50"
                    if c is clips[0] and i == 0 and rater == "rater-A":
                        row["glare"] = "1"
                    if c is clips[0] and i == 1 and rater == "rater-B":
                        row["unresolved"] = "1"
                    if c is clips[0] and i == 2 and rater == "rater-A":
                        row["center_lower_y"] = "20"  # physically inverted
                    writer.writerow(row)
        paths.append(p)
    return manifest, mp, paths

def reject(f):
    try:
        f()
    except (ValueError, KeyError):
        return
    raise AssertionError("Invalid evidence accepted")

def main():
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        manifest, mp, (a,b)=fixtures(root)
        out=adjudicate(mp,a,b)
        assert out["frames"]==120
        assert out["usable_pairwise_frames"]==117
        assert out["excluded_nuisance_frames"]==2
        assert out["excluded_inverted_geometry_frames"]==1
        assert out["median_abs_center_vertical_gap_disagreement_px"]==2
        assert out["decisions"]=={"ABSTAIN_UNCALIBRATED":4}
        assert out["product"]=="ABSTAIN_UNCALIBRATED"
        assert all(c["clip_id"] not in json.dumps(out) for c in manifest["clips"])
        reject(lambda: adjudicate(mp,a,a))
        truncated=root/"truncated.csv"
        truncated.write_text("\n".join(a.read_text().splitlines()[:-1])+"\n")
        reject(lambda: adjudicate(mp,truncated,b))
        spoof={"clock_kind":"EEG_sync","camera_clock_verified":True,
               "provenance":"EEG synchronisation only",
               "validity_domain":"not camera hardware","frames":[]}
        reject(lambda: _external_timing(spoof,manifest))
        camera={"clock_kind":"independent_camera_hardware",
                "camera_clock_verified":True,
                "provenance":"synthetic exact hardware clock",
                "validity_domain":"synthetic test only",
                "frames":[{"clip_id":c["clip_id"],"frame_in_clip":f["frame_in_clip"],
                           "nominal_time_s":f["frame_in_clip"]/150,
                           "exposure_s":.001,"clock_error_s":0}
                          for c in manifest["clips"] for f in c["frames"]]}
        valid=_external_timing(camera,manifest)
        assert len(valid)==120
        camera["frames"][1]["nominal_time_s"]=0
        reject(lambda: _external_timing(camera,manifest))
        camera["frames"][1]["nominal_time_s"]=1/150
        timing=root/"camera.json"
        timing.write_text(json.dumps(camera))
        partial=root/"partial.json"
        partial.write_text(json.dumps({"speed_upper":5,"threshold":.2}))
        incomplete=adjudicate(mp,a,b,timing,partial)
        assert incomplete["decisions"]=={"ABSTAIN_UNCALIBRATED":4}
        assert incomplete["physical_timing_provenance_authenticated"] is False
        print(json.dumps({"experiment":"E002-408",
                          "synthetic_fixtures_passed":True,
                          "test_frames":120,
                          "usable_frames":117,
                          "nuisance_excluded":2,
                          "geometry_excluded":1,
                          "spoofed_EEG_clock_rejected":True,
                          "incomplete_physical_calibration_abstained":True,
                          "real_human_ratings_present":False,
                          "physical_aperture_validated":False},indent=2))

if __name__=="__main__":
    main()
