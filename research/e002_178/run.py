import json
import numpy as np
from scipy.special import ndtr,ndtri
from pathlib import Path
w=(np.arange(4096)+.5)/4096
rows=[]
for R in (6.,9.,12.):
 for blur in (.8,1.5,2.5):
  x=np.linspace(R-6*blur,R+6*blur,6001)
  edge=ndtr((x-R)/blur)
  for gamma in (1.2,1.6,2.2):
   raw=edge**gamma
   cal=np.interp(raw,w**gamma,w)
   rows.append(dict(R=R,s=blur,gamma=gamma,
     raw_shift_px=float(np.interp(.5,raw,x)-R),
     corrected_shift_px=float(np.interp(.5,cal,x)-R),
     analytic_raw_shift_px=float(blur*ndtri(2**(-1/gamma)))))
x=np.linspace(0,18,6001)
edge=ndtr((x-9)/1.5)
local=float(np.interp(.5,edge**2.2,x)-9)
sparse=float(np.interp(.5,np.interp(edge,[0,.1,.5,.9,1],[0,.1,.65,.9,1]),x)-9)
result={'rows':rows,'adversarial':{'local_false_shift_px':local,
 'sparse_witness_false_shift_px':sparse},'human_waveform':'NOT_TESTED'}
assert len(rows)==27 and max(abs(r['corrected_shift_px']) for r in rows)<.01
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result,indent=2))
print('PASS 27 global cases; local and sparse counterexamples:',local,sparse)
