import json,pathlib
p=pathlib.Path("research/e002-219/RESULTS.json")
r=json.loads(p.read_text())
assert r["native_time_certified"] is False
assert len(r["sha256"])==64
assert r["rows"]>=0 and r["columns"]
print("E002-219 schema integrity gate passed; waveform gate remains CLOSED")
