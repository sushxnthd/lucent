import struct
def resolve(extra,usize,csize,local):
 p=0
 while p+4<=len(extra):
  tag,n=struct.unpack_from("<HH",extra,p);p+=4
  data=extra[p:p+n];p+=n
  if tag!=1:continue
  q=0
  if usize==0xffffffff:usize=struct.unpack_from("<Q",data,q)[0];q+=8
  if csize==0xffffffff:csize=struct.unpack_from("<Q",data,q)[0];q+=8
  if local==0xffffffff:local=struct.unpack_from("<Q",data,q)[0];q+=8
  break
 if 0xffffffff in (usize,csize,local):raise ValueError("ZIP64 missing")
 return usize,csize,local
