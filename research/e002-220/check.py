import json,hashlib
from pathlib import Path
p=Path("research/e002-220/RESULTS.json")
r=json.loads(p.read_text())
assert r["run"]=="E002-220" and r["status"] in ("blocked","manifest_complete")
if r["status"]=="manifest_complete":
 assert len(r["subjects"])==2 and r["entries"]>0
 for x in r["subjects"]:
  assert x["id"] in ("P_33","P_54")
  assert all(y["size"]>=0 and isinstance(y["crc"],int) for y in x["candidates"])
Path("research/e002-220/DERIVED_SHA256.txt").write_text(hashlib.sha256(p.read_bytes()).hexdigest()+"\n")
print("E002-220 manifest schema PASS; waveform and lag NOT tested")
