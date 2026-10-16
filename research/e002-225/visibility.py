#!/usr/bin/env python3
"""E002-225: bounded human RGB visibility preflight; NO waveform or lag claim."""
import csv, hashlib, json, math, subprocess, tempfile
from pathlib import Path
import cv2, mediapipe as mp, numpy as np

OUT=Path("research/e002-225")
OUT.mkdir(parents=True,exist_ok=True)
PINS={
"P_33":{"video":"edd83fd16806778ffe6565e5f2311a5dac17909edbfb603576d0b5448ec487d8","tracker":"3536d3d41ff8b2356fc35ce7f985c2000d671137ed33b8207669c72ca607265d","events":"8d05ddea2108fafb836aa1f26c3f40be0e0d9562e3183d3c93ce6fefb451cc62"},
"P_54":{"video":"dcfaa40b4c80b0c5a0c09a993d3d203ff33bed760a12ba0801e0db383a620869","tracker":"359838799cd8f02aab75e14f18ad571a33827165cf446558854462bea660e8f5","events":"f03b60c1ceab65794de07a205b9f1c405dc2d16aa7f29e850974819237369937"}}

def digest(path):
 h=hashlib.sha256()
 with open(path,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest()

def median(v):
 v=[float(x) for x in v if x is not None and math.isfinite(float(x))]
 return round(float(np.median(v)),5) if v else None

def eye(gray,lm,ids):
 h,w=gray.shape
 pts=np.array([(lm[i].x*w,lm[i].y*h) for i in ids])
 cx,cy=pts[0];r=float(np.median(np.linalg.norm(pts[1:]-pts[0],axis=1)))
 if not np.isfinite(r) or r<2 or not (0<=cx<w and 0<=cy<h):return [round(2*r,4) if np.isfinite(r) else None,None,None,None]
 p=int(max(3,math.ceil(1.5*r)));x0=max(0,int(cx)-p);x1=min(w,int(cx)+p+1);y0=max(0,int(cy)-p);y1=min(h,int(cy)+p+1)
 tile=gray[y0:y1,x0:x1];yy,xx=np.mgrid[y0:y1,x0:x1];dist=np.hypot(xx-cx,yy-cy)/r
 core=tile[dist<=.30];ring=tile[(dist>=.60)&(dist<=.95)]
 if len(core)<2 or len(ring)<4:return [round(2*r,4),None,None,None]
 contrast=float(np.median(ring)-np.median(core))
 mad=float(np.median(np.abs(ring.astype(float)-np.median(ring))))
 return [round(2*r,4),round(contrast,4),round(mad,4),round(float(cv2.Laplacian(tile,cv2.CV_64F).var()),4)]

def main():
 rows=[];sources={}
 with tempfile.TemporaryDirectory() as td,mp.solutions.face_mesh.FaceMesh(static_image_mode=True,max_num_faces=1,refine_landmarks=True,min_detection_confidence=.5) as model:
  for person in PINS:
   for kind,pin in PINS[person].items():
    path=Path("/tmp")/(person+"_"+kind);got=digest(path)
    if got!=pin:raise ValueError("SOURCE HASH MISMATCH "+person+" "+kind+" "+got)
    sources[person+"/"+kind]={"sha256":got,"bytes":path.stat().st_size}
   folder=Path(td)/person;folder.mkdir()
   subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss","5","-i","/tmp/"+person+"_video","-t","5","-vf","fps=6","-q:v","3",str(folder/"f_%03d.jpg")],check=True,timeout=120)
   frames=sorted(folder.glob("*.jpg"))
   if not frames:raise RuntimeError("NO FRAMES "+person)
   for idx,path in enumerate(frames):
    bgr=cv2.imread(str(path))
    if bgr is None:raise RuntimeError("DECODE "+str(path))
    gray=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
    result=model.process(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB))
    lm=result.multi_face_landmarks[0].landmark if result.multi_face_landmarks else []
    for label,ids in [("iris_468",[468,469,470,471,472]),("iris_473",[473,474,475,476,477])]:
     vals=eye(gray,lm,ids) if len(lm)>=478 else [None]*4
     rows.append({"participant":person,"frame_index":idx,"frame_sha256":digest(path),"eye":label,"face_mesh_detected":int(len(lm)>=478),"frame_brightness":round(float(gray.mean()),4),"width":gray.shape[1],"height":gray.shape[0],"iris_diameter_px":vals[0],"center_ring_contrast":vals[1],"ring_mad":vals[2],"sharpness":vals[3]})
 fields=list(rows[0]);p=OUT/"RAW_VISIBILITY.csv"
 with p.open("w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 participants={}
 for person in PINS:
  sample=[x for x in rows if x["participant"]==person];eyes={}
  for label in ("iris_468","iris_473"):
   a=[x for x in sample if x["eye"]==label];visible=[x for x in a if x["iris_diameter_px"] is not None];qualified=[x for x in visible if x["iris_diameter_px"]>=12]
   contrasts=[x["center_ring_contrast"] for x in visible if x["center_ring_contrast"] is not None]
   eyes[label]={"landmark_fraction":round(len(visible)/len(a),6),"diameter_12px_fraction":round(len(qualified)/len(a),6),"median_iris_diameter_px":median([x["iris_diameter_px"] for x in visible]),"median_center_ring_contrast":median(contrasts),"median_ring_mad":median([x["ring_mad"] for x in visible]),"median_sharpness":median([x["sharpness"] for x in visible]),"contrast_positive_fraction":round(sum(c>0 for c in contrasts)/len(contrasts),6) if contrasts else None,"exploratory_geometry_gate":len(qualified)/len(a)>=.8}
  participants[person]={"decoded_frames":len(set(x["frame_index"] for x in sample)),"median_frame_brightness":median([x["frame_brightness"] for x in sample]),"eyes":eyes}
 out={"run":"E002-225","source_provenance":sources,"participants":participants,"frame_csv_sha256":digest(p),"sampling":"6 fps images from nominal seconds 5-10; no certified exposure times","physiological_waveform_tested":False,"reference_paired_to_frames":False,"physiological_lag_certified":False,"gate":"exploratory: >=80% frames iris >=12 pixels"}
 (OUT/"RESULTS.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps(participants,indent=2))

if __name__=="__main__":main()
