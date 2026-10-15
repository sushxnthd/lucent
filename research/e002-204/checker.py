import json
from pathlib import Path
p=Path(__file__).resolve().parent/"results/NATIVE_WINDOW.json"
assert p.exists(),"MISSING_NATIVE_TIME_HUMAN_RESULT"
r=json.loads(p.read_text())
assert not r["errors"] and len(r["people"])==15,"EMPTY_OR_INCOMPLETE_HUMAN"
assert len({x["sha256"] for x in r["people"].values()})==15
for x in r["people"].values():
 assert x["n"]>=600
 for e in x["eyes"].values():
  assert 0<=e["window_valid"]<=e["window_n"]<=x["n"]
  assert 0<=e["pupil_valid"]<=x["n"] and 0<=e["positive_pupil"]<=e["pupil_valid"]
  assert e["pass"]==(e["window_n"]>=570 and e["window_valid"]>=570 and e["window_valid"]/e["window_n"]>=.95 and e["max_gap"] is not None and e["max_gap"]<=.026)
assert r["rgb_waveform"]=="NOT_TESTED"
print("PASS 15 original-human native-time reference checks; RGB NOT TESTED")
