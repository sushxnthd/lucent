import hashlib,zipfile
from parser import parse
def load(path):
    groups=[];manifest=[];errors=[]
    with zipfile.ZipFile(path) as z:
        for n in sorted(x for x in z.namelist() if x.lower().endswith(".tag")):
            raw=z.read(n)
            item={"file":n,"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}
            try:
                rows=parse(raw.decode("utf-8-sig"))
                item["frames"]=len(rows)
                groups.append((n,rows))
            except Exception as e:
                item["error"]=str(e)
                errors.append(item)
            manifest.append(item)
    return groups,manifest,errors
