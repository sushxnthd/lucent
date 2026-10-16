import json,math
from pathlib import Path
r=json.loads(Path(__file__).with_name('RESULTS.json').read_text())
assert r['run']=='E002-223' and not r['human_data_used']
assert max(r['max_pairwise_waveform_difference'])<1e-12
for f in (1,2,5):
 assert abs(r['clock_tolerance_ms'][str(f)]-1000*math.acos(.7)/(2*math.pi*f))<1e-9
print('independent arithmetic checker passed')
