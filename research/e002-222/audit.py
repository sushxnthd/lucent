#!/usr/bin/env python3
"""E002-222: blinded-to-RGB-pupil, native source timing and reference-signal admission.
Uses E002-220 verified extracted bytes. No RGB waveform fit or fatigue inference.
"""
import collections, hashlib, json, math, statistics, subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path("research/e002-222")
ROOT.mkdir(parents=True,exist_ok=True)
PINS={
"P_33":{"video":"edd83fd16806778ffe6565e5f2311a5dac17909edbfb603576d0b5448ec487d8","tracker":"3536d3d41ff8b2356fc35ce7f985c2000d671137ed33b8207669c72ca607265d","events":"8d05ddea2108fafb836aa1f26c3f40be0e0d9562e3183d3c93ce6fefb451cc62"},
"P_54":{"video":"dcfaa40b4c80b0c5a0c09a993d3d203ff33bed760a12ba0801e0db383a620869","tracker":"359838799cd8f02aab75e14f18ad571a33827165cf446558854462bea660e8f5","events":"f03b60c1ceab65794de07a205b9f1c405dc2d16aa7f29e850974819237369937"}
}
def quant(v,q):
 if not v:return None
 v=sorted(v);p=(len(v)-1)*q;i=int(p)
 return round(v[i]*(1-p+i)+v[min(i+1,len(v)-1)]*(p-i),6)
def pearson(a,b):
 if len(a)<3:return None
 ma=statistics.fmean(a);mb=statistics.fmean(b)
 aa=[x-ma for x in a];bb=[x-mb for x in b]
 den=math.sqrt(sum(x*x for x in aa)*sum(y*y for y in bb))
 return round(sum(x*y for x,y in zip(aa,bb))/den,6) if den>0 else None
def events_walk(x):
 if isinstance(x,list):
  for v in x:yield from events_walk(v)
 elif isinstance(x,dict):
  if "epoch" in x and ("type" in x or "event" in x):yield x
  else:
   for v in x.values():yield from events_walk(v)
def ffprobe(video,frames=False):
 entries="frame=best_effort_timestamp_time,pkt_dts_time,pkt_duration_time" if frames else "packet=pts_time,dts_time,duration_time"
 key="frames" if frames else "packets"
 raw=subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries",entries,"-of","json",str(video)])
 return json.loads(raw).get(key,[])
def summary_pts(vals):
 v=[float(t) for t in vals if t is not None]
 if not v:return {"n":0}
 diffs=[v[i]-v[i-1] for i in range(1,len(v))]
 nonzero=[d for d in diffs if d>0]
 return {"n":len(v),"distinct":len(set(v)),"distinct_fraction":round(len(set(v))/len(v),6),
  "first":v[0],"last":v[-1],"span_s":round(v[-1]-v[0],6),
  "nonmonotone":sum(d<0 for d in diffs),"zero_delta":sum(d==0 for d in diffs),
  "positive_step_median_ms":quant([d*1000 for d in nonzero],.5),
  "positive_step_p95_ms":quant([d*1000 for d in nonzero],.95)}
def ref_summary(rows,t0,t1):
 out={"native_records":len(rows)}
 for eye in ("left","right"):
  v=[(float(r["true_time"]),float(r[eye+"_pupil_diameter"])) for r in rows
     if r.get(eye+"_pupil_validity")==1 and isinstance(r.get(eye+"_pupil_diameter"),(int,float))
     and math.isfinite(r[eye+"_pupil_diameter"]) and r[eye+"_pupil_diameter"]>0]
  w=[(t,d) for t,d in v if t0<=t<t1]
  a=[d for _,d in w];ts=[t for t,_ in w]
  gaps=[1000*(ts[i]-ts[i-1]) for i in range(1,len(ts))]
  out[eye]={"valid":len(w),"p05_mm":quant(a,.05),"p95_mm":quant(a,.95),
   "std_mm":round(statistics.pstdev(a),6) if a else None,
   "range_p95_p05_mm":round(quant(a,.95)-quant(a,.05),6) if a else None,
   "median_valid_gap_ms":quant(gaps,.5),"p95_valid_gap_ms":quant(gaps,.95),
   "gaps_over_75ms":sum(d>75 for d in gaps)}
 pair=[(float(r["left_pupil_diameter"]),float(r["right_pupil_diameter"])) for r in rows
  if t0<=r["true_time"]<t1 and all(r.get(e+"_pupil_validity")==1 and
   isinstance(r.get(e+"_pupil_diameter"),(int,float)) and
   math.isfinite(r[e+"_pupil_diameter"]) and r[e+"_pupil_diameter"]>0 for e in ("left","right"))]
 out["binocular_joint_valid"]=len(pair)
 out["binocular_pearson"]=pearson([x for x,y in pair],[y for x,y in pair]) if pair else None
 return out
