import csv,io,json
from pathlib import Path
p=Path("research/e002-228")
d=json.loads((p/"E002_252_RAW.json").read_text())
a=list(csv.DictReader(io.StringIO(d["raw_csv"])))
g={}
for person in ("P_01","P_02","P_07"):
 v=[x for x in a if x["participant"]==person and x["eligible"]=="1"]
 n=sum(float(x["radius_ratio"]) in (.20,.78) for x in v)
 g[person]=[len(v),n]
print(g)
