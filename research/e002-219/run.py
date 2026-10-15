import csv,io,json,hashlib
from probe import archive_probe
from scanner import scan
from member import member
a=archive_probe()
for e in scan(a["url"],a["central_directory_offset"]+int(.01*a["central_directory_bytes"])):
 b=member(a["url"],e)
 rows=list(csv.reader(io.StringIO(b.decode("utf-8-sig"))))
 print(json.dumps({"member":e[0].decode(),"sha256":hashlib.sha256(b).hexdigest(),"columns":rows[0],"rows":len(rows)-1,"unique_timestamps":len(set(r[0] for r in rows[1:])),"native_time_certified":False}))
 break
