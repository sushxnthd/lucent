# E002-121 original human RGB annotated-mask spatial ceiling
import io,os,json,hashlib,zipfile,math,tempfile,pathlib,time,collections
import numpy as np
from PIL import Image, ImageFilter
import requests
URL="https://zenodo.org/api/records/20492528"
SIZES=[(32,16),(64,32),(128,64)]
SHIFTS=[0,.25,.5,.75]
def stem(s):
    x=pathlib.PurePosixPath(s).stem.lower()
    for suf in ("_mask","_segmentation","_label","_gt"):
        if x.endswith(suf):x=x[:-len(suf)]
    return x
def pairs(names):
    jpg=[s for s in names if s.lower().endswith((".jpg",".jpeg"))]
    png=[s for s in names if s.lower().endswith(".png")]
    lookup=collections.defaultdict(list)
    for s in png:lookup[stem(s)].append(s)
    out=[(s,lookup[stem(s)][0]) for s in jpg if len(lookup[stem(s)])==1]
    return out,{"jpg":len(jpg),"png":len(png),"matched":len(out),"examples":out[:5]}
def metric(p,e,box,size,shift):
    w,h=size;x0,y0,x1,y1=box
    sx=round(shift*(x1-x0)/w);sy=round(shift*(y1-y0)/h)
    box=(x0+sx,y0+sy,x1+sx,y1+sy)
    pp=np.asarray(Image.fromarray(p.astype("uint8")*255).crop(box).resize(size,Image.Resampling.BOX),float)/255
    ee=np.asarray(Image.fromarray(e.astype("uint8")*255).crop(box).resize(size,Image.Resampling.BOX),float)/255
    return math.sqrt(pp.sum()/ee.sum()) if ee.sum()>0 else np.nan, math.sqrt((pp>=.5).sum()/(ee>=.5).sum()) if (ee>=.5).sum()>0 else np.nan

EXPECTED_ARCHIVE_SHA256="049df72454682c1c77c50c8236bb607919a6e333528bc2b89c567b625e459700"
EXPECTED_FIRST480_SHA256="a0d3af5426ce91b1550cba114bf53d8cc5ad8d5635251cc0492a1e8ddefbc322"
CONDITIONS=("oracle","erode1","dilate1","erode3","dilate3")
def source_label(path):
    import re
    s=pathlib.PurePosixPath(path).stem.lower()
    m=re.match(r"(eye\s+\d+|camera\d+_\d{8}_\d+)",s)
    return m.group(1) if m else s.split("_frame_")[0][:64]
def masks_and_box(z,item):
    name,mask=item
    a=np.asarray(Image.open(io.BytesIO(z.read(mask))).convert("RGB"))
    p=a[:,:,0]>=128
    e=p|(a[:,:,1]>=128)
    npix=int(p.sum());neye=int(e.sum())
    if npix<16 or neye<64:return None,"small_mask"
    q=math.sqrt(npix/neye)
    if not 0<q<.9:return None,"invalid_ratio"
    yy,xx=np.nonzero(e);xlo,xhi=xx.min(),xx.max()+1;ylo,yhi=yy.min(),yy.max()+1
    pad=.25*max(xhi-xlo,yhi-ylo)
    width=max(xhi-xlo+2*pad,2*(yhi-ylo+2*pad))
    cx=(xlo+xhi)/2;cy=(ylo+yhi)/2
    box=tuple(round(v) for v in (cx-width/2,cy-width/4,cx+width/2,cy+width/4))
    x0,y0,x1,y1=box
    if e[max(0,y0):min(e.shape[0],y1),max(0,x0):min(e.shape[1],x1)].sum()/neye<.995:return None,"clipped"
    try:
        with z.open(name) as f:
            im=Image.open(io.BytesIO(f.read()))
            im.verify()
    except Exception:return None,"image_decode"
    # The original E002-121 filters also reject any zero-denominator low-res condition.
    for size in SIZES:
        vals=np.asarray([metric(p,e,box,size,shift) for shift in SHIFTS])
        if not np.isfinite(vals).all():return None,"zero_lowres"
    return (p,e,box,q,{"pupil_px":npix,"eye_px":neye,
       "red_pixels":int((a[:,:,0]>=128).sum()),"green_pixels":int((a[:,:,1]>=128).sum()),
       "blue_pixels":int((a[:,:,2]>=128).sum()),
       "red_green_overlap":int(((a[:,:,0]>=128)&(a[:,:,1]>=128)).sum())}),None
