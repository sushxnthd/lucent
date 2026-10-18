"""Independent constraint-intersection/LP checker for E002-285."""
import json,math,random
from pathlib import Path
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parent
def independent_bound(t0,t1,Z,D,eps):
 lines=[(1,0,Z),(1,0,-Z),(0,1,Z),(0,1,-Z),(-1,1,D),(-1,1,-D)]
 points=[]
 for i,(a,b,c) in enumerate(lines):
  for d,e,f in lines[i+1:]:
   det=a*e-b*d
   if abs(det)<1e-12:continue
   x=(c*e-b*f)/det;y=(a*f-c*d)/det
   if abs(x)<=Z+1e-9 and abs(y)<=Z+1e-9 and abs(y-x)<=D+1e-9:points.append((x,y))
 A,B=math.tan(math.radians(t1)),math.tan(math.radians(t0))
 return max(abs(A*y-B*x) for x,y in points)+eps*(1/math.cos(math.radians(t0))+1/math.cos(math.radians(t1)))
def check(data):
 assert data["run"]=="E002-285"
 for r in data["cases"]:
  t0,t1,Z,D,eps,delta=(r[k] for k in ["theta0_deg","theta1_deg","Z_mm","D_mm","eps_mm","closure_mm"])
  B=independent_bound(t0,t1,Z,D,eps)
  assert abs(r["critical_mm"]-2*B)<1e-9
  expected="distinguishable" if delta>2*B+1e-12 else "ambiguous"
  assert r["status"]==expected
  if expected=="ambiguous":
   c=data["collisions"][r["case"]];obs=[]
   for k in ["no_closure","closure"]:
    p=c[k]
    assert max(map(abs,p["z"]))<=Z+1e-9 and abs(p["z"][1]-p["z"][0])<=D+1e-9
    assert max(map(abs,p["e"]))<=eps+1e-9
    obs.append([p["h"][j]*math.cos(math.radians([t0,t1][j]))+p["z"][j]*math.sin(math.radians([t0,t1][j]))+p["e"][j] for j in [0,1]])
   assert max(abs(obs[0][j]-obs[1][j]) for j in [0,1])<1e-9
 return True
def main():
 d=json.loads((ROOT/"results.json").read_text());check(d)
 rng=random.Random(285)
 for _ in range(250):
  t0,t1=rng.uniform(-50,50),rng.uniform(-50,50)
  Z=rng.uniform(.01,2);D=rng.uniform(0,2.5*Z);eps=rng.uniform(.001,.15)
  A,B=math.tan(math.radians(t1)),math.tan(math.radians(t0))
  lp=linprog([B,-A],A_ub=[[-1,1],[1,-1]],b_ub=[D,D],bounds=[(-Z,Z),(-Z,Z)],method="highs")
  assert lp.success
  expected=-lp.fun+eps*(1/math.cos(math.radians(t0))+1/math.cos(math.radians(t1)))
  assert abs(independent_bound(t0,t1,Z,D,eps)-expected)<1e-9
 rejected=0
 for m in ["threshold","status","collision"]:
  altered=json.loads(json.dumps(d))
  if m=="threshold":altered["cases"][0]["critical_mm"]+=.1
  elif m=="status":altered["cases"][0]["status"]="ambiguous"
  else:altered["collisions"]["static_30_unconstrained"]["closure"]["h"][1]+=.2
  try:check(altered)
  except (AssertionError,KeyError):rejected+=1
 assert rejected==3
 print(json.dumps({"case_checks":len(d["cases"]),"randomized_lp_checks":250,"mutations_rejected":3,"all_pass":True}))
if __name__=="__main__":main()
