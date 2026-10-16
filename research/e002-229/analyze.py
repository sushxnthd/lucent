import csv,hashlib,json
from pathlib import Path
p=Path('research/e002-225/RAW_VISIBILITY.csv')
raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='087ca1cf7ce8cc1e24d9652ae5faa6e6a783abcaff716683d353a5544884e6fb'
rows=list(csv.DictReader(raw.decode().splitlines()))
assert len(rows)==120
out={'source_run':38866995557,'source_artifact':12031733076,'count_order':'geometry>=12px,contrast>0,joint','n_frames_per_person':30,'frozen_gate_failure':'P_33 iris_473','contrast_test':'exploratory','physiological_waveform':False}
for person in ('P_33','P_54'):
 out[person]={}
 frames={}
 for eye in ('iris_468','iris_473'):
  a=[r for r in rows if r['participant']==person and r['eye']==eye]
  assert len(a)==30
  g=lambda r:float(r['iris_diameter_px'])>=12
  c=lambda r:float(r['center_ring_contrast'])>0
  out[person][eye]=[sum(g(r) for r in a),sum(c(r) for r in a),sum(g(r) and c(r) for r in a)]
  for r in a:frames.setdefault(int(r['frame_index']),{})[eye]=(g(r),c(r))
 assert len(frames)==30
 out[person]['bilateral']=[sum(all(v[0] for v in f.values()) for f in frames.values()),sum(all(v[0] and v[1] for v in f.values()) for f in frames.values())]
Path('research/e002-229/RESULTS.json').write_text(json.dumps(out,sort_keys=True)+'\n')
print(out)
