#!/usr/bin/env python3
"""E002-267 frozen five-second waveform admission. Standard library; no clock fitting."""
import csv, json, math, random, statistics, hashlib, argparse
from collections import defaultdict

G=dict(window_s=5,min_valid=.80,min_ref_sd=.10,r=.75,lag_s=.067,amp_lo=.75,
       amp_hi=1.25,nrmse=.70,nuisance_margin=.10,min_coverage=.50,min_accuracy=.75)
FIELDS="participant_id session_id split device lighting glasses t_rgb_s t_ref_s rgb_ratio reference_mm brightness geometry iris_ratio valid_ref".split()
FEATURES="rgb_ratio brightness geometry iris_ratio".split()
def avg(x):return sum(x)/len(x)
def sd(x):
    m=avg(x);return math.sqrt(avg([(z-m)**2 for z in x]))
def corr(x,y):
    if len(x)<3 or sd(x)<1e-12 or sd(y)<1e-12:return None
    return avg([(a-avg(x))*(b-avg(y)) for a,b in zip(x,y)])/(sd(x)*sd(y))
def fit(x,y):
    if sd(x)<1e-12:return 0,avg(y)
    a=corr(x,y)*sd(y)/sd(x);return a,avg(y)-a*avg(x)
def load(path):
    with open(path,newline='') as f:
        rd=csv.DictReader(f)
        if set(FIELDS)-set(rd.fieldnames or []):raise ValueError("MISSING_COLUMNS")
        rows=list(rd)
    if not rows:raise ValueError("EMPTY")
    seen=defaultdict(set)
    for r in rows:
        if r["split"] not in ("train","val","test"):raise ValueError("BAD_SPLIT")
        seen[r["participant_id"]].add(r["split"])
        for k in ("t_rgb_s","t_ref_s","rgb_ratio","reference_mm","brightness","geometry","iris_ratio"):
            r[k]=float(r[k])
            if not math.isfinite(r[k]):raise ValueError("NONFINITE")
        if r["valid_ref"] not in ("0","1"):raise ValueError("BAD_VALIDITY")
    if any(len(v)>1 for v in seen.values()):raise ValueError("PARTICIPANT_LEAKAGE")
    return rows
def admit_provenance(m,rows):
    required=dict(reference_kind="native_time_same_eye_diameter",
      synchronization="independently_verified_exposure_clock",
      rgb_modality="visible_color",reference_interpolated=False,
      participant_split_frozen=True,preoutcome_protocol="E002-261")
    for k,v in required.items():
        if m.get(k)!=v:raise ValueError("PROVENANCE_"+k)
    if not m.get("source_dataset_sha256"):raise ValueError("SOURCE_HASH_MISSING")
    if m.get("data_type") not in ("synthetic","human"):raise ValueError("DATA_TYPE_UNKNOWN")
    if m["data_type"]=="human" and len(m["source_dataset_sha256"])!=64:
        raise ValueError("SOURCE_HASH_INVALID")
    if any(abs(r["t_rgb_s"]-r["t_ref_s"])>1/60+1e-9 for r in rows if r["valid_ref"]=="1"):
        raise ValueError("TIMESTAMP_DISCREPANCY")
    if float(m["camera_fps"])<=0:raise ValueError("INVALID_FPS")
def lag(pred,ref,ts,fps):
    # Timestamp-aware; do not shift compressed valid-row indices across missing frames.
    dt=1/fps; cands=[]
    for k in range(-round(.25/dt),round(.25/dt)+1):
        x=[];y=[]
        for i,t in enumerate(ts):
            near=min(range(len(ts)),key=lambda j:abs(ts[j]-(t+k*dt)))
            if abs(ts[near]-(t+k*dt))<.4*dt:x.append(pred[i]);y.append(ref[near])
        if len(x)>=.8*len(ts):
            r=corr(x,y)
            if r is not None:cands.append((r,-abs(k),k))
    return abs(max(cands)[2])*dt if cands else None
