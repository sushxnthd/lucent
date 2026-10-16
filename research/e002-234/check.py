import csv,hashlib,json
from pathlib import Path
D=Path('research/e002-234');p=D/'RAW_BOUNDARY.csv';o=json.loads((D/'RESULTS.json').read_text())
assert hashlib.sha256(p.read_bytes()).hexdigest()==o['raw_sha256']
rows=list(csv.DictReader(p.open()));assert len(rows)==o['n_rows']==120
assert len({(r['participant'],r['frame'],r['eye']) for r in rows})==120
for person,eyes in o['groups'].items():
 for eye,d in eyes.items():
  a=[r for r in rows if r['participant']==person and r['eye']==eye]
  assert len(a)==d['n']==30
  assert len({r['frame_sha256'] for r in a})==30
  assert sum(int(r['eligible']) for r in a)==d['admitted']
  assert sum(float(r['iris_diameter_px'] or 0)>=12 for r in a)==d['geometry_ge12']
  assert sum(float(r['peak'] or 0)>0 for r in a)==d['positive_peak']
  assert sum(float(r['edge_margin'] or 0)>=1.5 for r in a)==d['margin_ge1_5']
  assert sum(float(r['placebo_ratio'] or 100)<.8 for r in a)==d['placebo_lt_0_8']
  for r in a:
   if int(r['eligible']):
    assert r['reason']=='pass'
    assert float(r['iris_diameter_px'])>=12 and float(r['peak'])>0
    assert float(r['edge_margin'])>=1.5
    assert float(r['split_disagreement'])<=.120001
    assert float(r['gamma_disagreement'])<=.050001
    assert float(r['placebo_ratio'])<.8
assert not o['clock_calibrated'] and not o['waveform_certified'] and not o['measurement_certified']
print('INDEPENDENT_ACCOUNTING_PASS',len(rows),o['groups'])
