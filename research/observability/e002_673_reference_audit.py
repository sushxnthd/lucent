"""E002-673: positive-only held-out reference audit. Synthetic self-tests only."""
import json,sys
from collections import Counter,defaultdict
def audit(data):
    if data.get("protocol")!="E002-671": raise ValueError("wrong protocol")
    counts=Counter(); participants=defaultdict(set); seen=set(); failures=[]
    for r in data["records"]:
        p=r["participant"]; split=r["split"]; mode=r["modality"]; ident=(p,r["interval_id"],mode)
        if split not in ("development","test") or mode not in ("gap","exposure") or ident in seen: raise ValueError("invalid or duplicate row")
        seen.add(ident); participants[p].add(split); counts["total"]+=1
        if split!="test": continue
        counts["test"]+=1
        if r["certificate"] is not True: counts["abstained"]+=1; continue
        valid=all(r.get(k) is True for k in ("clock_calibrated","shutter_calibrated","quality_ok")) and r.get("velocity_basis")=="independent_hard_bound"
        if not valid:
            counts["invalid_certificate"]+=1; failures.append((r["interval_id"],"uncalibrated")); continue
        counts["eligible"]+=1
        if r["reference"]=="confirmed_closure":
            if r.get("rater1")==r.get("rater2")=="closure":
                counts["false_exclusions"]+=1; failures.append((r["interval_id"],"confirmed_false_exclusion"))
            else: counts["reference_disagreement"]+=1
        elif r["reference"]=="indeterminate": counts["reference_indeterminate"]+=1
        elif r["reference"]!="no_confirmed_closure": raise ValueError("unknown reference")
    if any(len(s)>1 for s in participants.values()): raise ValueError("participant leakage")
    return {"counts":dict(counts),"failures":failures,"release_blocked":True,"decision":"FAIL" if failures else "INSUFFICIENT_HUMAN_EVIDENCE"}
def selftest():
    r=dict(participant="p",split="test",interval_id="1",modality="gap",certificate=True,reference="confirmed_closure",rater1="closure",rater2="closure",clock_calibrated=True,shutter_calibrated=True,quality_ok=True,velocity_basis="independent_hard_bound")
    def check(x): return audit(dict(protocol="E002-671",records=[x]))["counts"]
    assert check(r)["false_exclusions"]==1
    assert check(dict(r,velocity_basis="finite_difference_max"))["invalid_certificate"]==1
    assert check(dict(r,reference="indeterminate"))["reference_indeterminate"]==1
    assert check(dict(r,certificate=False))["abstained"]==1
    try: audit(dict(protocol="E002-671",records=[r,dict(r,split="development",interval_id="2")]))
    except ValueError: pass
    else: raise AssertionError("split leakage")
    print("five synthetic self-tests passed")
if __name__=="__main__":
    if sys.argv[1:]==["--self-test"]: selftest()
    else:
        with open(sys.argv[1],encoding="utf8") as f: print(json.dumps(audit(json.load(f)),indent=2))
