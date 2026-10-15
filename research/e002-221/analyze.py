#!/usr/bin/env python3
"""E002-221: admission audit. Browser event time is not certified exposure time."""
import json, math, hashlib, subprocess, bisect, statistics, collections
from pathlib import Path
D=Path("research/e002-221")
PIN={"P_33":{"video":"edd83fd16806778ffe6565e5f2311a5dac17909edbfb603576d0b5448ec487d8","tracker":"3536d3d41ff8b2356fc35ce7f985c2000d671137ed33b8207669c72ca607265d","events":"8d05ddea2108fafb836aa1f26c3f40be0e0d9562e3183d3c93ce6fefb451cc62"},"P_54":{"video":"dcfaa40b4c80b0c5a0c09a993d3d203ff33bed760a12ba0801e0db383a620869","tracker":"359838799cd8f02aab75e14f18ad571a33827165cf446558854462bea660e8f5","events":"f03b60c1ceab65794de07a205b9f1c405dc2d16aa7f29e850974819237369937"}}
def quant(a,q):
 if not a:return None
 a=sorted(a);f=(len(a)-1)*q;i=int(f)
 return round(a[i]*(1-(f-i))+a[min(i+1,len(a)-1)]*(f-i),5)
def walk(obj):
 stack=[obj];out=[]
 while stack:
  x=stack.pop()
  if isinstance(x,list):stack.extend(x)
  elif isinstance(x,dict):
   if "epoch" in x and ("type" in x or "event" in x):out.append(x)
   else:stack.extend(x.values())
 return out
def admissible(x,eye):
 d=x.get(eye+"_pupil_diameter")
 return x.get(eye+"_pupil_validity")==1 and isinstance(d,(int,float)) and math.isfinite(d) and d>0
def audit(p):
 raw={k:Path("/tmp/"+p+"_"+k).read_bytes() for k in ("video","tracker","events")}
 assert all(hashlib.sha256(raw[k]).hexdigest()==PIN[p][k] for k in raw),"source SHA mismatch"
 rows=[];bad=0
 for line in raw["tracker"].splitlines():
  try:
   x=json.loads(line)
   if isinstance(x,dict) and isinstance(x.get("true_time"),(int,float)):rows.append(x)
   else:bad+=1
  except ValueError:bad+=1
 rows.sort(key=lambda x:x["true_time"])
 ts=[float(x["true_time"]) for x in rows]
 event_obj=json.loads(raw["events"]); ev=walk(event_obj)
 task=[x for x in ev if "_3_" in str(x.get("sessionId",x.get("sessionString","")))]
 start=[x for x in task if "start" in (str(x.get("type",""))+" "+str(x.get("event",""))).lower() and isinstance(x.get("epoch"),(int,float))]
 stop=[x for x in task if "stop" in (str(x.get("type",""))+" "+str(x.get("event",""))).lower() and isinstance(x.get("epoch"),(int,float))]
 t0=min([float(x["epoch"])/1000 for x in start],default=None)
 pts=[float(x["pts_time"]) for x in json.loads(subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries","packet=pts_time","-of","json","/tmp/"+p+"_video"]))["packets"] if "pts_time" in x]
 window=[t for t in pts if 5<=t<10]
 result={"participant":p,"sha256":PIN[p],"tracker_rows":len(rows),"tracker_unparsed":bad,
  "tracker_median_interval_ms":quant([(ts[i]-ts[i-1])*1000 for i in range(1,len(ts))],.5),
  "event_count":len(ev),"session3_events":len(task),"session3_start_count":len(start),"session3_stop_count":len(stop),
  "event_top_keys":list(event_obj)[:10] if isinstance(event_obj,dict) else [],
  "browser_start_epoch_s":t0,"video_window_packets":len(window),
  "video_window_unique":len(set(window)),"video_window_unique_fraction":round(len(set(window))/len(window),6) if window else None,
  "reference_window":None,"offset_sensitivity":{},"exposure_sync_certified":False,"waveform_tested":False}
 if t0 is None:return result
 selected=[x for x in rows if t0+5<=x["true_time"]<t0+10]
 result["reference_window"]={"count":len(selected),"left_valid":sum(admissible(x,"left") for x in selected),
 "right_valid":sum(admissible(x,"right") for x in selected),
 "either_valid":sum(admissible(x,"left") or admissible(x,"right") for x in selected),
 "left_p05_p95":[quant([x["left_pupil_diameter"] for x in selected if admissible(x,"left")],q) for q in (.05,.95)],
 "right_p05_p95":[quant([x["right_pupil_diameter"] for x in selected if admissible(x,"right")],q) for q in (.05,.95)]}
 for shift in (-1,-.5,0,.5,1):
  count=collections.Counter()
  for t in window:
   target=t0+t+shift
   i=bisect.bisect_left(ts,target)
   cand=[j for j in (i-1,i) if 0<=j<len(ts)]
   if not cand:continue
   j=min(cand,key=lambda j:abs(ts[j]-target))
   if abs(ts[j]-target)<=.075:
    count["near"]+=1
    for eye in ("left","right"):
     if admissible(rows[j],eye):count[eye]+=1
  result["offset_sensitivity"][str(shift)]={"near":count["near"],"left":count["left"],"right":count["right"],
   "left_fraction":round(count["left"]/len(window),6) if window else None,
   "right_fraction":round(count["right"]/len(window),6) if window else None}
 return result
out={"run":"E002-221","reference":"native-time Tobii Pro X3-120 pupil diameter","anchor":"browser recording-start event (provisional only)","participants":{}}
for p in PIN:out["participants"][p]=audit(p)
D.joinpath("RESULTS.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({k:{"events":v["session3_events"],"start":v["browser_start_epoch_s"],"reference":v["reference_window"],"offset_sensitivity":v["offset_sensitivity"]} for k,v in out["participants"].items()},indent=2))
