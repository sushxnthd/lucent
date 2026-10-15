#!/usr/bin/env python3
"""Independent fail-closed arithmetic and hash checker for E002-205."""
import csv,hashlib,io,itertools,json,math
from pathlib import Path
p=Path(__file__).resolve().parent/"results/EDGE_GATE_RESULTS.json"
assert p.exists(),"MISSING_RESULTS"
d=json.loads(p.read_text());rows=d["rows"]
assert d["reference"]=="SYNTHETIC_ONLY" and d["rgb"]=="NOT_TESTED" and d["source_replay"]=="PASS"
assert len(rows)==9 and len({r["case"] for r in rows})==9
assert math.isclose(d["max_leading_gap_s"],.25) and math.isclose(d["max_trailing_gap_s"],31/120)
badsets={"all_valid":set(),"first_30_invalid":set(range(30)),
"last_30_invalid":set(range(570,600)),"both_edges_15_invalid":set(range(15))|set(range(585,600)),
"first_4_invalid":set(range(4)),"first_1_invalid":{0},
"isolated_30_invalid":set(range(10,600,20)),"middle_30_invalid":set(range(285,315)),
"all_invalid":set(range(600))}
for r in rows:
 bad=badsets[r["case"]];valid=[i for i in range(600) if i not in bad]
 assert r["n_valid"]==len(valid)
 s=io.StringIO();w=csv.writer(s,delimiter="\t",lineterminator="\n")
 w.writerow(["system_timestamp","left_pupil_valid","left_gaze_point_valid","left_pupil_diameter",
             "right_pupil_valid","right_gaze_point_valid","right_pupil_diameter"])
 for i in range(600):
  ok=i not in bad
  w.writerow([f"{i*1e6/120:.6f}",int(ok),int(ok),"3.2" if ok else "-1",
              int(ok),int(ok),"3.2" if ok else "-1"])
 assert hashlib.sha256(s.getvalue().encode()).hexdigest()==r["tsv_sha256"]
 if len(valid)>1:
  interior=max((b-a)/120 for a,b in zip(valid,valid[1:]))
  old=len(valid)>=570 and interior<=.026
  new=old and max(valid[0]/120,5-valid[-1]/120,interior)<=.026
 else:old=new=False
 assert r["old_pass"]==old and r["boundary_pass"]==new
assert sum(r["old_pass"] and not r["boundary_pass"] for r in rows)==4
for n in range(2,11):
 for k in range(1,n+1):
  seq=[v for v in itertools.product((0,1),repeat=n) if sum(v)==k]
  assert max(next(i for i,b in enumerate(v) if b) for v in seq)==n-k
  assert max(n-1-max(i for i,b in enumerate(v) if b) for v in seq)==n-k
print("PASS: independent hash verification, 9/9 cases, four false acceptances, sharp finite edge bound n<=10")
