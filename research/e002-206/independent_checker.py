import json
from pathlib import Path
def main():
 o=json.loads(Path("research/e002-206/results/HUMAN_EDGE_COVERAGE.json").read_text())
 assert len(o["participants"])==15 and not o["errors"]
 for eye in ("left","right"):
  old_count=new_count=0
  for p in o["participants"]:
   times=p["times_s"];e=p["eyes"][eye]
   assert len(times)==len(e["bits"])
   assert all(b>a for a,b in zip(times,times[1:]))
   selected=[t for t,b in zip(times,e["bits"]) if b=="1"]
   assert len(selected)==e["valid_n"]
   gaps=[b-a for a,b in zip(selected,selected[1:])]
   max_interior=max(gaps) if gaps else 100.0
   original=len(selected)>=570 and len(selected)/len(times)>=.95 and max_interior<=.026
   corrected=original and max(selected[0],5-selected[-1],max_interior)<=.026
   assert e["old_pass"]==original and e["complete_pass"]==corrected
   old_count+=original;new_count+=corrected
  assert o[eye]["old_pass"]==old_count and o[eye]["complete_pass"]==new_count
  assert o[eye]["product_75pct"]==(new_count>=12)
 print("PASS independent 30-eye human timestamp and validity replay")
if __name__=="__main__":main()
