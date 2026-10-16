import csv,hashlib,json,subprocess,tempfile
from pathlib import Path
import cv2,mediapipe as mp,numpy as np
from edge import evaluate
OUT=Path('research/e002-234')
PINS={'P_33':'edd83fd16806778ffe6565e5f2311a5dac17909edbfb603576d0b5448ec487d8',
'P_54':'dcfaa40b4c80b0c5a0c09a993d3d203ff33bed760a12ba0801e0db383a620869'}
EYES={'iris_468':[468,469,470,471,472],'iris_473':[473,474,475,476,477]}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 rows=[];sources={}
 with tempfile.TemporaryDirectory() as tmp,mp.solutions.face_mesh.FaceMesh(
  static_image_mode=True,max_num_faces=1,refine_landmarks=True,min_detection_confidence=.5) as mesh:
  for person,pin in PINS.items():
   video=Path('/tmp')/(person+'_video')
   assert sha(video)==pin,'SOURCE HASH MISMATCH'
   sources[person]={'video_sha256':pin,'video_bytes':video.stat().st_size}
   folder=Path(tmp)/person;folder.mkdir()
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','5','-i',str(video),
                   '-t','5','-vf','fps=6','-q:v','3',str(folder/'f_%03d.jpg')],check=True,timeout=120)
   frames=sorted(folder.glob('*.jpg'));assert len(frames)==30,(person,len(frames))
   for i,path in enumerate(frames):
    bgr=cv2.imread(str(path));assert bgr is not None
    gray=cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY)
    output=mesh.process(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB))
    lm=output.multi_face_landmarks[0].landmark if output.multi_face_landmarks else []
    for eye,ids in EYES.items():
     base={'participant':person,'frame':i,'eye':eye,'frame_sha256':sha(path)}
     if len(lm)<478:
      rows.append({**base,'eligible':0,'reason':'face_mesh_missing'});continue
     pts=np.array([(lm[j].x*gray.shape[1],lm[j].y*gray.shape[0]) for j in ids])
     rows.append({**base,**evaluate(gray,pts)})
 keys=['participant','frame','eye','frame_sha256','iris_diameter_px','center_x','center_y',
       'eligible','reason','radius_ratio','peak','edge_margin','split_disagreement',
       'gamma_disagreement','placebo_ratio']
 p=OUT/'RAW_BOUNDARY.csv'
 with p.open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows(rows)
 groups={}
 for person in PINS:
  groups[person]={}
  for eye in EYES:
   a=[r for r in rows if r['participant']==person and r['eye']==eye]
   groups[person][eye]={'n':len(a),'admitted':sum(int(r['eligible']) for r in a),
    'geometry_ge12':sum(float(r.get('iris_diameter_px') or 0)>=12 for r in a),
    'positive_peak':sum(float(r.get('peak') or 0)>0 for r in a),
    'margin_ge1_5':sum(float(r.get('edge_margin') or 0)>=1.5 for r in a),
    'placebo_lt_0_8':sum(float(r.get('placebo_ratio') or 100)<.8 for r in a)}
 result={'run':'E002-234','source':sources,'raw_sha256':sha(p),'groups':groups,
  'n_rows':len(rows),'clock_calibrated':False,'human_reference_compared':False,
  'waveform_certified':False,'measurement_certified':False,
  'limitation':'Uncalibrated radial estimator without true pupil contour or certified clock'}
 (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(groups,sort_keys=True))
if __name__=='__main__':main()
