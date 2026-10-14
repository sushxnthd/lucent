#!/usr/bin/env python3
"""Bounded public ZIP central-directory provenance check. No original face media downloaded."""
import json,hashlib,struct,re,urllib.request
from pathlib import Path
URL="https://webgazer.cs.brown.edu/data/WebGazerETRA2018Dataset_Release20180420.zip"
out={"run":"E002-184","source":URL,"status":"BLOCKED","requests":[],"human_waveform_evaluated":False}
def request(spec):
    req=urllib.request.Request(URL,headers={"Range":spec,"User-Agent":"Lucent-public-provenance/1.0"})
    with urllib.request.urlopen(req,timeout=35) as r:
        headers={k.lower():v for k,v in r.headers.items()}
        out["requests"].append({"range":spec,"status":r.status,"content_range":headers.get("content-range"),"content_length":headers.get("content-length")})
        if r.status!=206:raise ValueError("HTTP_RANGE_UNSUPPORTED")
        m=re.fullmatch(r"bytes (\\d+)-(\\d+)/(\\d+)",headers.get("content-range",""))
        if not m:raise ValueError("CONTENT_RANGE_INVALID")
        a,b,total=map(int,m.groups())
        if b-a+1>8*1024*1024:raise ValueError("RANGE_TOO_LARGE")
        body=r.read(8*1024*1024+1)
        if len(body)!=b-a+1:raise ValueError("TRUNCATED")
        return body,total
try:
    prefix,total=request("bytes=0-15")
    if not prefix.startswith(b"PK"):raise ValueError("NOT_ZIP")
    tail,n=request("bytes=-65557")
    if n!=total:raise ValueError("LENGTH_CHANGED")
    pos=tail.rfind(b"PK\\x05\\x06")
    if pos<0:raise ValueError("ZIP_EOCD_MISSING")
    fields=struct.unpack_from("<IHHHHIIH",tail,pos)
    _,disk,cdisk,n_this,n_total,cd_size,cd_off,comment=fields
    if disk or cdisk or n_this!=n_total or cd_size>8*1024*1024:raise ValueError("ZIP_UNSUPPORTED")
    if cd_off==0xffffffff or cd_size==0xffffffff:raise ValueError("ZIP64_NEEDS_FOLLOWUP")
    directory,n=request(f"bytes={cd_off}-{cd_off+cd_size-1}")
    if n!=total:raise ValueError("LENGTH_CHANGED")
    out["central_directory_sha256"]=hashlib.sha256(directory).hexdigest()
    names=[];i=0
    while i<len(directory):
        if directory[i:i+4]!=b"PK\\x01\\x02":raise ValueError("BAD_CENTRAL_DIRECTORY")
        a,b,c=struct.unpack_from("<HHH",directory,i+28)
        names.append(directory[i+46:i+46+a].decode("utf8","replace"))
        i+=46+a+b+c
    people={}
    for name in names:
        match=re.search(r"(?:^|/)(P_\\d+)/([^/]+)$",name)
        if not match:continue
        p,f=match.groups()
        d=people.setdefault(p,{"webcam":0,"tobii":0,"event":0})
        if re.search(r"\\.(mp4|webm)$",f,re.I) and re.search(r"[-_](?:study|dot|typing|reading|point|search)",f,re.I):d["webcam"]+=1
        if f==p+".txt":d["tobii"]+=1
        if re.fullmatch(r"\\d{13}\\.(txt|json)",f):d["event"]+=1
    out.update({"status":"INDEX_VERIFIED","zip_size":total,"zip_members":len(names),"participants":len(people),"complete_triplets":sum(all(v.values()) for v in people.values()),"counts":people})
except Exception as exc:
    out.update({"status":"ACCESS_OR_FORMAT_BLOCKED","error_type":type(exc).__name__,"error":str(exc)[:300]})
Path("research/e002-184/probe_results.json").write_text(json.dumps(out,sort_keys=True,indent=2)+"\\n")
print(json.dumps(out,sort_keys=True))
