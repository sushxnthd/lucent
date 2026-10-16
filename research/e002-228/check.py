import csv,json,hashlib
from pathlib import Path
b=Path('research/e002-225')
d=json.loads((b/'RESULTS.json').read_text())
p=b/'RAW_VISIBILITY.csv'
assert hashlib.sha256(p.read_bytes()).hexdigest()==d['frame_csv_sha256']
rows=list(csv.DictReader(p.open()))
fail=[]
for person in ('P_33','P_54'):
 for eye in ('iris_468','iris_473'):
  a=[r for r in rows if r['participant']==person and r['eye']==eye]
  assert len(a)>=20
  f=sum(bool(r['iris_diameter_px']) and float(r['iris_diameter_px'])>=12 for r in a)/len(a)
  assert abs(f-d['participants'][person]['eyes'][eye]['diameter_12px_fraction'])<1e-6
  if f<.8:fail.append([person,eye,f])
Path('research/e002-228/FAILED_GATES.json').write_text(json.dumps(fail))
print('INDEPENDENT_GATE_CHECK_PASS',len(rows),'SCIENTIFIC_GATE_FAILURES',fail)
