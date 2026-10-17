#!/usr/bin/env python3
"""E002-262 original-human reference blink-clock admission.
Valid-free gaps, NOT consecutive invalid Tobii rows, are event candidates.
No physiological waveform or RGB blink claim.
"""
import json,hashlib,math,copy,statistics
from pathlib import Path
PINS={
"P_33":{"tracker":"3536d3d41ff8b2356fc35ce7f985c2000d671137ed33b8207669c72ca607265d","events":"8d05ddea2108fafb836aa1f26c3f40be0e0d9562e3183d3c93ce6fefb451cc62"},
"P_54":{"tracker":"359838799cd8f02aab75e14f18ad571a33827165cf446558854462bea660e8f5","events":"f03b60c1ceab65794de07a205b9f1c405dc2d16aa7f29e850974819237369937"}}
def walk(x):
 if isinstance(x,list):
  for y in x:yield from walk(y)
 elif isinstance(x,dict):
  if isinstance(x.get("epoch"),(int,float)) and ("event" in x or "type" in x):yield x
  else:
   for y in x.values():yield from walk(y)
def valid(x,e):
 d=x.get(e+"_pupil_diameter")
 return x.get(e+"_pupil_validity")==1 and isinstance(d,(int,float)) and math.isfinite(d) and d>0
def gaps(t,threshold=.1):
 t=sorted(set(t))
 return [{"start_epoch":round(a,5),"end_epoch":round(b,5),"gap_ms":round((b-a)*1000,3)}
         for a,b in zip(t,t[1:]) if b-a>=threshold]
def audit(p):
 raw={k:Path("/tmp/"+p+"_"+k).read_bytes() for k in ("tracker","events")}
 for k in raw:assert hashlib.sha256(raw[k]).hexdigest()==PINS[p][k],"SOURCE_SHA_FAIL"
 rows=[]
 for line in raw["tracker"].splitlines():
  try:
   x=json.loads(line)
   if isinstance(x,dict) and isinstance(x.get("true_time"),(int,float)):rows.append(x)
  except (ValueError,TypeError):pass
 rows.sort(key=lambda x:x["true_time"])
 ev=list(walk(json.loads(raw["events"])))
 task=[x for x in ev if "_3_" in str(x.get("sessionId",x.get("sessionString","")))]
 start=[x for x in task if "start" in (str(x.get("type",""))+" "+str(x.get("event",""))).lower()]
 assert start,"NO_START_EVENT"
 t0=min(float(x["epoch"])/1000 for x in start)
 win=[x for x in rows if t0+5<=x["true_time"]<t0+10]
 assert win,"NO_REFERENCE_WINDOW"
 left=[float(x["true_time"]) for x in win if valid(x,"left")]
 right=[float(x["true_time"]) for x in win if valid(x,"right")]
 either=sorted(set(left+right))
 primary=gaps(either,.1)
 all_dt=[(b-a)*1000 for a,b in zip(either,either[1:])]
 return {"source_sha256":PINS[p],"session_start_epoch_s":t0,"reference_rows":len(win),
         "left_valid":len(left),"right_valid":len(right),"either_valid_unique_times":len(either),
         "valid_fraction_left":round(len(left)/len(win),6),
         "valid_fraction_right":round(len(right)/len(win),6),
         "median_any_valid_spacing_ms":round(statistics.median(all_dt),3) if all_dt else None,
         "max_any_valid_spacing_ms":round(max(all_dt),3) if all_dt else None,
         "bilateral_valid_free_gaps_ge100ms":primary,
         "bilateral_valid_free_gaps_ge150ms":gaps(either,.15),
         "two_event_clock_gate":"PASS" if len(primary)>=2 else "FAIL"}
def check(o):
 for v in o["participants"].values():
  n=v["reference_rows"];a=v["left_valid"];b=v["right_valid"]
  assert 0<=a<=n and 0<=b<=n
  assert v["either_valid_unique_times"]>=max(a,b) or v["either_valid_unique_times"]>=min(a,b)
  assert v["two_event_clock_gate"]==("PASS" if len(v["bilateral_valid_free_gaps_ge100ms"])>=2 else "FAIL")
 assert o["human_waveform_evaluated"] is False
if __name__=="__main__":
 o={"run":"E002-262","source":"Brown EOTT original P_33/P_54",
    "participants":{p:audit(p) for p in PINS},
    "human_waveform_evaluated":False,"clock_sync_certified":False,
    "method":"consecutive gaps in union of native valid left/right Tobii timestamps; threshold 100ms, sensitivity 150ms",
    "warning":"tracker invalidity is not itself a blink; two gaps are only a necessary preflight, never sufficient synchronization"}
 check(o);bad=copy.deepcopy(o)
 v=bad["participants"]["P_33"]
 v["two_event_clock_gate"]="FAIL" if v["two_event_clock_gate"]=="PASS" else "PASS"
 try:check(bad)
 except AssertionError:o["mutation_test"]="DETECTED"
 else:raise AssertionError("MUTATION_ESCAPED")
 Path("research/e002-220/E002_262.json").write_text(json.dumps(o,sort_keys=True,indent=2)+"\n")
 print("E002_262_RESULT="+json.dumps(o,sort_keys=True))
