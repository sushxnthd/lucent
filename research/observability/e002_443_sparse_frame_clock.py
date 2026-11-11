#!/usr/bin/env python3
"""E002-443: prospective sparse RelTime-event timing test on human S19 sync table.
Never infers physical shutter time, anatomical aperture or release authorization.
"""
import argparse, csv, hashlib, io, json, math, statistics, tempfile, zipfile
from pathlib import Path
from e002_442_sync_timebase import SOURCES, VIDEO_FRAMES, _num, percentile

def evaluate_events(times, frame_count=VIDEO_FRAMES):
    if not isinstance(times,list) or frame_count<2: raise ValueError("invalid event inputs")
    parsed=[_num(t) for t in times]
    if len(parsed)<2 or any(t is None for t in parsed):
        return {"event_count":len(times),"invalid_event_time_count":sum(t is None for t in parsed),
                "candidate_event_clock":False,"reason":"missing_or_nonfinite_event_time"}
    gaps=[b-a for a,b in zip(parsed,parsed[1:])]
    positives=[x for x in gaps if x>0]
    nonpositive=sum(x<=0 for x in gaps)
    within=sum(.001<=x<=.003 for x in gaps)
    long10=sum(x>.010 for x in gaps)
    long100=sum(x>.100 for x in gaps)
    burst=1;longest=1
    for gap in gaps:
        burst=burst+1 if 0<gap<=.010 else 1
        longest=max(longest,burst)
    median=statistics.median(positives) if positives else None
    pass_clock=(len(times)==frame_count and nonpositive==0 and
        within/len(gaps)>=.90 and median is not None and .0015<=median<=.0025 and longest>=100)
    return {"event_count":len(times),"video_frame_count":frame_count,
        "event_count_matches_frames":len(times)==frame_count,
        "invalid_event_time_count":0,"nonpositive_event_gap_count":nonpositive,
        "median_positive_gap_s":median,"p01_positive_gap_s":percentile(positives,.01),
        "p99_positive_gap_s":percentile(positives,.99),
        "fraction_1_to_3ms_gaps":within/len(gaps),
        "gaps_over_10ms":long10,"gaps_over_100ms":long100,
        "longest_10ms_burst_frames":longest,"event_span_s":parsed[-1]-parsed[0],
        "candidate_event_clock":pass_clock,
        "reason":"candidate_table_event_clock_only" if pass_clock else "frozen_timing_checks_failed"}

def analyze_zip(path,verify=True):
    path=Path(path);expected,size=SOURCES["S19"];h=hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1048576),b""):h.update(chunk)
    if verify and (h.hexdigest()!=expected or path.stat().st_size!=size):
        raise ValueError("S19 archive MD5/size mismatch")
    with zipfile.ZipFile(path) as z:
        members=[m for m in z.infolist() if m.filename.lower().endswith("_sync.csv") and not m.is_dir()]
        if len(members)!=1:raise ValueError("expected exactly one sync CSV")
        m=members[0]
        if Path(m.filename).is_absolute() or ".." in Path(m.filename).parts:raise ValueError("unsafe ZIP member")
        times=[];total=0
        with z.open(m) as f:
            rows=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig",errors="replace",newline=""))
            if not rows.fieldnames or not {"Time","RelTime"}.issubset(rows.fieldnames):raise ValueError("missing sync columns")
            for row in rows:
                total+=1
                if _num(row.get("RelTime")) is not None:times.append(row.get("Time"))
    result=evaluate_events(times)
    return {"experiment":"E002-443","archive_md5_verified":h.hexdigest()==expected and path.stat().st_size==size,
        "sync_row_count":total,"frame_event_statistics":result,
        "row_to_video_frame_alignment_authenticated":False,
        "sensor_exposure_clock_authenticated":False,
        "physical_aperture_reference_authenticated":False,
        "e002_371_physical_validation":"FAIL",
        "physical_release_authorized":False,"product_claim":"ABSTAIN_UNCALIBRATED"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--zip",type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--fixture",action="store_true")
    a=p.parse_args()
    with tempfile.TemporaryDirectory() as td:
        z=a.zip or Path(td)/"S19.zip"
        if a.zip is None:
            from e002_441_human_acquisition import download
            download("S19",z)
        result=analyze_zip(z,verify=not a.fixture)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"experiment":"E002-443","events":result["frame_event_statistics"]["event_count"],
        "candidate_event_clock":result["frame_event_statistics"]["candidate_event_clock"],
        "physical_validation":"FAIL"}))
if __name__=="__main__":main()
