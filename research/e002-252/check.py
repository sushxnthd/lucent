import csv,hashlib,io,json
from pathlib import Path
root=Path("research/e002-228")
d=json.loads((root/"E002_252_RAW.json").read_text())
r=d["result"]
b=d["raw_csv"].replace("\n","\r\n").encode()
assert hashlib.sha256(b).hexdigest()==r["raw_sha256"]
a=list(csv.DictReader(io.StringIO(d["raw_csv"])))
assert len(a)==r["n_rows"]==180
assert len({(x["participant"],x["frame"],x["eye"]) for x in a})==180
