# E002-121 original human RGB annotated-mask spatial ceiling
import io,os,json,hashlib,zipfile,math,tempfile,pathlib,time,collections
import numpy as np
from PIL import Image
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
def one(z,item):
    name,mask=item
    a=np.asarray(Image.open(io.BytesIO(z.read(mask))).convert("RGB"))
    p=a[:,:,0]>=128;e=p|(a[:,:,1]>=128)
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
        with z.open(name) as f:im=Image.open(io.BytesIO(f.read()));im.verify()
    except Exception:return None,"image_decode"
    out={"q":q,"pupil_px":npix,"eye_px":neye,"path":name}
    for size in SIZES:
        vals=np.asarray([metric(p,e,box,size,shift) for shift in SHIFTS])
        if not np.isfinite(vals).all():return None,"zero_lowres"
        key="%dx%d"%size
        out[key]={"soft_error":float(np.mean(abs(vals[:,0]-q))),"hard_error":float(np.mean(abs(vals[:,1]-q))),"soft_range":float(np.ptp(vals[:,0])),"hard_range":float(np.ptp(vals[:,1]))}
    return out,None
def ci(a,seed):
    a=np.asarray(a);rng=np.random.default_rng(seed)
    boots=np.median(a[rng.integers(len(a),size=(1000,len(a)))],axis=1)
    return np.quantile(boots,[.025,.975]).tolist()
def summary(rows):
    out={}
    for w,h in SIZES:
        key=f"{w}x{h}";out[key]={}
        for m in ("soft_error","hard_error","soft_range","hard_range"):
            v=np.asarray([r[key][m] for r in rows]);out[key][m]={"median":float(np.median(v)),"p90":float(np.quantile(v,.9))}
        delta=np.asarray([r[key]["soft_error"]-r[key]["hard_error"] for r in rows])
        out[key]["soft_beats_hard_fraction"]=float(np.mean(delta<0))
        out[key]["median_error_delta_ci95"]=ci(delta,1212026)
    a,b,c=[out[f"{w}x{h}"] for w,h in SIZES]
    out["gates"]={
       "G0_access":len(rows)>=100,
       "G1_32x16":a["soft_error"]["median"]<=.5*a["hard_error"]["median"] and a["soft_range"]["median"]<=.5*a["hard_range"]["median"],
       "G2_generality":b["soft_error"]["median"]<b["hard_error"]["median"] and c["soft_error"]["median"]<c["hard_error"]["median"] and a["soft_beats_hard_fraction"]>.7,
       "G3_waveform_state":"UNTESTED"}
    return out
def run():
    result={"experiment":"E002-121","status":"NOT_EVALUABLE","dataset":URL,"claim_boundary":"Original human RGB annotations only; no paired tracker waveform, no RGB segmenter, no behavioral state"}
    try:
        session=requests.Session()
        r=session.get(URL,timeout=90);r.raise_for_status();meta=r.json()
        files=meta.get("files",[])
        result["record"]={"id":meta.get("id"),"title":meta.get("metadata",{}).get("title"),"license":meta.get("metadata",{}).get("license"),"files":[{"key":f.get("key"),"size":f.get("size"),"checksum":f.get("checksum")} for f in files]}
        cand=[f for f in files if f.get("key","").lower().endswith(".zip") and 0<f.get("size",0)<=200*1024**2]
        if not cand:raise RuntimeError("No eligible public ZIP <=200MB")
        f=max(cand,key=lambda x:x["size"])
        link=f.get("links",{}).get("self") or f.get("links",{}).get("download")
        if not link:raise RuntimeError("Missing public file link")
        with tempfile.TemporaryDirectory() as td:
            path=os.path.join(td,"source.zip");md5=hashlib.md5();sha=hashlib.sha256();total=0
            with session.get(link,stream=True,timeout=(40,150)) as res:
                res.raise_for_status()
                with open(path,"wb") as dest:
                    for chunk in res.iter_content(1024*1024):
                        if not chunk:continue
                        total+=len(chunk)
                        if total>200*1024**2:raise RuntimeError("Download exceeded size cap")
                        md5.update(chunk);sha.update(chunk);dest.write(chunk)
            result["archive"]={"filename":f["key"],"bytes":total,"sha256":sha.hexdigest(),"md5":md5.hexdigest()}
            if str(f.get("checksum","")).startswith("md5:") and f["checksum"][4:]!=md5.hexdigest():raise RuntimeError("Archive MD5 mismatch")
            with zipfile.ZipFile(path) as z:
                bad=z.testzip()
                if bad:raise RuntimeError("Archive CRC failure: "+bad)
                names=z.namelist();items,inv=pairs(names);result["inventory"]=inv
                result["csv_files"]=[s for s in names if s.lower().endswith(".csv")][:12]
                if len(items)<100:raise RuntimeError("Insufficient matched RGB/mask pairs")
                items.sort(key=lambda item:hashlib.sha256(item[0].encode()).hexdigest())
                rows=[];excl=collections.Counter()
                for item in items:
                    row,reason=one(z,item)
                    if row is None:excl[reason]+=1
                    else:rows.append(row)
                    if len(rows)>=480:break
                result["n_scored"]=len(rows);result["excluded"]=dict(excl)
                if len(rows)<100:raise RuntimeError("Insufficient eligible pairs after filters")
                result["summary"]=summary(rows)
                result["sample_sha256"]=hashlib.sha256("\n".join(r["path"] for r in rows).encode()).hexdigest()
                result["status"]="ORACLE_MASK_SPATIAL_CEILING_SCORED"
    except Exception as e:
        result["error"]=f"{type(e).__name__}: {e}"
    out=pathlib.Path("research/e002-121/RESULTS.json");out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps(result,indent=2,default=str)[:25000])
if __name__=="__main__":run()
