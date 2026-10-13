"""E002-159 original-human mask normalization sensitivity; not physiology."""
import csv,hashlib,json,math,random,collections,pathlib
P=pathlib.Path("research/e002-159");P.mkdir(parents=True,exist_ok=True)
SRC=pathlib.Path("research/e002-155/PAIRS.csv")
EXPECTED="ec150e35dc84e120f1a0418a003989f4948595a8034ecbc68088954cfe0ce730"
assert hashlib.sha256(SRC.read_bytes()).hexdigest()==EXPECTED,"pinned E002-155 input mismatch"
T=math.log(1.05)
def label(v):return 1 if v>=T else (-1 if v<=-T else 0)
rows=[]
with SRC.open(newline="") as f:
 for z in csv.DictReader(f):
  lag=int(z["lag"]);de=float(z["dE"]);dd=float(z["dD"]);dp=float(z["dPn"]);dq=float(z["dq"])
  a=dp/2;b=dq;c=(dp+de-dd)/2
  rows.append(dict(group=z["group"],lag=lag,frame1=z["frame1"],frame2=z["frame2"],
   A=a,B=b,C=c,dD=dd,aclass=label(a),bclass=label(b),cclass=label(c),
   disagree=int(label(a)!=label(b)),strong=int(label(a)*label(b)==-1),
   signflip=int(a*b<0),raw_disagree=int(label(c)!=label(b)),
   error=abs(b-(a-dd/2))))
assert len(rows)==17903
result={"experiment":"E002-159","classification":"POST_HOC_EXPLORATORY_ORIGINAL_HUMAN_MASKS",
 "source_sha256":EXPECTED,"original_archive_sha256":"049df72454682c1c77c50c8236bb607919a6e333528bc2b89c567b625e459700",
 "threshold_log_radius":T,"n_pairs":len(rows),"n_groups":len({r["group"] for r in rows}),
 "claim_boundary":"Only original-human annotated mask-normalization sensitivity; neither proxy is true pupil waveform, no tracker, RGB segmenter, participant identity, FPS or fatigue.","lags":{}}
for lag in (1,5,15,30):
 s=[r for r in rows if r["lag"]==lag];n=len(s)
 counts={k:sum(r[k] for r in s) for k in ("disagree","strong","signflip","raw_disagree")}
 groups={}
 for g in sorted({r["group"] for r in s}):
  t=[r for r in s if r["group"]==g]
  groups[g]={"n":len(t),"disagreement_n":sum(r["disagree"] for r in t),"strong_n":sum(r["strong"] for r in t)}
 ci=None
 if lag in (1,30):
  rng=random.Random(1592026);keys=sorted(groups);values=[]
  for _ in range(3000):
   chosen=rng.choices(keys,k=len(keys))
   values.append(sum(groups[g]["disagreement_n"] for g in chosen)/sum(groups[g]["n"] for g in chosen))
  values.sort();ci=[values[int(.025*(len(values)-1))],values[int(.975*(len(values)-1))]]
 v=sorted(abs(r["dD"]) for r in s);cut=v[math.ceil(.9*n)-1]
 hi=[r for r in s if abs(r["dD"])>=cut];lo=[r for r in s if abs(r["dD"])<cut]
 result["lags"][str(lag)]={"n":n,"counts":counts,"disagreement_rate":counts["disagree"]/n,
  "strong_opposite_rate":counts["strong"]/n,"signflip_rate":counts["signflip"]/n,
  "raw_vs_visible_disagreement_rate":counts["raw_disagree"]/n,"cluster_bootstrap_ci95":ci,
  "groups":groups,"wildcard":{"top_decile_dD_threshold":cut,"high_n":len(hi),
   "high_disagreement_rate":sum(r["disagree"] for r in hi)/len(hi),
   "lower_disagreement_rate":sum(r["disagree"] for r in lo)/len(lo)}}
result["max_decomposition_error"]=max(r["error"] for r in rows)
result["gates"]={"G0":result["n_groups"]>=10 and result["lags"]["1"]["n"]>=1000,
 "G1":result["lags"]["1"]["disagreement_rate"]<=.05,
 "G2":result["lags"]["30"]["disagreement_rate"]<=.05,
 "G3":sum(result["lags"][str(k)]["counts"]["strong"] for k in (1,5,15,30))==0,
 "G4":result["max_decomposition_error"]<1e-10,"G5":"CHECK_INDEPENDENTLY","G6":"UNTESTED"}
(P/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
with (P/"DISAGREEMENTS.csv").open("w",newline="") as f:
 fields=("group","lag","frame1","frame2","A","B","C","dD","aclass","bclass","cclass","disagree","strong","signflip","raw_disagree")
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:r[k] for k in fields} for r in rows if r["disagree"])
print(json.dumps({"gates":result["gates"],"lag_rates":{k:v["disagreement_rate"] for k,v in result["lags"].items()}},indent=2))
