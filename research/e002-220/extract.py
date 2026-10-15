import source,zipfile,struct,zlib,hashlib,json
from pathlib import Path
def raw(r,i):
 r.seek(i.header_offset);h=r.read(30)
 if h[:4]!=b"PK\x03\x04":raise ValueError("ZIP header")
 n,e=struct.unpack_from("<HH",h,26)
 r.seek(i.header_offset+30+n+e);b=r.read(i.compress_size)
 if i.compress_type==8:b=zlib.decompress(b,-15)
 elif i.compress_type!=0:raise ValueError("ZIP method")
 if len(b)!=i.file_size or zlib.crc32(b)&0xffffffff!=i.CRC:raise ValueError("CRC")
 return b
r=source.R();out={}
with zipfile.ZipFile(r) as z:
 a=z.infolist()
 for p in ("P_33","P_54"):
  q=[i for i in a if f"/{p}/" in "/"+i.filename]
  choose=lambda suffix:next(i for i in q if i.filename.endswith(suffix))
  v=choose("-study-dot_test.webm");t=choose("/"+p+".txt")
  log=next(i for i in q if i.filename.endswith(".json"))
  out[p]={}
  for kind,i in (("video",v),("tracker",t),("events",log)):
   b=raw(r,i);Path("/tmp/"+p+"_"+kind).write_bytes(b)
   out[p][kind]={"path":i.filename,"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"crc32":i.CRC}
Path("research/e002-220/MEMBER_HASHES.json").write_text(json.dumps(out,indent=2))
print("CRC/SHA verified",[(p,{k:v["bytes"] for k,v in d.items()}) for p,d in out.items()])
