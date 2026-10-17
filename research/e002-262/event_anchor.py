#!/usr/bin/env python3
"""Original-human bilateral eye-tracker validity-event preflight; not blink truth."""
import json,hashlib,math,copy
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
def runs(rows,eye=None):
 out=[];cur=[]
 for x in rows:
  bad=(not valid(x,"left") and not valid(x,"right")) if eye is None else not valid(x,eye)
  if bad:
   if cur and x["true_time"]-cur[-1]["true_time"]>.1:out.append(cur);cur=[]
   cur.append(x)
  elif cur:out.append(cur);cur=[]
 if cur:out.append(cur)
 return [{"first":round(z[0]["true_time"],5),"last":round(z[-1]["true_time"],5),"n":len(z)} for z in out if len(z)>=2]
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
 both=runs(win)
 return {"source_sha256":PINS[p],"session_start_epoch_s":t0,"reference_rows":len(win),
         "left_valid":sum(valid(x,"left") for x in win),
         "right_valid":sum(valid(x,"right") for x in win),
         "both_invalid_samples":sum(not valid(x,"left") and not valid(x,"right") for x in win),
         "bilateral_invalid_episodes_ge2":both,
         "unilateral_invalid_episodes_ge2":{"left":runs(win,"left"),"right":runs(win,"right")},
         "two_event_clock_gate":"PASS" if len(both)>=2 else "FAIL"}
def check(o):
 for v in o["participants"].values():
  n=v["reference_rows"];a=v["left_valid"];b=v["right_valid"]
  assert 0<=a<=n and 0<=b<=n
  assert 0<=v["both_invalid_samples"]<=min(n-a,n-b)
  assert v["two_event_clock_gate"]==("PASS" if len(v["bilateral_invalid_episodes_ge2"])>=2 else "FAIL")
 assert o["human_waveform_evaluated"] is False
if __name__=="__main__":
 o={"run":"E002-262","source":"Brown EOTT original P_33/P_54",
    "participants":{p:audit(p) for p in PINS},
    "human_waveform_evaluated":False,"clock_sync_certified":False,
    "scope":"reference-only five-second validity preflight; invalidity is not independently confirmed blink"}
 check(o);bad=copy.deepcopy(o);bad["participants"]["P_33"]["two_event_clock_gate"]="PASS"
 try:check(bad)
 except AssertionError:o["mutation_test"]="DETECTED"
 else:raise AssertionError("MUTATION_ESCAPED")
 Path("research/e002-220/E002_262.json").write_text(json.dumps(o,sort_keys=True,indent=2)+"\n")
 print("E002_262_RESULT="+json.dumps(o,sort_keys=True))
