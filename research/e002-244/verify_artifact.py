import csv,hashlib,io,json,sys,zipfile
z=zipfile.ZipFile(sys.argv[1]);e=json.loads(z.read("e002-228/E002_244_RAW.json"))
raw=e["raw_csv"].replace("\n","\r\n").encode()
assert hashlib.sha256(raw).hexdigest()==e["result"]["raw_sha256"]
a=list(csv.DictReader(io.StringIO(e["raw_csv"])))
v=list(csv.DictReader(io.StringIO(z.read("e002-225/RAW_VISIBILITY.csv").decode())))
idx={(r["participant"],r["frame_index"],r["eye"]):r for r in v}
assert len(a)==len(v)==120
assert len({(r["participant"],r["frame"],r["eye"]) for r in a})==120
for p,eyes in e["result"]["groups"].items():
 for eye,g in eyes.items():
  b=[r for r in a if r["participant"]==p and r["eye"]==eye]
  assert len(b)==30
  assert all(r["frame_sha256"]==idx[(p,r["frame"],eye)]["frame_sha256"] for r in b)
  assert sum(int(r["eligible"]) for r in b)==g["admitted"]
assert not e["result"]["human_reference_compared"]
print("INDEPENDENT_PASS",sum(int(r["eligible"]) for r in a))
