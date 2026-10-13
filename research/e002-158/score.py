import io,math,pathlib,re,numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation,gaussian_filter
from auc import auc
PAT=re.compile(r"(.+)_frame_(\d+)_pic_(\d+)$",re.I)
def score(jpg,png,path,i):
 rgb=np.asarray(Image.open(io.BytesIO(jpg)).convert("RGB"),dtype=float)/255
 mask=np.asarray(Image.open(io.BytesIO(png)).convert("RGB"))
 if rgb.shape!=mask.shape:return None,"shape"
 p=mask[:,:,0]>=128;e=p|(mask[:,:,1]>=128)
 if p.sum()<16 or e.sum()<64 or not 0<math.sqrt(p.sum()/e.sum())<.9:return None,"mask"
 ring=binary_dilation(p,iterations=4)&~p&e
 if ring.sum()<16:return None,"ring"
 y=rgb[:,:,0]*.2126+rgb[:,:,1]*.7152+rgb[:,:,2]*.0722
 s={"lum":-y,"red":-rgb[:,:,0],"green":-rgb[:,:,1],"blue":-rgb[:,:,2],
 "highpass":-(y-gaussian_filter(y,5))}
 g=PAT.match(pathlib.PurePosixPath(path).stem)
 row={"path":path,"group":g.group(1).lower() if g else "unknown","brightness":float(np.median(y[e]))}
 for k,v in s.items():row["auc_"+k]=auc(v[p],v[ring])
 vals=np.r_[(-y)[p],(-y)[ring]]
 labels=np.r_[np.ones(int(p.sum()),bool),np.zeros(int(ring.sum()),bool)]
 np.random.default_rng(1582026+i).shuffle(labels)
 row["auc_placebo"]=auc(vals[labels],vals[~labels])
 return row,None
