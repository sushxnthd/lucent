import json
from pathlib import Path
def rows(path):
 s=Path(path).read_text(errors="replace")
 try:a=json.loads(s)
 except ValueError:a=None
 if isinstance(a,list):
  for x in a:
   if isinstance(x,dict):yield x
 elif isinstance(a,dict):
  for x in a.get("events",a.get("records",[])):
   if isinstance(x,dict):yield x
 else:
  for line in s.splitlines():
   try:
    x=json.loads(line)
    if isinstance(x,dict):yield x
   except ValueError:continue