def audit(p):
 raw={k:Path("/tmp/"+p+"_"+k).read_bytes() for k in ("video","tracker","events")}
 observed={k:hashlib.sha256(v).hexdigest() for k,v in raw.items()}
 assert observed==PINS[p],f"PIN mismatch for {p}"
 rows=[]
 for line in raw["tracker"].splitlines():
  try:
   x=json.loads(line)
   if isinstance(x,dict) and isinstance(x.get("true_time"),(int,float)):rows.append(x)
  except (ValueError,TypeError):pass
 rows.sort(key=lambda x:x["true_time"])
 ev=sorted(events_walk(json.loads(raw["events"])),key=lambda x:x.get("epoch",0))
 sess=[x for x in ev if "_3_" in str(x.get("sessionId",x.get("sessionString","")))]
 starts=[x for x in sess if "recording start" in str(x.get("type","")).lower()]
 stops=[x for x in sess if "recording stop" in str(x.get("type","")).lower()]
 t0=min((float(x["epoch"])/1000 for x in starts),default=None)
 stop=min((float(x["epoch"])/1000 for x in stops if t0 is not None and float(x["epoch"])/1000>=t0),default=None)
 packets=ffprobe(Path("/tmp/"+p+"_video"))
 frames=ffprobe(Path("/tmp/"+p+"_video"),True)
 pkt=summary_pts([x.get("pts_time") for x in packets])
 frm=summary_pts([x.get("best_effort_timestamp_time") for x in frames])
 types=collections.Counter(str(x.get("type","<missing>"))+" | "+str(x.get("event","<missing>")) for x in sess)
 anchors=[{"type":str(x.get("type","")),"event":str(x.get("event","")),
           "epoch_s":round(float(x["epoch"])/1000,6),
           "time_ms":x.get("time")} for x in sess
          if "recording" in str(x.get("type","")).lower() and isinstance(x.get("epoch"),(int,float))]
 out={"participant":p,"sha256":observed,"source_bytes":{k:len(v) for k,v in raw.items()},
  "session3_event_count":len(sess),"session3_event_types":dict(types.most_common(20)),
  "session3_recording_anchors":anchors[:15],"start_epoch_s":t0,"stop_epoch_s":stop,
  "event_recording_duration_s":round(stop-t0,6) if t0 is not None and stop is not None else None,
  "packet_pts":pkt,"decoded_frame_pts":frm,"video_packet_count":len(packets),
  "tracker_true_time_min_max":[rows[0]["true_time"],rows[-1]["true_time"]] if rows else None,
  "clock_anchor_certified":False,"exposure_sync_certified":False,
  "native_rgb_pupil_waveform_tested":False}
 if t0 is not None:
  out["reference_first_5s"]=ref_summary([r for r in rows if t0+5<=r["true_time"]<t0+10],t0+5,t0+10)
  out["reference_full_video_window"]=ref_summary([r for r in rows if t0<=r["true_time"]<t0+max(pkt.get("span_s",0),0)],t0,t0+max(pkt.get("span_s",0),0))
  out["event_video_duration_difference_s"]=round((stop-t0)-pkt["span_s"],6) if stop is not None and pkt.get("span_s") is not None else None
 return out
out={"run":"E002-222","date_utc":datetime.now(timezone.utc).isoformat(),
 "source":"EOTT Brown ETRA 2018 original archive; source members verified SHA-256 and CRC32",
 "question":"Does this released video plus event log establish exposure-time alignment precise enough for 5s pupil waveform lag certification?",
 "participants":{p:audit(p) for p in PINS},
 "smallest_supported_claim":"Pending result audit; native eye-tracker sampling does not alone certify RGB exposure synchronization.",
 "scientific_gate":"No independent physical event-to-exposure anchor found unless evidence explicitly recorded.",
 "product_gate":"No lag-certified waveform admission without independent clock calibration."}
(ROOT/"RESULTS.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({p:{"event_duration":x["event_recording_duration_s"],"video_pts":x["packet_pts"],"decoded_pts":x["decoded_frame_pts"],"event_minus_pts":x.get("event_video_duration_difference_s"),"anchors":x["session3_recording_anchors"],"ref_5s":x.get("reference_first_5s")} for p,x in out["participants"].items()},indent=2))
