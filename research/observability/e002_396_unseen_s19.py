#!/usr/bin/env python3
"""E002-396: frozen, unseen S19 participant transfer. No physical aperture claims."""
import argparse
import bisect
import csv
import io
import json
import pathlib
import tempfile
import zipfile
import cv2
import numpy as np

import e002_395_human_proxy as prior

MD5 = "8a16cf170a9c7e9660f6e22b81d7d0a"
FROZEN_S01_THR = 0.7938034188034189

def load(z):
    sync_suffix, avi_suffix = "_sync.csv", "_phantom.avi"
    syncs = {n[:-len(sync_suffix)]:n for n in z.namelist() if n.endswith(sync_suffix)}
    avis = {n[:-len(avi_suffix)]:n for n in z.namelist() if n.lower().endswith(avi_suffix)}
    shared = sorted(set(syncs)&set(avis))
    if not shared:
        raise RuntimeError("No paired session source")
    stem = shared[0]
    frames, markers = [], []
    with z.open(syncs[stem]) as f:
        reader = csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig"))
        if not {"Time","PhanFrame","Blinks"}.issubset(reader.fieldnames or []):
            raise RuntimeError("Missing synchronized human markers")
        for row in reader:
            t = prior.num(row.get("Time"))
            fid = prior.num(row.get("PhanFrame"))
            blink = prior.num(row.get("Blinks"))
            if t is None:
                continue
            if fid is not None:
                frames.append((int(fid),t))
            if blink is not None and blink > 0:
                markers.append(t)
    if len(frames)<1000:
        raise RuntimeError("Insufficient high-speed frames")
    if any(b[0]-a[0]!=1 or b[1]<=a[1] for a,b in zip(frames,frames[1:])):
        raise RuntimeError("Noncontiguous frame IDs or nonmonotonic EEG time")
    return stem, avis[stem], frames, markers

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    if prior.md5(a.archive)!=MD5:
        raise RuntimeError("S19 source MD5 mismatch")
    out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(a.archive) as z:
        stem,avi,frames,markers=load(z)
        times=[t for _,t in frames]
        def near(t):
            i=bisect.bisect_left(times,t)
            cand=[j for j in (i-1,i) if 3<=j<len(times)-3]
            if not cand:return None
            k=min(cand,key=lambda j:abs(times[j]-t))
            if abs(times[k]-t)>.0100001:return None
            if any(times[q+1]-times[q]>.0200001 for q in range(k-3,k+3)):
                return None
            return k
        pairs=[]
        rejected={"uncovered_or_gap":0,"no_control":0}
        for t in markers:
            k=near(t)
            if k is None:
                rejected["uncovered_or_gap"]+=1
                continue
            control=None
            for delta in prior.OFFSETS:
                tt=t+delta
                if min(abs(tt-m) for m in markers)<.35:
                    continue
                j=near(tt)
                if j is not None and abs(j-k)>6:
                    control=j;break
            if control is None:
                rejected["no_control"]+=1
                continue
            pairs.append((k,control))
        if len(pairs)<15:
            raise RuntimeError("Underpowered S19 paired marker/control windows")
        wanted=set()
        for k,j in pairs:
            wanted.update(range(k-3,k+4))
            wanted.update(range(j-3,j+4))
        with tempfile.TemporaryDirectory() as tmp:
            path=pathlib.Path(tmp)/"s19.avi"
            with z.open(avi) as src,open(path,"wb") as dst:
                for block in iter(lambda:src.read(1<<20),b""):
                    dst.write(block)
            cap=cv2.VideoCapture(str(path))
            if not cap.isOpened() or int(cap.get(cv2.CAP_PROP_FRAME_COUNT))!=len(frames):
                raise RuntimeError("Video/EEG frame count disagreement")
            scores={};i=0
            while True:
                ok,frame=cap.read()
                if not ok:break
                if i in wanted:
                    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                    scores[i]={v:prior.proxy(prior.transform(gray,v))
                               for v in prior.VARIANTS}
                i+=1
            cap.release()
        if i!=len(frames) or len(scores)!=len(wanted):
            raise RuntimeError("Video frame decode incomplete")
    anonymous=[]
    for k,j in pairs:
        row={}
        for variant in prior.VARIANTS:
            row[variant]={
                "positive":max(scores[q][variant][0] for q in range(k-3,k+4)),
                "control":max(scores[q][variant][0] for q in range(j-3,j+4)),
                "clipping":max(scores[q][variant][1] for q in
                               list(range(k-3,k+4))+list(range(j-3,j+4)))}
        anonymous.append(row)
    variants={}
    for variant in prior.VARIANTS:
        p=[r[variant]["positive"] for r in anonymous]
        n=[r[variant]["control"] for r in anonymous]
        direct=prior.auc(p,n)
        inverse=prior.auc([1-x for x in p],[1-x for x in n])
        variants[variant]={"direct_auc":direct,"inverse_auc":inverse,
            **prior.binary_stats(p,n,FROZEN_S01_THR),
            "mean_window_max_clipped_fraction":float(np.mean([r[variant]["clipping"] for r in anonymous]))}
    clean=variants["clean"]
    result={"experiment":"E002-396","source_md5":MD5,"verified":True,
            "source_record":"Zenodo 21905748 S19.zip","selected_session_stem":stem,
            "session_selection":"lexicographically first paired AVI and sync",
            "participants":1,"unseen_from_S01":True,"camera_frames":len(frames),
            "eeg_markers":len(markers),"paired_windows":len(pairs),
            "rejected":rejected,"frozen_s01_threshold":FROZEN_S01_THR,
            "variants":variants,
            "H1_inverse_auc_ge_075":clean["inverse_auc"]>=.75,
            "H2_direct_auc_below_050":clean["direct_auc"]<.5,
            "H3_frozen_threshold_specificity_le_050":clean["specificity"]<=.5,
            "human_physical_aperture":False,"exposure_calibrated":False,
            "independent_velocity":False,"product":"ABSTAIN_UNCALIBRATED",
            "evidence_tier":"unseen participant EEG-marker/image proxy association, no physical aperture"}
    (out/"e002_396_result.json").write_text(json.dumps(result,indent=2))
    (out/"e002_396_anonymous_scores.json").write_text(json.dumps(anonymous,separators=(",",":")))
    print(json.dumps({"session":stem,"frames":len(frames),"markers":len(markers),
        "pairs":len(pairs),"direct_auc":clean["direct_auc"],
        "inverse_auc":clean["inverse_auc"],
        "specificity":clean["specificity"],
        "H1":result["H1_inverse_auc_ge_075"],
        "H2":result["H2_direct_auc_below_050"],
        "H3":result["H3_frozen_threshold_specificity_le_050"],
        "product":result["product"]},indent=2))

if __name__=="__main__":
    main()
