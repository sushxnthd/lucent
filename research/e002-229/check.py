import csv,json,hashlib
from pathlib import Path
p=Path('research/e002-225/RAW_VISIBILITY.csv')
assert hashlib.sha256(p.read_bytes()).hexdigest()=='087ca1cf7ce8cc1e24d9652ae5faa6e6a783abcaff716683d353a5544884e6fb'
rows=list(csv.DictReader(p.open()))
r=json.loads(Path('research/e002-229/RESULTS.json').read_text())
assert len(rows)==120
for person in ('P_33','P_54'):
 frames={}
 for x in rows:
  if x['participant']!=person:continue
  i=int(x['frame_index']);e=x['eye']
  assert e not in frames.setdefault(i,{})
  frames[i][e]=x
 assert len(frames)==30
 for eye in ('iris_468','iris_473'):
  a=[frames[i][eye] for i in range(30)]
  g=lambda x:float(x['iris_diameter_px'])>=12
  c=lambda x:float(x['center_ring_contrast'])>0
  assert [sum(g(x) for x in a),sum(c(x) for x in a),sum(g(x) and c(x) for x in a)]==r[person][eye]
  assert all(len(frames[i])==2 for i in range(30))
  bilateral=[sum(all(g(x) for x in f.values()) for f in frames.values()),sum(all(g(x) and c(x) for x in f.values()) for f in frames.values())]
  assert bilateral==r[person]['bilateral']
assert r['P_33']['iris_473'][0]==23 and r['P_54']['bilateral']==[30,5]
print('independent count checker PASS')
