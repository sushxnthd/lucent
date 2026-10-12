# E002-144: execute E002-141 frozen MEYELens original-image holdout.
import csv,hashlib,io,json,sys,zipfile
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
H=(5,10,15,20,25)
S=((128,64),(64,32),(32,16),(16,8))
A="32ebe8e393eda64b1c9fbdbc7048578388a188a317ddb4e57d0e1f7190d266e6"
def sample(rows):
 return rows if len(rows)<=24 else [rows[round(i*(len(rows)-1)/23)] for i in range(24)]
def med(x):return float(np.median(x)) if x else None
def feat(z,ip,mp,size):
 im=Image.open(io.BytesIO(z.read(ip))).convert("RGB")
 m=np.asarray(Image.open(io.BytesIO(z.read(mp))).convert("RGB"))
 if m.shape[:2]!=im.size[::-1]:raise ValueError("size")
 p=m[:,:,0]>127;e=m[:,:,1]>127
 if not p.any() or not e.any():return None
 y,x=np.where(p|e);x0,x1=x.min(),x.max()+1;y0,y1=y.min(),y.max()+1
 dx=max(1,round((x1-x0)*.1));dy=max(1,round((y1-y0)*.1))
 box=(max(0,x0-dx),max(0,y0-dy),min(im.width,x1+dx),min(im.height,y1+dy))
 def mask(a):return Image.fromarray((a[box[1]:box[3],box[0]:box[2]]*255).astype("uint8"))
 pm=mask(p);em=mask(e);rgb=im.crop(box)
 def rs(a,method):return np.asarray(a.resize(size,method),dtype=float)/255
 pn,en=rs(pm,Image.Resampling.NEAREST),rs(em,Image.Resampling.NEAREST)
 pb,eb=rs(pm,Image.Resampling.BOX),rs(em,Image.Resampling.BOX)
 lum=np.asarray(rgb.resize(size,Image.Resampling.BOX),dtype=float)/255@np.array([.2126,.7152,.0722])
 eye=eb>.5;norm=np.full(lum.shape,np.nan)
 if eye.any():
  lo,hi=np.percentile(lum[eye],[5,95])
  if hi-lo>=.01:norm=np.clip((lum-lo)/(hi-lo),0,1)
 return dict(gt=float(p.sum()/e.sum()),nn=float(pn.sum()/en.sum()) if en.sum() else None,
  box=float(pb.sum()/eb.sum()) if eb.sum() else None,zero=bool(pn.sum()==0),
  eye=eye,ebox=eb,truth=pb>.5,raw=lum,norm=norm)
def pred(f,mode,t):
 a=f[mode]
 if not np.isfinite(a).all() or not f["eye"].any():return None
 p=(a<=t)&f["eye"];g=f["truth"];d=p.sum()+g.sum()
 return (float(2*(p&g).sum()/d) if d else 1.,float(abs((p.sum()/f["ebox"].sum())/f["gt"]-1)))
def score(fs,mode,t):
 nn=[];box=[];dice=[];err=[]
 for f in fs:
  if f["nn"] is not None:nn.append(abs(f["nn"]/f["gt"]-1))
  if f["box"] is not None:box.append(abs(f["box"]/f["gt"]-1))
  q=pred(f,mode,t)
  if q:dice.append(q[0]);err.append(q[1])
 return dict(n=len(fs),nn_median=med(nn),box_median=med(box),
  nn_p90=float(np.quantile(nn,.9)) if nn else None,
  box_p90=float(np.quantile(box,.9)) if box else None,
  threshold_dice_median=med(dice),threshold_area_error_median=med(err),
  threshold_valid=len(dice),zero_nn_fraction=float(np.mean([f["zero"] for f in fs])) if fs else None)
def run(path):
 b=Path(path).read_bytes();out=dict(archive_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),
  protocol="E002-141 FROZEN",source="Zenodo 20492528",participant_disjoint=False,
  timebase_validity=False,state_validity=False)
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  names=z.namelist();csvs=[n for n in names if n.endswith("/annotation/annotations.csv")]
  assert len(csvs)==1
  raw=z.read(csvs[0]);out["annotations_sha256"]=hashlib.sha256(raw).hexdigest()
  assert out["annotations_sha256"]==A
  seq=defaultdict(list)
  for r in csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))):
   if float(r["eye_area"])>0 and float(r["pupil_area"])>0:seq[r["filename"].split("_frame_")[0]].append(r)
  keys=sorted(seq);assert len(keys)==26
  ims=defaultdict(list);masks=defaultdict(list)
  for n in names:
   if "/fullFrames/" in n and n.lower().endswith((".jpg",".jpeg")):ims[Path(n).stem].append(n)
   if "/annotation/png/" in n and n.lower().endswith(".png"):masks[Path(n).stem].append(n)
  out["selected_sequences"]=[keys[i] for i in (0,*H)]
  records={};errors={}
  for k in out["selected_sequences"]:
   records[k]=[];errors[k]=[]
   for r in sample(sorted(seq[k],key=lambda x:x["filename"])):
    stem=Path(r["filename"]).stem
    if len(ims[stem])!=1 or len(masks[stem])!=1:
     errors[k].append("missing/ambiguous:"+stem);continue
    records[k].append((ims[stem][0],masks[stem][0]))
  out["matched_counts"]={k:len(v) for k,v in records.items()}
  out["errors"]=errors
  g0=sum(len(records[keys[i]])>=10 for i in H)>=3
  out["gates"]={"G0":g0,"G5":"NOT_EVALUABLE"}
  if not g0:return out
  dev=[feat(z,*v,(64,32)) for v in records[keys[0]]]
  dev=[x for x in dev if x]
  thresholds={}
  for mode in ("norm","raw"):
   opts=[]
   for t in np.linspace(0,1,21):
    q=[pred(f,mode,float(t)) for f in dev];v=[x[0] for x in q if x]
    opts.append((float(np.mean(v)) if v else -1.,float(t)))
   best=max(v for v,t in opts)
   thresholds[mode]=min(t for v,t in opts if np.isclose(v,best))
  out["development_thresholds"]=thresholds;out["holdout"]={}
  for i in H:
   k=keys[i];out["holdout"][k]={}
   for size in S:
    fs=[feat(z,*v,size) for v in records[k]];fs=[x for x in fs if x]
    out["holdout"][k][f"{size[0]}x{size[1]}"]={m:score(fs,m,t) for m,t in thresholds.items()}
  h=list(out["holdout"].values())
  out["gates"].update(G1=sum(x["32x16"]["norm"]["box_median"] is not None and x["32x16"]["norm"]["box_median"]<=.05 for x in h)>=4,
   G2=sum(x["16x8"]["norm"]["nn_median"] is not None and x["16x8"]["norm"]["box_median"] is not None and x["16x8"]["norm"]["nn_median"]>x["16x8"]["norm"]["box_median"] for x in h)>=4,
   G3=sum(x["64x32"]["norm"]["threshold_dice_median"] is not None and x["64x32"]["norm"]["threshold_dice_median"]>=.5 for x in h)>=3,
   G4=sum(x["32x16"]["norm"]["threshold_area_error_median"] is not None and x["32x16"]["norm"]["threshold_area_error_median"]<=.25 for x in h)>=3)
  return out
if __name__=="__main__":
 result=run(sys.argv[1]);open("e002_144_results.json","w").write(json.dumps(result,indent=2))
 print(json.dumps({"gates":result["gates"],"matched":result["matched_counts"],
  "thresholds":result.get("development_thresholds")},indent=2))
