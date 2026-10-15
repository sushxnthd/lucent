import struct,zlib
from probe import fetch
def get(url,offset,size):
 if not 0<size<=1500000:raise ValueError("budget")
 status,headers,data=fetch(url,headers={"Range":f"bytes={offset}-{offset+size-1}"},limit=size)
 if status!=206 or len(data)!=size:raise ValueError("range failure")
 return data
def member(url,entry):
 name,flags,method,crc,csize,usize,offset=entry
 if flags&1 or method not in (0,8) or max(csize,usize)>1000000:raise ValueError("unsupported")
 head=get(url,offset,30)
 if head[:4]!=bytes.fromhex("504b0304"):raise ValueError("header")
 n,e=struct.unpack_from("<HH",head,26)
 if get(url,offset+30,n)!=name:raise ValueError("filename")
 data=get(url,offset+30+n+e,csize)
 payload=zlib.decompress(data,-15) if method==8 else data
 if len(payload)!=usize or zlib.crc32(payload)&0xffffffff!=crc:raise ValueError("CRC")
 return payload