def evaluate(rows,m):
    admit_provenance(m,rows)
    tr=[r for r in rows if r["split"]=="train" and r["valid_ref"]=="1"]
    if len(tr)<20:raise ValueError("NO_TRAIN_CALIBRATION")
    models={k:fit([r[k] for r in tr],[r["reference_mm"] for r in tr]) for k in FEATURES}
    groups=defaultdict(list)
    for r in rows:
        if r["split"]=="test":groups[r["participant_id"],r["session_id"]].append(r)
    windows=[]
    for (p,s),group in sorted(groups.items()):
        group.sort(key=lambda r:r["t_rgb_s"])
        if len(set(r["t_rgb_s"] for r in group))!=len(group):raise ValueError("DUPLICATE_TIMESTAMP")
        start=group[0]["t_rgb_s"];bins=defaultdict(list)
        for r in group:bins[int((r["t_rgb_s"]-start+1e-8)//5)].append(r)
        for wi,chunk in sorted(bins.items()):
            if chunk[-1]["t_rgb_s"]-chunk[0]["t_rgb_s"]<4.9:continue
            valid=[r for r in chunk if r["valid_ref"]=="1"]
            rec=dict(participant=p,session=s,window=wi,device=chunk[0]["device"],
                     lighting=chunk[0]["lighting"],glasses=chunk[0]["glasses"],
                     valid=len(valid),expected=round(5*float(m["camera_fps"])))
            reason=None
            if len(valid)<.8*rec["expected"]:reason="LOW_VALIDITY"
            elif sd([r["reference_mm"] for r in valid])<.1:reason="LOW_REFERENCE_VARIANCE"
            elif sd([r["rgb_ratio"] for r in valid])<1e-12:reason="CONSTANT_RGB"
            if reason:
                rec.update(admitted=False,accurate=False,reason=reason);windows.append(rec);continue
            ref=[r["reference_mm"] for r in valid];metrics={}
            for f in FEATURES:
                a,b=models[f];pred=[a*r[f]+b for r in valid]
                metrics[f]=dict(r=corr(pred,ref),amplitude=sd(pred)/sd(ref),
                     nrmse=math.sqrt(avg([(x-y)**2 for x,y in zip(pred,ref)]))/sd(ref))
            a,b=models["rgb_ratio"];pred=[a*r["rgb_ratio"]+b for r in valid]
            shuffled=pred[len(pred)//2:]+pred[:len(pred)//2]
            metrics["half_window_shift"]=dict(r=corr(shuffled,ref))
            nuisance=max(v["r"] for k,v in metrics.items() if k!="rgb_ratio" and v["r"] is not None)
            l=lag(pred,ref,[r["t_rgb_s"] for r in valid],float(m["camera_fps"]))
            x=metrics["rgb_ratio"]
            good=(x["r"] is not None and x["r"]>=.75 and l is not None and l<=.067 and
                  .75<=x["amplitude"]<=1.25 and x["nrmse"]<=.70 and x["r"]>=nuisance+.10)
            rec.update(admitted=True,accurate=good,reason="PASS" if good else "WAVEFORM_OR_CONTROL_FAIL",
                       metrics=metrics,lag_s=l,nuisance_max_r=nuisance)
            windows.append(rec)
    accepted=[w for w in windows if w["admitted"]];by_p=defaultdict(list)
    for w in accepted:by_p[w["participant"]].append(w)
    r_ci=None;acc_ci=None
    if by_p:
        rng=random.Random(261);keys=sorted(by_p);rs=[];acc=[]
        for _ in range(2000):
            draw=[w for _ in keys for w in by_p[rng.choice(keys)]]
            rs.append(avg([w["metrics"]["rgb_ratio"]["r"] for w in draw]))
            acc.append(avg([int(w["accurate"]) for w in draw]))
        rs.sort();acc.sort();r_ci=[rs[49],rs[1949]];acc_ci=[acc[49],acc[1949]]
    tr_all=[r for r in rows if r["split"]=="train"];test=[r for r in rows if r["split"]=="test"]
    holdouts={k:bool(tr_all and test and set(r[k] for r in tr_all).isdisjoint(set(r[k] for r in test)))
              for k in ("device","lighting","glasses")}
    holdouts["participant"]=True
    coverage=len(accepted)/len(windows) if windows else 0
    accuracy=avg([int(w["accurate"]) for w in accepted]) if accepted else 0
    base=bool(m["data_type"]=="human" and len(by_p)>=8 and accuracy>=.75 and
              r_ci is not None and r_ci[0]>=.75)
    return dict(protocol="E002-261+E002-267",gates=G,source_type=m["data_type"],
                participant_count=len(by_p),test_windows=len(windows),admitted=len(accepted),
                passed=sum(w["accurate"] for w in accepted),coverage=coverage,
                conditional_accuracy=accuracy,bootstrap_mean_r_ci95=r_ci,
                bootstrap_accuracy_ci95=acc_ci,holdouts=holdouts,
                positive_control_gate_pass=base,
                product_gate_pass=base and coverage>=.5 and all(holdouts.values()),
                training_calibration=models,windows=windows)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--csv",required=True);p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();m=json.load(open(a.manifest));rows=load(a.csv);out=evaluate(rows,m)
    out["input_sha256"]={k:hashlib.sha256(open(v,"rb").read()).hexdigest() for k,v in (("csv",a.csv),("manifest",a.manifest))}
    with open(a.out,"w") as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps({k:v for k,v in out.items() if k not in ("windows","training_calibration")},indent=2))