def perturb(p,e,kind):
    if kind=="oracle":return p
    rad=1 if kind.endswith("1") else 3
    filt=ImageFilter.MinFilter(2*rad+1) if kind.startswith("erode") else ImageFilter.MaxFilter(2*rad+1)
    out=np.asarray(Image.fromarray(p.astype("uint8")*255).filter(filt))>=128
    return out & e
def score(p,e,box,q):
    out={}
    for cond in CONDITIONS:
        pp=perturb(p,e,cond)
        out[cond]={}
        for size in SIZES:
            key="%dx%d"%size
            v=np.asarray([metric(pp,e,box,size,shift) for shift in SHIFTS])
            if not np.isfinite(v).all():
                out[cond][key]={"soft":float("nan"),"hard":float("nan")}
            else:
                out[cond][key]={"soft":float(np.mean(abs(v[:,0]-q))),
                                 "hard":float(np.mean(abs(v[:,1]-q)))}
    return out
def bootstrap_ci(values,seed=1222026):
    a=np.asarray(values,float);a=a[np.isfinite(a)]
    if len(a)==0:return None
    rng=np.random.default_rng(seed)
    # 500 image-level bootstrap resamples; do not interpret as participant-clustered.
    vals=np.median(a[rng.integers(0,len(a),size=(500,len(a)))],axis=1)
    return [float(v) for v in np.quantile(vals,[.025,.975])]
def summarize(rows):
    out={}
    for size in SIZES:
        key="%dx%d"%size
        out[key]={}
        for cond in CONDITIONS:
            a=np.asarray([r["scores"][cond][key]["soft"] for r in rows],float)
            b=np.asarray([r["scores"][cond][key]["hard"] for r in rows],float)
            valid=np.isfinite(a)&np.isfinite(b)
            out[key][cond]={
                "n_valid":int(valid.sum()),
                "median_soft_error":float(np.median(a[valid])) if valid.any() else None,
                "median_hard_error":float(np.median(b[valid])) if valid.any() else None,
                "soft_beats_hard_fraction":float(np.mean(a[valid]<b[valid])) if valid.any() else None,
                "median_soft_minus_hard_ci95":bootstrap_ci(a[valid]-b[valid]),
            }
        for cond in ("erode1","dilate1","erode3","dilate3"):
            a=np.asarray([r["scores"][cond][key]["soft"] for r in rows])
            b=np.asarray([r["scores"]["oracle"][key]["soft"] for r in rows])
            v=np.isfinite(a)&np.isfinite(b)
            out[key][cond]["median_perturb_minus_oracle_soft"]=float(np.median(a[v]-b[v])) if v.any() else None
    o=out["128x64"]
    pooled=np.asarray([r["scores"][cond]["128x64"]["soft"] for r in rows for cond in ("erode1","dilate1")])
    pooled=pooled[np.isfinite(pooled)]
    oracle=np.asarray([r["scores"]["oracle"]["128x64"]["soft"] for r in rows])
    gates={
       "G0":len(rows)>=300,
       "G1":all(out[f"{w}x{h}"]["oracle"]["median_soft_error"]<out[f"{w}x{h}"]["oracle"]["median_hard_error"] for w,h in SIZES),
       "G2":bool(np.median(pooled)>np.median(oracle)),
       "G3":"NOT_EVALUABLE_NO_RGB_SEGMENTER_TRACKER_OR_STATE"}
    out["pooled_1px_128x64_median_soft_error"]=float(np.median(pooled))
    out["gates"]=gates
    return out
