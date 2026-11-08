"""E002-726: ingest actual ffprobe frame timestamps and independent reference edges.
No claimed calibration: produces an auditable alignment report, never closure certificates.
Usage: python e002_726_capture_alignment.py frames.json reference.csv
frames.json: ffprobe -show_frames -select_streams v:0 -show_entries frame=best_effort_timestamp_time,pkt_duration_time -of json capture.mp4
reference.csv: time_s,closed (0/1), from independently clocked reference.
"""
import csv,json,sys
from decimal import Decimal,InvalidOperation
def dec(x):
    d=Decimal(str(x))
    if not d.is_finite(): raise ValueError("nonfinite")
    return d
def analyze(frames,reference):
    try:
        f=[dec(x["best_effort_timestamp_time"]) for x in frames["frames"]]
        r=[(dec(x["time_s"]),str(x["closed"])) for x in reference]
    except (KeyError,InvalidOperation,ValueError,TypeError) as e:
        return {"status":"ABSTAIN_BAD_INPUT","reason":str(e)}
    if len(f)<3 or len(r)<2: return {"status":"ABSTAIN_INSUFFICIENT_SAMPLES"}
    if any(b<=a for a,b in zip(f,f[1:])):return {"status":"ABSTAIN_NONMONOTONIC_CAMERA"}
    if any(b[0]<=a[0] for a,b in zip(r,r[1:])):return {"status":"ABSTAIN_NONMONOTONIC_REFERENCE"}
    if any(x[1] not in ("0","1") for x in r):return {"status":"ABSTAIN_BAD_REFERENCE_LABEL"}
    gaps=[b-a for a,b in zip(f,f[1:])]
    edges=[str(t) for (t,v),(u,w) in zip(r,r[1:]) if v!=w]
    return {"status":"TIMELINE_PARSED_NOT_SYNCHRONIZED","camera_frames":len(f),
            "reference_samples":len(r),"camera_gap_min_s":str(min(gaps)),
            "camera_gap_max_s":str(max(gaps)),"reference_transitions_at_sample_s":edges,
            "limitations":["ffprobe timestamps are not exposure start/end",
            "independent clocks are not aligned by this script",
            "reference transitions are interval-censored between samples",
            "no shutter calibration or velocity ceiling is inferred"]}
def main():
    with open(sys.argv[1],encoding="utf-8") as fh: frames=json.load(fh)
    with open(sys.argv[2],newline="",encoding="utf-8") as fh: ref=list(csv.DictReader(fh))
    print(json.dumps(analyze(frames,ref),indent=2))
if __name__=="__main__":main()
