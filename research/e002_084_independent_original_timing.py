#!/usr/bin/env python3
"""Lucent E002-084: CRC-verified original WebM vs independent ffprobe packet PTS."""
import json, re, struct, zlib, tempfile, subprocess
from urllib.request import Request, urlopen
from pathlib import Path
from decimal import Decimal

URL="https://webgazer.cs.brown.edu/data/WebGazerETRA2018Dataset_Release20180420.zip"
# ZIP local offset, compressed length, original length, CRC32, filename length, method
SPECS={
"P_02_initial":(1052426785,3946286,3953477,1427821152,81,8),
"P_02_final":(1045249967,3570629,3579633,3337732900,88,8),
"P_06_initial":(2542541874,3136910,3136910,2419120984,81,0),
"P_07_initial":(3091234193,2474428,2478911,3770429305,81,8)}
SEG=0x18538067; INFO=0x1549A966; SCALE=0x2AD7B1
TRACKS=0x1654AE6B; ENTRY=0xAE; TNUM=0xD7; TTYPE=0x83
CLUSTER=0x1F43B675; CTIME=0xE7; SIMPLE=0xA3; GROUP=0xA0; BLOCK=0xA1

def read_range(a,n):
    if not 0<n<8_000_000: raise ValueError("invalid range")
    b=a+n-1
    req=Request(URL,headers={"Range":f"bytes={a}-{b}","Accept-Encoding":"identity"})
    with urlopen(req,timeout=90) as response:
        if response.status!=206 or not re.fullmatch(rf"bytes {a}-{b}/\d+",response.headers.get("Content-Range","")):
            raise ValueError("Range server response invalid")
        data=response.read(n+1)
    if len(data)!=n: raise ValueError("Range truncated")
    return data

def original(spec):
    off,compressed,uncompressed,crc,namelen,method=spec
    h=struct.unpack("<IHHHHHIIIHH",read_range(off,30))
    if h[0]!=0x04034b50 or h[3]!=method or h[9]!=namelen or h[10]!=0:
        raise ValueError("ZIP local header mismatch")
    data=read_range(off+30+namelen,compressed)
    raw=zlib.decompress(data,-15) if method==8 else data
    if len(raw)!=uncompressed or (zlib.crc32(raw)&0xffffffff)!=crc:
        raise ValueError("ZIP CRC mismatch")
    return raw

def vint(buf,p,is_id=False):
    if p>=len(buf) or not buf[p]: raise ValueError("bad VINT")
    n=9-buf[p].bit_length()
    if n>(4 if is_id else 8) or p+n>len(buf): raise ValueError("bad VINT length")
    val=int.from_bytes(buf[p:p+n],"big")
    if not is_id:
        val &= (1<<(7*n))-1
        if val==(1<<(7*n))-1: val=None
    return val,n

def elem(buf,p,lim):
    eid,n=vint(buf,p,True); sz,m=vint(buf,p+n)
    start=p+n+m; end=lim if sz is None else start+sz
    if start>lim or end>lim or end<=p: raise ValueError("invalid EBML bounds")
    return eid,start,end,sz

def children(buf,a,b):
    while a<b:
        tag,start,end,sz=elem(buf,a,b)
        if sz is None: raise ValueError("unknown nested EBML size")
        yield tag,start,end
        a=end

def parse(buf):
    pos=0; segment=None
    while pos<len(buf):
        tag,a,b,sz=elem(buf,pos,len(buf))
        if tag==SEG: segment=(a,b); break
        pos=b
    if segment is None: raise ValueError("no Segment")
    pos,limit=segment; scale=1_000_000; tracks={}; packets=[]; clusters=0
    while pos<limit:
        tag,a,b,sz=elem(buf,pos,limit)
        if tag==INFO:
            for t,x,y in children(buf,a,b):
                if t==SCALE: scale=int.from_bytes(buf[x:y],"big")
        elif tag==TRACKS:
            for t,x,y in children(buf,a,b):
                if t!=ENTRY: continue
                track={}
                for q,c,d in children(buf,x,y):
                    if q==TNUM: track["id"]=int.from_bytes(buf[c:d],"big")
                    if q==TTYPE: track["type"]=int.from_bytes(buf[c:d],"big")
                if "id" in track: tracks[track["id"]]=track
        elif tag==CLUSTER:
            clusters+=1; q=a; stamp=None; blocks=[]; stop=b
            while q<stop:
                t,x,y,s=elem(buf,q,stop)
                if t==CLUSTER:
                    if sz is not None: raise ValueError("nested Cluster")
                    stop=q; break
                if s is None: raise ValueError("unknown child size")
                if t==CTIME: stamp=int.from_bytes(buf[x:y],"big")
                elif t==SIMPLE: blocks.append(buf[x:y])
                elif t==GROUP: blocks.extend(buf[c:d] for k,c,d in children(buf,x,y) if k==BLOCK)
                q=y
            if stamp is None: raise ValueError("Cluster time missing")
            for block in blocks:
                tr,n=vint(block,0)
                if tr is None or n+3>len(block): raise ValueError("invalid Block")
                relative=struct.unpack_from(">h",block,n)[0]
                packets.append((tr,(stamp+relative)*scale))
            pos=stop; continue
        pos=b
    video=[k for k,v in tracks.items() if v.get("type")==1]
    if len(video)!=1: raise ValueError("video track count")
    pts=[t for k,t in packets if k==video[0]]
    if not pts or any(t%1_000_000 for t in pts): raise ValueError("PTS unit")
    return [t//1_000_000 for t in pts],clusters

def audit(name,spec):
    data=original(spec); pts,clusters=parse(data)
    with tempfile.TemporaryDirectory() as temp:
        path=Path(temp)/"original.webm"; path.write_bytes(data)
        cp=subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
            "-show_entries","packet=pts_time","-of","json",str(path)],
            check=True,text=True,capture_output=True,timeout=120)
        probe=[int(Decimal(x["pts_time"])*1000) for x in json.loads(cp.stdout)["packets"]]
    return {"packets":len(pts),"distinct_pts":len(set(pts)),"clusters":clusters,
        "ordered_pts_equal_ffprobe":pts==probe,"ffprobe_packets":len(probe),
        "collision_fraction":(len(pts)-len(set(pts)))/len(pts),
        "crc_verified":True}

def main():
    rows={name:audit(name,spec) for name,spec in SPECS.items()}
    expect={"P_02_initial":(857,792),"P_02_final":(783,463),
            "P_06_initial":(687,382),"P_07_initial":(535,350)}
    gates={
        "G1_crc_all":all(x["crc_verified"] for x in rows.values()),
        "G2_full_ordered_pts_ffprobe":all(x["ordered_pts_equal_ffprobe"] for x in rows.values()),
        "G3_original_wolfram_counts":all((x["packets"],x["distinct_pts"])==expect[k] for k,x in rows.items()),
        "G4_within_session_reversal":rows["P_02_final"]["collision_fraction"]-rows["P_02_initial"]["collision_fraction"]>0.2}
    out={"experiment":"E002-084","rows":rows,"gates":gates,
         "overall":"PASS" if all(gates.values()) else "FAIL",
         "boundary":"PTS != exposure timestamps; no RGB/reference waveform or fatigue validity"}
    Path("e002_084_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    if not all(gates.values()): raise SystemExit(1)

if __name__=="__main__": main()
