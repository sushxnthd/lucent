"""E002-155: frozen human RGB-annotation aperture-reference audit. No tracker or fatigue labels."""
import collections,csv,hashlib,io,json,math,pathlib,random,re,tempfile,zipfile
import numpy as np
from PIL import Image
import requests

OUT=pathlib.Path("research/e002-155")
URL="https://zenodo.org/api/records/20492528"
EXPECTED="049df72454682c1c77c50c8236bb607919a6e333528bc2b89c567b625e459700"
LAGS=(1,5,15,30); T=-2*math.log(.95)
PAT=re.compile(r"^(?P<group>.+)_frame_(?P<frame>\d+)_pic_(?P<pic>\d+)$",re.I)

def mask_stats(data,name):
    m=PAT.match(pathlib.PurePosixPath(name).stem)
    if not m:return None,"unparsed"
    a=np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
    p=a[:,:,0]>=128; e=p|(a[:,:,1]>=128)
    P=int(p.sum()); E=int(e.sum())
    if P<16 or E<64:return None,"small_mask"
    q=math.sqrt(P/E)
    if not 0<q<.9:return None,"ratio"
    xx=np.nonzero(e)[1]; w=int(xx.max()-xx.min()+1)
    if w<8:return None,"width"
    return dict(group=m["group"].lower(),frame=int(m["frame"]),P=P,E=E,W=w,
                le=math.log(E),ld=math.log(E/w**2),lp=math.log(P/w**2),lq=math.log(q)),None

def quant(a,q):
    return float(np.quantile(a,q)) if a else None

def frac(rows,key):
    return sum(abs(r[key])>T for r in rows)/len(rows) if rows else None

