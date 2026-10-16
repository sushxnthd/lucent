import csv,hashlib,json,statistics
from pathlib import Path
p=Path("research/e002-225")
raw=(p/"RAW_VISIBILITY.csv").read_bytes()
res=json.loads((p/"RESULTS.json").read_text())
assert hashlib.sha256(raw).hexdigest()==res["frame_csv_sha256"]
assert not res["physiological_waveform_tested"]
assert not res["physiological_lag_certified"]
assert not res["reference_paired_to_frames"]
rows=list(csv.DictReader(raw.decode().splitlines()))
def n(s):return float(s) if s else None
def med(a):return round(statistics.median(a),5) if a else None
for participant,summary in res["participants"].items():
 a=[r for r in rows if r["participant"]==participant]
 assert len(a)==2*summary["decoded_frames"]
 for eye,stats in summary["eyes"].items():
  b=[r for r in a if r["eye"]==eye]
  v=[r for r in b if n(r["iris_diameter_px"]) is not None]
  q=[r for r in v if n(r["iris_diameter_px"])>=12]
  assert abs(len(v)/len(b)-stats["landmark_fraction"])<1e-5
  assert abs(len(q)/len(b)-stats["diameter_12px_fraction"])<1e-5
  assert stats["exploratory_geometry_gate"]==(len(q)/len(b)>=.8)
  assert med([n(r["iris_diameter_px"]) for r in v])==stats["median_iris_diameter_px"]
print("Independent check passed")
