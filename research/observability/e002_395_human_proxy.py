#!/usr/bin/env python3
"""E002-395 frozen one-person human video / EEG event association. NOT physical aperture."""
import argparse
import bisect
import csv
import hashlib
import io
import json
import math
import pathlib
import random
import tempfile
import zipfile

import cv2
import numpy as np

MD5 = "fef02cb7ebf62e4f3efb6303284fd6cb"
EXCLUDED = {758, 1249, 1667, 2610, 3284, 4045}
OFFSETS = (0.55, -0.55, 0.75, -0.75, 1.05, -1.05)
VARIANTS = ("clean", "gain_070", "gain_130", "offset_plus25", "offset_minus25",
            "blur_sigma2", "glare", "translation_8_6")

def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()

def num(raw):
    try:
        v = float(raw)
        return v if math.isfinite(v) else None
    except (ValueError, TypeError):
        return None

def auc(pos, neg):
    p, n = np.asarray(pos, dtype=float), np.asarray(neg, dtype=float)
    if not len(p) or not len(n):
        return None
    return float(((p[:, None] > n[None, :]).sum() +
                  .5 * (p[:, None] == n[None, :]).sum()) / (len(p)*len(n)))

def threshold_fit(pos, neg):
    all_scores = sorted(set(float(x) for x in list(pos)+list(neg)))
    candidates = all_scores + [max(all_scores) + 1e-9]
    def youden(thr):
        return sum(x >= thr for x in pos)/len(pos) - sum(x >= thr for x in neg)/len(neg)
    return float(max(candidates, key=lambda thr: (youden(thr), thr)))

def binary_stats(pos, neg, thr):
    return {"sensitivity": float(sum(x >= thr for x in pos)/len(pos)),
            "specificity": float(sum(x < thr for x in neg)/len(neg)),
            "false_positive_controls": int(sum(x >= thr for x in neg)),
            "missed_eeg_marker_windows": int(sum(x < thr for x in pos))}

def transform(gray, name):
    if name == "clean":
        return gray
    if name == "gain_070":
        return np.clip(gray.astype(np.float32)*.7, 0, 255).astype(np.uint8)
    if name == "gain_130":
        return np.clip(gray.astype(np.float32)*1.3, 0, 255).astype(np.uint8)
    if name == "offset_plus25":
        return np.clip(gray.astype(np.int16)+25, 0, 255).astype(np.uint8)
    if name == "offset_minus25":
        return np.clip(gray.astype(np.int16)-25, 0, 255).astype(np.uint8)
    if name == "blur_sigma2":
        return cv2.GaussianBlur(gray, (7,7), 2.0)
    if name == "glare":
        g = gray.copy()
        g[145:175,130:205] = 255
        return g
    if name == "translation_8_6":
        return cv2.warpAffine(gray, np.float32([[1,0,8],[0,1,6]]),
                              (gray.shape[1], gray.shape[0]),
                              borderMode=cv2.BORDER_REPLICATE)
    raise ValueError(name)

def proxy(gray):
    eye = gray[118:190,100:230]
    skin = gray[125:200,45:85]
    if eye.shape != (72,130) or skin.shape != (75,40):
        raise RuntimeError("Unexpected camera dimensions")
    baseline = float(np.median(skin))
    threshold = baseline - max(20., .25*baseline)
    dark_fraction = float(np.mean(eye < threshold))
    clipping = float(np.mean((eye == 0) | (eye == 255)))
    return 1.0-dark_fraction, clipping

