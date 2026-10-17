import json
from pathlib import Path
O={}
for p,t0 in [('P_33',1492456828.724),('P_54',1493130049.332)]:
 R=[json.loads(s) for s in Path('/tmp/'+p+'_tracker').read_bytes().splitlines()]
 E={}
 for e in ('left','right'):
  T=sorted(float(r['true_time'])-t0 for r in R if r.get(e+'_pupil_validity')==1 and isinstance(r.get(e+'_pupil_diameter'),(float,int)) and r[e+'_pupil_diameter']>0)
  E[e]=[[round(a,4),round(b,4)] for a,b in zip(T,T[1:]) if .12<=b-a<=.8 and 5<=(a+b)/2<=25]
 O[p]={'gaps':E,'binocular':sum(abs((a+b-c-d)/2)<.12 and min(b,d)-max(a,c)>=.04 for a,b in E['left'] for c,d in E['right'])}
Path('research/e002-261/GAPS.json').write_text(json.dumps(O,indent=2)+'\n')
print({p:(len(v['gaps']['left']),len(v['gaps']['right']),v['binocular']) for p,v in O.items()})