def ci(rows):
    groups=collections.defaultdict(lambda:[0,0])
    for r in rows:
        x=groups[r["group"]];x[0]+=1;x[1]+=abs(r["dD"])>T
    keys=sorted(groups)
    if len(keys)<2:return None
    rng=random.Random(1552026); out=[]
    for _ in range(2000):
        draw=rng.choices(keys,k=len(keys))
        out.append(sum(groups[k][1] for k in draw)/sum(groups[k][0] for k in draw))
    return [quant(out,.025),quant(out,.975)]

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    result=dict(experiment="E002-155",status="NOT_EVALUABLE",threshold=T,
                claim_boundary="Original human annotated pupil and visible-eye masks; no anatomical iris, ordinary RGB segmenter, synchronized tracker or fatigue")
    try:
        s=requests.Session(); resp=s.get(URL,timeout=90);resp.raise_for_status()
        meta=resp.json()
        f=next(x for x in meta["files"] if x["key"]=="human_eyeregion_pupil_segmentation_dataset.zip")
        link=f["links"].get("self") or f["links"].get("download")
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/"data.zip";h=hashlib.sha256();m=hashlib.md5();n=0
            with s.get(link,stream=True,timeout=(40,180)) as resp:
                resp.raise_for_status()
                with p.open("wb") as dest:
                    for chunk in resp.iter_content(1048576):
                        if not chunk:continue
                        n+=len(chunk)
                        if n>200*1024**2:raise ValueError("archive cap")
                        h.update(chunk);m.update(chunk);dest.write(chunk)
            manifest=dict(record=URL,record_id=meta.get("id"),filename=f["key"],
                          bytes=n,sha256=h.hexdigest(),md5=m.hexdigest(),
                          upstream_checksum=f.get("checksum"),license=meta.get("metadata",{}).get("license"))
            (OUT/"DATA_MANIFEST.json").write_text(json.dumps(manifest,indent=2,default=str)+"\n")
            if h.hexdigest()!=EXPECTED:raise ValueError("pinned SHA256 mismatch")
            if f.get("checksum","").startswith("md5:") and m.hexdigest()!=f["checksum"][4:]:
                raise ValueError("upstream MD5 mismatch")
            groups=collections.defaultdict(lambda:collections.defaultdict(list))
            excluded=collections.Counter()
            with zipfile.ZipFile(p) as z:
                names=sorted(x for x in z.namelist() if "/annotation/png/" in x.lower() and x.lower().endswith(".png"))
                for name in names:
                    try: item,err=mask_stats(z.read(name),name)
                    except Exception as exc:item,err=None,"decode_"+type(exc).__name__
                    if err:excluded[err]+=1
                    else:groups[item["group"]][item["frame"]].append(item)
            rows=[];dup=0
            for group,frames in sorted(groups.items()):
                uniq={k:v[0] for k,v in frames.items() if len(v)==1}
                dup+=sum(len(v) for v in frames.values() if len(v)!=1)
                for i,a in sorted(uniq.items()):
                    for lag in LAGS:
                        if i+lag not in uniq:continue
                        b=uniq[i+lag]
                        de=b["le"]-a["le"];dd=b["ld"]-a["ld"]
                        dp=b["lp"]-a["lp"];dq=b["lq"]-a["lq"]
                        rows.append(dict(group=group,lag=lag,frame1=i,frame2=i+lag,
                                         dE=de,dD=dd,dPn=dp,dq=dq,
                                         residual=dq-(dp-dd)/2,
                                         direction="closing" if dd<0 else "opening",
                                         source_class="camera" if group.startswith("camera") else "eye_or_other"))
            cols=["group","lag","frame1","frame2","dE","dD","dPn","dq","residual","direction","source_class"]
            with (OUT/"PAIRS.csv").open("w",newline="") as fp:
                w=csv.DictWriter(fp,fieldnames=cols);w.writeheader();w.writerows(rows)
            summary={}
            for lag in LAGS:
                rr=[r for r in rows if r["lag"]==lag]
                summary[str(lag)]=dict(n_pairs=len(rr),n_groups=len({r["group"] for r in rr}),
                   fraction_scale_normalized=frac(rr,"dD"),fraction_raw=frac(rr,"dE"),
                   median_abs_dD=quant([abs(r["dD"]) for r in rr],.5),
                   p90_abs_dD=quant([abs(r["dD"]) for r in rr],.9),
                   p95_abs_dD=quant([abs(r["dD"]) for r in rr],.95),
                   cluster_ci95=ci(rr))
            a=summary["1"];b=summary["30"]
            residual=max((abs(r["residual"]) for r in rows),default=None)
            gates=dict(G0_access=a["n_pairs"]>=100 and a["n_groups"]>=10,
                G1_adjacent=(a["fraction_scale_normalized"]<=.05) if a["n_pairs"]>=100 else None,
                G2_lag30=(b["fraction_scale_normalized"]<=.05) if b["n_pairs"]>=100 else None,
                G3_cluster_upper=(a["cluster_ci95"][1]<=.05) if a["cluster_ci95"] else None,
                G4_identity=(residual<=1e-10) if residual is not None else None,
                G5_RGB_tracker_state="UNTESTED")
            sub={}
            for cls in ("camera","eye_or_other"):
                for d in ("closing","opening"):
                    rr=[r for r in rows if r["lag"]==1 and r["source_class"]==cls and r["direction"]==d]
                    sub[cls+"/"+d]=dict(n=len(rr),fraction=frac(rr,"dD"))
            extreme=sorted((r for r in rows if r["lag"]==1),key=lambda r:abs(r["dD"]),reverse=True)[:10]
            result.update(status="ORIGINAL_HUMAN_MASKS_SCORED",n_masks=len(names),
                n_filename_groups=len(groups),duplicate_index_rows=dup,exclusions=dict(excluded),
                summary=summary,gates=gates,max_identity_residual=residual,
                exploratory_subgroups=sub,exploratory_extremes=extreme)
    except Exception as exc:result["error"]=type(exc).__name__+": "+str(exc)
    (OUT/"RESULTS.json").write_text(json.dumps(result,indent=2,default=str)+"\n")
    sums=[]
    for name in ("DATA_MANIFEST.json","PAIRS.csv","RESULTS.json"):
        p=OUT/name
        if p.exists():sums.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+name)
    (OUT/"SHA256SUMS").write_text("\n".join(sums)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="exploratory_extremes"},indent=2,default=str))
    if result["status"]!="ORIGINAL_HUMAN_MASKS_SCORED":raise SystemExit(2)

if __name__=="__main__":main()
