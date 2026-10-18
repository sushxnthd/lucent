"""Freeze nine synthetic observability boundaries before downstream changes."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent
a=json.loads((p/"results.json").read_text())
b=json.loads((p/"summary.json").read_text())
assert a["kernel"]==b["kernel"]=="E002-279"
assert len(a["rows"])==len(b["rows"])==9
for x,y in zip(a["rows"],b["rows"]):
    name,lag,d,crit=y
    assert x["schedule"]==name and x["artifact_lag_s"]==lag
    assert abs(x["d_inf"]-d)<2e-6,(x,y)
    if crit is None:
        assert x["Acrit"] is None
        assert not x["separable"]
    else:
        assert abs(x["Acrit"]-crit)<1e-8
        assert x["separable"]
    assert abs(x["d_inf"]-x["dual_d_inf"])<2e-7
assert a["adversarial"]["reduced_nuisance_false_positive"]
assert not a["adversarial"]["full_nuisance_certificate"]
print("Nine frozen boundary gates and nuisance-collision adversary PASS")
