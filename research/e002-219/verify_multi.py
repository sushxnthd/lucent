import json,pathlib
p=pathlib.Path("research/e002-219")
a=json.loads((p/"MULTI_RESULTS.json").read_text())["windows"]
b=json.loads((p/"MULTI_VERIFIED.json").read_text())["samples"]
assert len(a)==len(b)==3
for x,y in zip(a,b):
 assert x["status"]=="ok"
 for k in ("member","sha256","rows","unique_timestamps"):assert x[k]==y[k]
 assert x["unique_timestamps"]==1
print("E002-219 independent pinned-byte and timestamp-collapse checks passed")
