import json,runpy,sys
from pathlib import Path
sys.path.insert(0,"research/e002-234")
source=json.loads(Path("research/e002-228/E002_247_SOURCE.json").read_text())
ns=runpy.run_path("research/e002-234/run.py",run_name="e002_247")
main=ns["main"]
main.__globals__["PINS"]={p:d["video"]["sha256"] for p,d in source["participants"].items()}
main.__globals__["OUT"]=Path("research/e002-228")
main()
out=Path("research/e002-228")
data={"source":source,"raw_csv":(out/"RAW_BOUNDARY.csv").read_text(),"original_result":json.loads((out/"RESULTS.json").read_text()),"reference_compared":False}
(out/"E002_247_RAW.json").write_text(json.dumps(data,sort_keys=True))
print("E002-247 detector unchanged")
