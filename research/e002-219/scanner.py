import struct
from member import get
def scan(url,offset):
 b=get(url,offset,524288);p=b.find(bytes.fromhex("504b0102"))
 while p>=0 and p+46<len(b) and b[p:p+4]==bytes.fromhex("504b0102"):
  flags,method=struct.unpack_from("<HH",b,p+8)
  crc,csize,usize=struct.unpack_from("<III",b,p+16)
  n,e,k=struct.unpack_from("<HHH",b,p+28)
  local=struct.unpack_from("<I",b,p+42)[0]
  end=p+46+n+e+k
  if end>len(b):break
  raw=b[p+46:p+46+n]
  if raw.endswith(b"/session_data.csv"):
   if 0xffffffff in (csize,usize,local):raise ValueError("ZIP64 entry needs separate parser")
   yield (raw,flags,method,crc,csize,usize,local)
  p=end
