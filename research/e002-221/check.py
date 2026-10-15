import json
from pathlib import Path
r=json.loads(Path("research/e002-221/RESULTS.json").read_text())
assert set(r["participants"])=={"P_33","P_54"}
for k,x in r["participants"].items():
 n=x["video_window_packets"];u=x["video_window_unique"]
 assert n>0 and 0<=u<=n
 assert abs(x["video_window_unique_fraction"]-u/n)<1e-5
 assert x["exposure_sync_certified"] is False
 if x["reference_window"] is not None:
  a=x["reference_window"]
  assert 0<=a["left_valid"]<=a["count"]
  assert 0<=a["right_valid"]<=a["count"]
  for z in x["offset_sensitivity"].values():
   assert z["near"]<=n
print("independent count consistency: PASS")