def run():
    result={"experiment":"E002-122","status":"NOT_EVALUABLE","protocol":"research/e002-122/FROZEN_PROTOCOL.md",
        "dataset":URL,"scope":"original human annotated masks only; image-disjoint not participant-disjoint"}
    try:
        session=requests.Session()
        r=session.get(URL,timeout=90);r.raise_for_status();meta=r.json()
        files=meta.get("files",[])
        cand=[f for f in files if f.get("key","").lower().endswith(".zip") and 0<f.get("size",0)<=200*1024**2]
        if not cand:raise RuntimeError("No eligible public ZIP <=200MB")
        f=max(cand,key=lambda x:x["size"])
        link=f.get("links",{}).get("self") or f.get("links",{}).get("download")
        with tempfile.TemporaryDirectory() as td:
            path=os.path.join(td,"source.zip");md5=hashlib.md5();sha=hashlib.sha256();total=0
            with session.get(link,stream=True,timeout=(40,150)) as res:
                res.raise_for_status()
                with open(path,"wb") as dest:
                    for chunk in res.iter_content(1024*1024):
                        if not chunk:continue
                        total+=len(chunk)
                        if total>200*1024**2:raise RuntimeError("Download size cap")
                        md5.update(chunk);sha.update(chunk);dest.write(chunk)
            result["archive"]={"filename":f["key"],"bytes":total,"sha256":sha.hexdigest(),"md5":md5.hexdigest()}
            if sha.hexdigest()!=EXPECTED_ARCHIVE_SHA256:raise RuntimeError("Archive SHA256 differs from E002-121")
            if str(f.get("checksum","")).startswith("md5:") and f["checksum"][4:]!=md5.hexdigest():raise RuntimeError("MD5 mismatch")
            with zipfile.ZipFile(path) as z:
                bad=z.testzip()
                if bad:raise RuntimeError("ZIP CRC failure "+bad)
                items,inventory=pairs(z.namelist());result["inventory"]=inventory
                items.sort(key=lambda item:hashlib.sha256(item[0].encode()).hexdigest())
                first=[];rows=[];excl=collections.Counter();prefix_first=collections.Counter();prefix_new=collections.Counter()
                checked=0
                for item in items:
                    checked+=1
                    obj,reason=masks_and_box(z,item)
                    if reason:
                        excl[reason]+=1
                        continue
                    if len(first)<480:
                        first.append(item[0]);prefix_first[source_label(item[0])]+=1
                        continue
                    p,e,box,q,maskstats=obj
                    scores=score(p,e,box,q)
                    rows.append({"path":item[0],"source":source_label(item[0]),
                                 "pupil_px":maskstats["pupil_px"],"eye_px":maskstats["eye_px"],
                                 "mask_stats":maskstats,"scores":scores})
                    prefix_new[source_label(item[0])]+=1
                    if len(rows)>=480:break
                first_hash=hashlib.sha256("\n".join(first).encode()).hexdigest()
                result["first480_hash"]=first_hash
                result["first480_matches_e002121"]=first_hash==EXPECTED_FIRST480_SHA256
                result["holdout_path_overlap"]=len(set(first)&set(r["path"] for r in rows))
                result["n_scored"]=len(rows);result["checked"]=checked;result["excluded"]=dict(excl)
                result["holdout_sha256"]=hashlib.sha256("\n".join(r["path"] for r in rows).encode()).hexdigest()
                result["source_overlap_count"]=len(set(prefix_first)&set(prefix_new))
                result["source_prefix_first480"]=prefix_first.most_common(20)
                result["source_prefix_holdout"]=prefix_new.most_common(20)
                result["mask_channel_stats"]={k:float(np.median([r["mask_stats"][k] for r in rows])) for k in
                   ("red_pixels","green_pixels","blue_pixels","red_green_overlap")}
                result["summary"]=summarize(rows)
                if not result["first480_matches_e002121"]:result["summary"]["gates"]["G0"]=False
                if result["holdout_path_overlap"]!=0:result["summary"]["gates"]["G0"]=False
                for size in ("32x16","64x32","128x64"):
                    exceptions=[r for r in rows if r["scores"]["oracle"][size]["soft"]>=r["scores"]["oracle"][size]["hard"]]
                    result.setdefault("exceptions",{})[size]={
                        "n":len(exceptions),
                        "median_pupil_px":float(np.median([r["pupil_px"] for r in exceptions])) if exceptions else None,
                        "examples":[r["path"] for r in exceptions[:8]]}
                result["status"]="ORIGINAL_HUMAN_ORACLE_MASK_HOLDOUT_SCORED"
    except Exception as exc:
        result["error"]=type(exc).__name__+": "+str(exc)
    out=pathlib.Path("research/e002-122/RESULTS.json");out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,allow_nan=False)[:24000])
    if "error" in result:raise SystemExit(1)
if __name__=="__main__":run()
