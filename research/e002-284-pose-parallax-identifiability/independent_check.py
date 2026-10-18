"""Independent 16-corner verifier; does not import experiment.py."""
import json,math,itertools,pathlib,copy
P=pathlib.Path(__file__).resolve().parent
def verify(obj):
 for c in obj['rows']:
  a,b=math.radians(c['theta0_deg']),math.radians(c['theta1_deg'])
  z,e,d=c['Z_mm'],c['eps_mm'],c['delta_mm']
  V=[-z0*math.tan(a)+z1*math.tan(b)-e0/math.cos(a)+e1/math.cos(b) for z0,z1,e0,e1 in itertools.product((-z,z),(-z,z),(-e,e),(-e,e))]
  B=max(V);assert abs(min(V)+B)<1e-9
  assert abs(B-c['B_mm'])<1e-9 and abs(2*B-c['critical_mm'])<1e-9
  status='separable' if d>2*B else 'ambiguous'
  assert c['status']==status
  if status=='ambiguous':
   pair=obj['collisions'][c['case']]
   def proj(q):
    return (q['h0']*math.cos(a)+q['z0']*math.sin(a)+q['e0'],q['h1']*math.cos(b)+q['z1']*math.sin(b)+q['e1'])
   x,y=proj(pair['no_change']),proj(pair['closure'])
   assert max(abs(u-v) for u,v in zip(x,y))<1e-9
   assert abs(pair['closure']['h0']-pair['closure']['h1']-d)<1e-9
   for q in (pair['no_change'],pair['closure']):
    assert abs(q['z0'])<=z+1e-9 and abs(q['z1'])<=z+1e-9
    assert abs(q['e0'])<=e+1e-9 and abs(q['e1'])<=e+1e-9
  else:assert c['case'] not in obj['collisions']
 return True
x=json.loads((P/'results.json').read_text());assert verify(x)
for kind in ('threshold','label','collision'):
 y=copy.deepcopy(x)
 if kind=='threshold':y['rows'][0]['critical_mm']+=.1
 if kind=='label':y['rows'][1]['status']='separable'
 if kind=='collision':y['collisions']['pitch15']['closure']['h1']-=.1
 try:verify(y);raise RuntimeError('mutation not rejected: '+kind)
 except AssertionError:pass
print('PASS: 7 cases, 5 exact collisions, 3 mutation tests')
