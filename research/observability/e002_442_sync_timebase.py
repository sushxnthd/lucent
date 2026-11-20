#!/usr/bin/env python3
"""E002-442: preregistered S19 synchronization-clock candidate audit.
Only relative timing aggregates leave the process; exposure timing is NOT authenticated.
"""
import argparse, csv, hashlib, io, json, math, statistics, tempfile, zipfile
from pathlib import Path

SOURCES = {"S19": ("8a16cf12526f7558b4e49926c4bc5e8e", 373146176)}
COLUMNS = ("Time", "PhanTime", "RelTime", "RecordingTimestamp", "LocalTimeStamp")
UNITS = {"seconds": 1.0, "milliseconds": 1e-3, "microseconds": 1e-6, "nanoseconds": 1e-9}
VIDEO_FRAMES = 56911  # independently probed on hash-verified S19 in E002-441
NATIVE_FPS_HYPOTHESIS = 500.0  # publication description, NOT measured sensor clock

def percentile(values, q):
    if not values: return None
    s = sorted(values)
    k = (len(s)-1)*q
    lo, hi = math.floor(k), math.ceil(k)
    return s[lo]*(hi-k)+s[hi]*(k-lo) if lo != hi else s[lo]

def _num(s):
    try:
        v = float(s)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError, OverflowError):
        return None

def summarize_column(values, video_frames=VIDEO_FRAMES):
    if not isinstance(values, list) or video_frames <= 0: raise ValueError("invalid inputs")
    parsed = [_num(v) for v in values]
    steps = [b-a for a,b in zip(parsed,parsed[1:]) if a is not None and b is not None]
    positive = [v for v in steps if v > 0]
    nonpositive = sum(v <= 0 for v in steps)
    valid = sum(v is not None for v in parsed)
    raw_span = parsed[-1]-parsed[0] if len(parsed)>1 and parsed[0] is not None and parsed[-1] is not None else None
    unit_results = {}
    for unit,scale in UNITS.items():
        near = sum(.0016 <= d*scale <= .0024 for d in steps)
        frac = near/len(steps) if steps else 0.0
        span = raw_span*scale if raw_span is not None else None
        expected = (video_frames-1)/NATIVE_FPS_HYPOTHESIS
        span_ok = span is not None and abs(span-expected) <= .05*expected
        unit_results[unit] = {
            "median_positive_delta_s": statistics.median(positive)*scale if positive else None,
            "p01_positive_delta_s": percentile(positive,.01)*scale if positive else None,
            "p99_positive_delta_s": percentile(positive,.99)*scale if positive else None,
            "relative_span_s": span, "fraction_2ms_compatible": frac,
            "candidate_frame_clock": bool(len(steps)>=1000 and len(values)==video_frames
                and nonpositive==0 and frac>=.95 and span_ok and valid==len(values))
        }
    return {"row_count":len(values),"numeric_count":valid,"unparseable_count":len(values)-valid,
        "adjacent_numeric_step_count":len(steps),"nonpositive_step_count":nonpositive,
        "positive_step_count":len(positive),"row_count_equals_video_frames":len(values)==video_frames,
        "units":unit_results}

def analyze_zip(path, video_frames=VIDEO_FRAMES, verify=True):
    path = Path(path)
    expected,size = SOURCES["S19"]
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1048576),b""): h.update(chunk)
    if verify and (h.hexdigest()!=expected or path.stat().st_size!=size):
        raise ValueError("S19 archive failed published MD5/size verification")
    with zipfile.ZipFile(path) as z:
        members = [x for x in z.infolist() if x.filename.lower().endswith("_sync.csv") and not x.is_dir()]
        if len(members)!=1: raise ValueError("Expected exactly one S19 sync CSV")
        m = members[0]
        if Path(m.filename).is_absolute() or ".." in Path(m.filename).parts:
            raise ValueError("unsafe ZIP member path")
        with z.open(m) as f:
            reader = csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig",errors="replace",newline=""))
            if not reader.fieldnames or not set(COLUMNS).issubset(reader.fieldnames):
                raise ValueError("S19 sync columns missing")
            cols = {k:[] for k in COLUMNS}
            for row in reader:
                for k in COLUMNS: cols[k].append(row.get(k))
    results = {k:summarize_column(v,video_frames) for k,v in cols.items()}
    candidates = [{"column":k,"unit":u} for k,v in results.items()
                  for u,stat in v["units"].items() if stat["candidate_frame_clock"]]
    return {"experiment":"E002-442","source":"S19 Zenodo 18978288",
        "published_archive_md5_verified":h.hexdigest()==expected and path.stat().st_size==size,
        "video_frame_count_prior_probe":video_frames,"avi_container_fps_prior_probe":"1/1",
        "dataset_nominal_acquisition_fps":500,
        "sync_column_summaries":results,"candidate_frame_clocks":candidates,
        "row_to_frame_alignment_authenticated":False,
        "camera_exposure_clock_authenticated":False,
        "anatomical_aperture_reference_available":False,
        "physiological_velocity_upper_bound_validated":False,
        "e002_371_physical_validation":"FAIL",
        "physical_release_authorized":False,"product_claim":"ABSTAIN_UNCALIBRATED"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zip",type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--fixture",action="store_true")
    a = p.parse_args()
    with tempfile.TemporaryDirectory() as td:
        z = a.zip or Path(td)/"S19.zip"
        if a.zip is None:
            from e002_441_human_acquisition import download
            download("S19",z)
        result = analyze_zip(z,verify=not a.fixture)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"experiment":"E002-442",
        "sync_rows":result["sync_column_summaries"]["PhanTime"]["row_count"],
        "candidate_frame_clocks":result["candidate_frame_clocks"],"physical_validation":"FAIL"}))

if __name__=="__main__": main()