def load_sync(z):
    names = [n for n in z.namelist() if n.endswith("_sync.csv")]
    if len(names) != 1:
        raise RuntimeError("Expected one sync CSV")
    frames, markers = [], []
    with z.open(names[0]) as f:
        rows = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig"))
        if not {"Time", "PhanFrame", "Blinks"}.issubset(rows.fieldnames or []):
            raise RuntimeError("Missing sync columns")
        for row in rows:
            t, fid, blink = num(row.get("Time")), num(row.get("PhanFrame")), num(row.get("Blinks"))
            if t is None:
                continue
            if fid is not None:
                frames.append((int(fid), t))
            if blink is not None and blink > 0:
                markers.append(t)
    if len(frames) != 53680 or len(markers) != 112:
        raise RuntimeError("Unexpected source dimensions or event count")
    if any(b[0]-a[0] != 1 or b[1] <= a[1] for a,b in zip(frames, frames[1:])):
        raise RuntimeError("Noncontiguous frame IDs or nonmonotonic EEG clock")
    return frames, markers

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    if md5(args.archive) != MD5:
        raise RuntimeError("Source MD5 mismatch")
    out = pathlib.Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.archive) as z:
        frames, markers = load_sync(z)
        times = [t for _,t in frames]
        ids = [fid for fid,_ in frames]
        def near(t):
            j = bisect.bisect_left(times, t)
            candidates = [k for k in (j-1,j) if 3 <= k < len(times)-3]
            if not candidates:
                return None
            k = min(candidates, key=lambda k: abs(times[k]-t))
            if abs(times[k]-t) > .0100001:
                return None
            if any(times[q+1]-times[q] > .0200001 for q in range(k-3,k+3)):
                return None
            return k
        pairs = []
        rejected = {"uncovered_or_gap":0, "exploratory_six":0, "no_clean_control":0}
        for t in markers:
            k = near(t)
            if k is None:
                rejected["uncovered_or_gap"] += 1
                continue
            if ids[k] in EXCLUDED:
                rejected["exploratory_six"] += 1
                continue
            ctrl = None
            for delta in OFFSETS:
                candidate = t+delta
                if min(abs(candidate-m) for m in markers) < .35:
                    continue
                j = near(candidate)
                if j is not None and abs(j-k) > 6:
                    ctrl = j
                    break
            if ctrl is None:
                rejected["no_clean_control"] += 1
                continue
            pairs.append((k,ctrl))
        if len(pairs) < 50:
            raise RuntimeError("Insufficient predeclared paired windows")
        train_n = int(len(pairs)*.60)
        if len(pairs)-train_n < 20:
            raise RuntimeError("Underpowered holdout")
        selected = set()
        for k,j in pairs:
            selected.update(range(k-3,k+4))
            selected.update(range(j-3,j+4))
        video_names = [n for n in z.namelist() if n.lower().endswith("_phantom.avi")]
        if len(video_names) != 1:
            raise RuntimeError("Expected one Phantom video")
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp)/"source.avi"
            with z.open(video_names[0]) as src, open(path,"wb") as dst:
                for block in iter(lambda:src.read(1 << 20), b""):
                    dst.write(block)
            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened() or int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) != len(frames):
                raise RuntimeError("Video decode/frame-count mismatch")
            scores = {}
            i = 0
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                if i in selected:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    scores[i] = {v: proxy(transform(gray,v)) for v in VARIANTS}
                i += 1
            cap.release()
        if i != len(frames) or len(scores) != len(selected):
            raise RuntimeError("Incomplete video decode")
    anonymous = []
    for k,j in pairs:
        rec = {}
        for variant in VARIANTS:
            rec[variant] = {
                "positive": max(scores[q][variant][0] for q in range(k-3,k+4)),
                "control": max(scores[q][variant][0] for q in range(j-3,j+4)),
                "clip_positive_max": max(scores[q][variant][1] for q in range(k-3,k+4)),
                "clip_control_max": max(scores[q][variant][1] for q in range(j-3,j+4))
            }
        anonymous.append(rec)
    train = anonymous[:train_n]
    test = anonymous[train_n:]
    threshold = threshold_fit([p["clean"]["positive"] for p in train],
                              [p["clean"]["control"] for p in train])
    result_variants = {}
    for variant in VARIANTS:
        p = [r[variant]["positive"] for r in test]
        n = [r[variant]["control"] for r in test]
        result_variants[variant] = {"auc": auc(p,n), **binary_stats(p,n,threshold),
            "mean_max_clipped_fraction":float(np.mean([max(r[variant]["clip_positive_max"],
                                                          r[variant]["clip_control_max"]) for r in test]))}
    rng = random.Random(371)
    pos = [r["clean"]["positive"] for r in test]
    neg = [r["clean"]["control"] for r in test]
    boot = []
    for _ in range(1000):
        pick = [rng.randrange(len(test)) for _ in test]
        boot.append(auc([pos[q] for q in pick],[neg[q] for q in pick]))
    labels = [1]*len(pos)+[0]*len(neg)
    rng.shuffle(labels)
    combined = pos+neg
    null_auc = auc([s for s,l in zip(combined,labels) if l],
                   [s for s,l in zip(combined,labels) if not l])
    clean_auc = result_variants["clean"]["auc"]
    gain_ok = all(clean_auc-result_variants[v]["auc"] <= .08
                  for v in ("gain_070","gain_130","offset_plus25","offset_minus25"))
    result = {"experiment":"E002-395", "source_verified":True, "source_md5":MD5,
              "human_participants":1, "frames":len(frames), "eeg_markers":len(markers),
              "pairs":len(pairs), "train_pairs":len(train), "heldout_pairs":len(test),
              "excluded_previously_inspected_phantom_ids":sorted(EXCLUDED),
              "rejected":rejected, "fixed_feature":"1 - skin-normalized eye dark-pixel fraction",
              "threshold_fit_on_training_only":threshold,
              "variants":result_variants,
              "auc_bootstrap_95_interval":[float(np.percentile(boot,2.5)),float(np.percentile(boot,97.5))],
              "shuffled_label_auc":null_auc,
              "frozen_primary_auc_ge_075":clean_auc >= .75,
              "frozen_brightness_auc_drop_le_008":gain_ok,
              "frozen_null_abs_deviation_le_015":abs(null_auc-.5) <= .15,
              "physical_aperture_validated":False, "actual_exposure_known":False,
              "independent_velocity_bound":False,
              "product_decision":"ABSTAIN_UNCALIBRATED",
              "evidence_tier":"single-person EEG-marker-associated image surrogate; no physical blink labels"}
    (out/"e002_395_result.json").write_text(json.dumps(result,indent=2))
    (out/"e002_395_anonymous_scores.json").write_text(json.dumps({
        "train_n":train_n,"train":train,"test":test},separators=(",",":")))
    print(json.dumps({"pairs":len(pairs),"train":len(train),"test":len(test),
                      "auc":clean_auc,"auc_ci":result["auc_bootstrap_95_interval"],
                      "variants":{k:round(v["auc"],4) for k,v in result_variants.items()},
                      "frozen_primary_passed":result["frozen_primary_auc_ge_075"],
                      "brightness_passed":gain_ok,
                      "null_auc":null_auc,
                      "product":result["product_decision"]},indent=2))

if __name__ == "__main__":
    main()
