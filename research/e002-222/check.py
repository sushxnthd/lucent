import json,hashlib
from pathlib import Path
x=json.loads(Path("research/e002-222/RESULTS.json").read_text())
assert x["run"]=="E002-222"
assert len(x["participants"])==2
for p,v in x["participants"].items():
 for kind,h in v["sha256"].items():
  assert hashlib.sha256(Path("/tmp/"+p+"_"+kind).read_bytes()).hexdigest()==h
 for typ in ("packet_pts","decoded_frame_pts"):
  assert 0<=v[typ]["distinct"]<=v[typ]["n"]
 assert v["exposure_sync_certified"] is False
 assert v["native_rgb_pupil_waveform_tested"] is False
print("Independent pinned-source and timing schema checker passed")
