#!/usr/bin/env python3
"""E002-217: read-only audit of the authors' publicly linked EyeDentify Kaggle release.
No human images or tracker samples are uploaded to GitHub.
"""
import collections, datetime, hashlib, io, json, os, pathlib, tempfile, urllib.error, urllib.request, zipfile

URL_META="https://www.kaggle.com/api/v1/datasets/view/vijuls/PupilDiameterDatasets"
URL_ARCHIVE="https://www.kaggle.com/api/v1/datasets/download/vijuls/PupilDiameterDatasets"
MAX_BYTES=370_000_000
OUT=pathlib.Path("research/e002-217/RELEASE_PROBE.json")
def digest(x): return hashlib.sha256(x).hexdigest()
def req(url):
    return urllib.request.Request(url,headers={"User-Agent":"Lucent-Research-Provenance/1.0","Accept":"application/json, application/zip, */*"})
def safe_error(e):
    return {"kind":type(e).__name__,"http_status":getattr(e,"code",None),"message":str(e)[:240]}
def inventory(z,level):
    names=z.namelist()
    ext=collections.Counter(pathlib.PurePosixPath(n).suffix.lower() for n in names if not n.endswith("/"))
    candidates=[n for n in names if any(s in n.lower() for s in ["tobii","timestamp","session_data","pupil"]) and not n.endswith("/")]
    sample_csv=[]
    for name in names:
        if len(sample_csv)>=5: break
        info=z.getinfo(name)
        if pathlib.PurePosixPath(name).suffix.lower()==".csv" and info.file_size<2_000_000:
            try:
                with z.open(name) as f:
                    header=f.readline(4096).decode("utf-8-sig",errors="replace").strip()
                sample_csv.append({"path":name,"header":header[:600]})
            except Exception as e: sample_csv.append({"path":name,"error":str(e)[:100]})
    return {"level":level,"members":len(names),"extensions":dict(sorted(ext.items())),
            "candidate_paths":candidates[:40],"sample_csv_headers":sample_csv,
            "zip_member_crc_not_cryptographic_hash":True,
            "nested_archives":[{"path":i.filename,"bytes":i.file_size} for i in z.infolist() if i.filename.lower().endswith(".zip")][:20]}
def run():
    out={"run":"E002-217","utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source":"author-linked Kaggle vijuls/PupilDiameterDatasets",
        "metadata_url":URL_META,"archive_url":URL_ARCHIVE,
        "max_bytes":MAX_BYTES,"metadata":{},"archive":{},
        "native_tracker_and_frame_timestamps_verified":False,
        "paired_native_rgb_reference_certified":False,
        "human_waveform_evaluated":False}
    try:
        with urllib.request.urlopen(req(URL_META),timeout=30) as f: b=f.read(5_000_001)
        if len(b)>5_000_000: raise ValueError("metadata too large")
        j=json.loads(b)
        out["metadata"]={"status":"ok","sha256":digest(b),"top_level_keys":sorted(j.keys()),"key_shapes":{k:(len(v) if isinstance(v,(list,dict)) else type(v).__name__) for k,v in j.items()},
            "title":j.get("title"),"totalBytes":j.get("totalBytes"),"lastUpdated":j.get("lastUpdated"),
            "resources":[{"name":x.get("name"),"totalBytes":x.get("totalBytes"),"size":x.get("size")} for x in j.get("resources",[])][:100]}
    except Exception as e:
        out["metadata"]={"status":"blocked","error":safe_error(e)}
    try:
        with urllib.request.urlopen(req(URL_ARCHIVE),timeout=50) as r:
            length=r.headers.get("Content-Length")
            ctype=r.headers.get("Content-Type","")
            if length and int(length)>MAX_BYTES: raise ValueError("archive exceeds bounded download size")
            h=hashlib.sha256()
            with tempfile.TemporaryFile() as f:
                total=0
                while True:
                    b=r.read(1024*1024)
                    if not b: break
                    total+=len(b)
                    if total>MAX_BYTES: raise ValueError("archive exceeded 370 MB cap")
                    h.update(b);f.write(b)
                f.seek(0)
                if not zipfile.is_zipfile(f): raise ValueError("download not ZIP")
                with zipfile.ZipFile(f) as z:
                    inv=inventory(z,"outer")
                    # Inspect at most one nested archive; no human pixels are decoded.
                    nested=[i for i in z.infolist() if i.filename.lower().endswith(".zip") and i.file_size<=MAX_BYTES]
                    if nested:
                        with tempfile.TemporaryFile() as nf:
                            with z.open(nested[0]) as src:
                                while True:
                                    chunk=src.read(1024*1024)
                                    if not chunk: break
                                    nf.write(chunk)
                            nf.seek(0)
                            if zipfile.is_zipfile(nf):
                                with zipfile.ZipFile(nf) as inner:
                                    inv["first_nested_inventory"]=inventory(inner,"nested")
                out["archive"]={"status":"inspected","bytes":total,"sha256":h.hexdigest(),
                    "content_type":ctype,"inventory":inv}
    except Exception as e:
        out["archive"]={"status":"blocked","error":safe_error(e)}
    # A file-name inventory cannot establish timestamp alignment or raw-tracker lineage.
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"metadata_status":out["metadata"]["status"],
                      "archive_status":out["archive"]["status"],
                      "archive_bytes":out["archive"].get("bytes"),
                      "native_pair_certified":False},sort_keys=True))
if __name__=="__main__": run()
