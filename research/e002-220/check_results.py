import json,copy
from pathlib import Path
r=json.loads(Path("research/e002-220/EVIDENCE.json").read_text())
def check(a):
 for p in ("P_33","P_54"):
  x=a[p];q=x["unique_pts"]/x["packets"]
  assert abs(q-x["fraction"])<1e-12
  assert x["gate"]==("PASS" if q>=a["frozen_unique_pts_gate"] else "FAIL")
check(r)
bad=copy.deepcopy(r);bad["P_54"]["fraction"]=0.99
try:check(bad)
except AssertionError:pass
else:raise AssertionError("mutation escaped")
print("Independent arithmetic and mutation checks PASS")
# E002-262 isolated research branch only: original E002-220 workflow remains unchanged.
import subprocess,sys
subprocess.run([sys.executable,"research/e002-262/event_anchor.py"],check=True)
