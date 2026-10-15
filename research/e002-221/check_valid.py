import json
from pathlib import Path
root=Path("research/e002-221")
a=json.loads((root/"RESULTS.json").read_text())
b=json.loads((root/"VALID_ONLY.json").read_text())
assert set(a["participants"])==set(b["participants"])
for p in a["participants"]:
 raw=a["participants"][p]
 derived=b["participants"][p]
 for eye in ("left","right"):
  counts=derived["validity_cross_tab"][eye]
  assert sum(counts.values())==raw["tracker_rows"]+raw["tracker_unparsed"] or sum(counts.values())==raw["tracker_rows"]
  sample=derived["eyes"][eye]
  assert sample["valid_samples_window"]<=raw["reference_window"]["count"]
  for v in sample["offsets"].values():
   assert 0<=v["valid_reference_within_75ms"]<=raw["video_window_packets"]
   assert abs(v["coverage"]-v["valid_reference_within_75ms"]/raw["video_window_packets"])<1e-5
print("E002-221 valid-only cross-check passed")
