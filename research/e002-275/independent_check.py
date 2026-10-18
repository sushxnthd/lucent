import json,math,sys
d=json.load(open(sys.argv[1]))
assert d["run"]=="E002-275"
assert d["deterministic_trials"]==d["interval_covered"]==2400
assert d["algebraic_endpoint_checks"]==2400
a=d["cases"]
assert a["unbounded_webcam"]["decision"]=="UNCERTIFIED"
assert a["tight_calibrated_pass"]["decision"]=="CERTIFIED_PASS"
assert a["boundary_ambiguous"]["decision"]=="INDETERMINATE"
assert a["far_lag_fail"]["decision"]=="CERTIFIED_FAIL"
for name,lag,j,e in [("tight_calibrated_pass",.02,.01,.005),("boundary_ambiguous",.06,.01,.005),("far_lag_fail",.10,.01,.005)]:
    lo,hi=a[name]["true_lag_interval_s"]
    assert math.isclose(lo,lag-j-e,abs_tol=1e-12)
    assert math.isclose(hi,lag+j+e,abs_tol=1e-12)
assert d["eligibility"]["consumer_device_holdout_certified"] is False
assert len({v["device_model"] for v in d["camera_sources"].values() if v["consumer_webcam"]})==1
print("PASS")
