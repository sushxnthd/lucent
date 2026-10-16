import csv,json,hashlib
from pathlib import Path
p=Path('research/e002-225/RAW_VISIBILITY.csv')
assert hashlib.sha256(p.read_bytes()).hexdigest()=='087ca1cf7ce8cc1e24d9652ae5faa6e6a783abcaff716683d353a5544884e6fb'
rows=list(csv.DictReader(p.open()))
r=json.loads(Path('research/e002-229/RESULTS.json').read_text())
assert len(rows)==120
for person in ('P_33','P_54'):
 for eye in ('iris_468','iris_473'):
  a=[x for x in rows if x['participant']==person and x['eye']==eye]
  assert len(a)==30
  counts=[sum(float(x['iris_diameter_px'])>=12 for x in a),sum(float(x['center_ring_contrast'])>0 for x in a),sum(float(x['iris_diameter_px'])>=12 and float(x['center_ring_contrast'])>0 for x in a)]
  assert counts==r[person][eye]
assert r['P_33']['iris_473'][0]==23
assert r['P_54']['bilateral']==[30,5]
print('independent count checker PASS')
