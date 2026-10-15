#!/usr/bin/env python3
"""E002-205: test actual E002-204 native_window.trial with synthetic boundary censoring."""
import csv,hashlib,importlib.util,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
N=600;HZ=120;W=5.;GAP=.026
def synth(bad):
 s=io.StringIO();w=csv.writer(s,delimiter="\t",lineterminator="\n")
 w.writerow(["system_timestamp","left_pupil_valid","left_gaze_point_valid","left_pupil_diameter",
             "right_pupil_valid","right_gaze_point_valid","right_pupil_diameter"])
 for j in range(N):
  ok=j not in bad
  w.writerow([f"{j*1e6/HZ:.6f}",int(ok),int(ok),"3.2" if ok else "-1",
              int(ok),int(ok),"3.2" if ok else "-1"])
 return s.getvalue().encode()
def evaluate(bad):
 valid=[i for i in range(N) if i not in bad]
 if not valid:return False,False,None,None,None
 interior=max((b-a)/HZ for a,b in zip(valid,valid[1:])) if len(valid)>1 else None
 old=len(valid)>=570 and interior is not None and interior<=GAP
 first=valid[0]/HZ;last=W-valid[-1]/HZ
 return old,bool(old and max(first,last,interior)<=GAP),first,last,interior
def main():
 p=ROOT/"e002-204/native_window.py"
 assert p.exists(),"E002_204_SOURCE_MISSING"
 spec=importlib.util.spec_from_file_location("e204",p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 cases={"all_valid":set(),"first_30_invalid":set(range(30)),
        "last_30_invalid":set(range(570,600)),
        "both_edges_15_invalid":set(range(15))|set(range(585,600)),
        "first_4_invalid":set(range(4)),"first_1_invalid":{0},
        "isolated_30_invalid":set(range(10,600,20)),
        "middle_30_invalid":set(range(285,315)),"all_invalid":set(range(600))}
 expected={"all_valid":(True,True),"first_30_invalid":(True,False),
           "last_30_invalid":(True,False),"both_edges_15_invalid":(True,False),
           "first_4_invalid":(True,False),"first_1_invalid":(True,True),
           "isolated_30_invalid":(True,True),"middle_30_invalid":(False,False),
           "all_invalid":(False,False)}
 rows=[]
 for name,bad in cases.items():
  data=synth(bad);old,new,first,last,interior=evaluate(bad)
  actual=mod.trial(data)["eyes"]["left"]
  assert actual["pass"]==old,(name,actual)
  assert actual["window_valid"]==600-len(bad),(name,actual)
  assert (old,new)==expected[name],name
  rows.append({"case":name,"tsv_sha256":hashlib.sha256(data).hexdigest(),
               "n_valid":600-len(bad),"old_pass":old,"boundary_pass":new,
               "first_gap_s":first,"last_gap_s":last,"interior_gap_s":interior})
 out={"run":"E002-205","source_blob_sha":"d7cfbea86c38f98bcdceac12ac16b04127bbef88",
      "source_replay":"PASS","reference":"SYNTHETIC_ONLY","rgb":"NOT_TESTED",
      "max_leading_gap_s":30/120,"max_trailing_gap_s":31/120,"rows":rows}
 dest=Path(__file__).resolve().parent/"results";dest.mkdir(exist_ok=True)
 (dest/"EDGE_GATE_RESULTS.json").write_text(json.dumps(out,indent=2)+"\n")
 print("PASS: actual E002-204 gate accepts 4 edge-censored counterexamples; boundary-inclusive gate rejects all four.")
if __name__=="__main__":main()
