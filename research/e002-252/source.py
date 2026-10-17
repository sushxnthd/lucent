"""E002-252: fixed-participant original RGB source retrieval and integrity."""
import hashlib,json,sys,zipfile
from pathlib import Path
sys.path.insert(0,"research/e002-220")
from source import R
PEOPLE=("P_01","P_02","P_07")
out={}
with zipfile.ZipFile(R()) as z:
    entries=z.infolist()
    for person in PEOPLE:
        candidates=[x for x in entries if ("/"+person+"/") in ("/"+x.filename) and x.filename.endswith("-study-dot_test.webm")]
        if len(candidates)!=1:
            raise RuntimeError("Ambiguous or missing frozen video "+person+": "+str([x.filename for x in candidates]))
        info=candidates[0]
        data=z.read(info)
        assert len(data)==info.file_size
        dest=Path("/tmp")/(person+"_video")
        dest.write_bytes(data)
        out[person]={"video":{"path":info.filename,"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data),"crc32":info.CRC}}
Path("research/e002-228/E002_252_SOURCES.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print("E002-252 source CRC verified",[(p,x["video"]["bytes"]) for p,x in out.items()])
