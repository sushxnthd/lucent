"""E002-320 frozen SYNTHETIC prediction check; no human observations."""
from fractions import Fraction as F
import json
from pathlib import Path
from independent_checker import phase_minimax
p=Path(__file__).with_name("FROZEN_PREDICTION.json")
x=json.loads(p.read_text())
P=F(x["period_seconds"]);E=F(x["exposure_seconds"])
a=F(x["amplitude"]);eta=F(x["error_bound"])
critical=P-E+4*eta*E/a
assert critical==F(x["critical_duration_seconds"])
out={"holdout_kind":"synthetic_only","critical_seconds":str(critical),"cases":[]}
for k in ("A","B"):
    d=F(x["duration_"+k])
    m,s=phase_minimax(P,E,d)
    certify=a*m>2*eta*E
    assert certify==(x["decision_"+k]=="CERTIFY")
    out["cases"].append({"duration_seconds":str(d),"worst_overlap":str(m),"worst_phase":str(s),"certify":certify,"prediction_pass":True})
Path(__file__).with_name("holdout_results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
