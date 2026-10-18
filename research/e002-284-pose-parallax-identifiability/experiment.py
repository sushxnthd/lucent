"""E002-284 reproducible synthetic pose/parallax experiment. No human data."""
import csv,json,math,pathlib
from scipy.optimize import linprog
P=pathlib.Path(__file__).resolve().parent
CASES=[('frontal',0,0,.7,.05,.4),('pitch15',15,15,.7,.05,.8),('pitch30',30,30,.7,.05,1.7),('pitch45',45,45,.7,.05,3.2),('pitch_transition',-10,25,.7,.05,1.0),('small_depth',30,30,.2,.02,.5),('synthetic_holdout',-23,37,.43,.037,1.12)]
def halfwidth(a,b,z,e):
 a,b=math.radians(a),math.radians(b)
 return z*(abs(math.tan(a))+abs(math.tan(b)))+e*(abs(1/math.cos(a))+abs(1/math.cos(b)))
def collision(a,b,z,e,delta):
 a,b=math.radians(a),math.radians(b)
 B=z*(abs(math.tan(a))+abs(math.tan(b)))+e*(1/math.cos(a)+1/math.cos(b))
 def nuisance(r):
  v=r/B
  return [-math.copysign(z,math.tan(a))*v,math.copysign(z,math.tan(b))*v,-e*v,e*v]
 z0,z1,e0,e1=nuisance(-delta/2);Z0,Z1,E0,E1=nuisance(delta/2)
 H=5.
 Y0=H*math.cos(a)+z0*math.sin(a)+e0
 Y1=H*math.cos(b)+z1*math.sin(b)+e1
 H1=(Y0-Z0*math.sin(a)-E0)/math.cos(a)
 y0=H1*math.cos(a)+Z0*math.sin(a)+E0
 y1=(H1-delta)*math.cos(b)+Z1*math.sin(b)+E1
 assert max(abs(Y0-y0),abs(Y1-y1))<1e-9
 return {'no_change':{'h0':H,'h1':H,'z0':z0,'z1':z1,'e0':e0,'e1':e1},'closure':{'h0':H1,'h1':H1-delta,'z0':Z0,'z1':Z1,'e0':E0,'e1':E1},'same_observed_u':[Y0,Y1]}
def run():
 rows=[]; collisions={}
 for name,a,b,z,e,d in CASES:
  B=halfwidth(a,b,z,e)
  ca,cb=math.radians(a),math.radians(b)
  coeff=[-math.tan(ca),math.tan(cb),-1/math.cos(ca),1/math.cos(cb)]
  limits=[(-z,z),(-z,z),(-e,e),(-e,e)]
  lo=linprog(coeff,bounds=limits,method='highs')
  hi=linprog([-x for x in coeff],bounds=limits,method='highs')
  assert lo.success and hi.success and abs(lo.fun+B)<1e-9 and abs(hi.fun+B)<1e-9
  status='separable' if d>2*B else 'ambiguous'
  if status=='ambiguous':collisions[name]=collision(a,b,z,e,d)
  rows.append({'case':name,'theta0_deg':a,'theta1_deg':b,'Z_mm':z,'eps_mm':e,'delta_mm':d,'B_mm':B,'critical_mm':2*B,'margin_mm':d-2*B,'status':status})
 (P/'results.json').write_text(json.dumps({'kind':'synthetic only','model':'u=h cos(theta)+z sin(theta)+e','rows':rows,'collisions':collisions,'wildcard':{'coherent_depth_30deg_critical_mm':4*.05/math.cos(math.radians(30)),'warning':'z0=z1 assumption unvalidated during blinks'}},indent=2)+'\n')
 with (P/'raw_cases.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print('cases',len(rows),'ambiguous',len(collisions))
if __name__=='__main__':run()
