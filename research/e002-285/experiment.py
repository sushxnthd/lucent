"""E002-285: temporal depth coherence; synthetic instrument only."""
import csv,json,math
from pathlib import Path
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parent
CASES=[("static_30_coherent",30,30,.7,.08,.05,.5),
("static_30_unconstrained",30,30,.7,1.4,.05,.5),
("static_30_moderate_depth",30,30,.7,.4,.05,.5),
("pitch_30_to_40_coherent",30,40,.7,.08,.05,.5),
("pitch_minus_10_to_25",-10,25,.7,.08,.05,.5),
("frontal",0,0,.7,.08,.05,.5),
("pose_15_to_20_coherent",15,20,.7,.08,.05,.5),
("unseen_synthetic_pose_heldout",-17,31,.53,.11,.035,.75)]
def bound(t0,t1,Z,D,eps):
 a,b=math.tan(math.radians(t1)),math.tan(math.radians(t0))
 d=min(D,2*Z)
 vs=[(Z,Z),(-Z,-Z),(Z,Z-d),(Z-d,Z),(-Z,-Z+d),(-Z+d,-Z)]
 z0,z1=max(vs,key=lambda v:a*v[1]-b*v[0])
 S=a*z1-b*z0
 E=eps*(1/math.cos(math.radians(t0))+1/math.cos(math.radians(t1)))
 return S+E,S,E,(z0,z1)
def independent_lp(t0,t1,Z,D,eps):
 a,b=math.tan(math.radians(t1)),math.tan(math.radians(t0))
 c=[b,-a,1/math.cos(math.radians(t0)),-1/math.cos(math.radians(t1))]
 r=linprog(c,A_ub=[[-1,1,0,0],[1,-1,0,0]],b_ub=[D,D],bounds=[(-Z,Z),(-Z,Z),(-eps,eps),(-eps,eps)],method="highs")
 assert r.success
 return -r.fun
def collision(t0,t1,Z,D,eps,delta):
 B,S,E,vertex=bound(t0,t1,Z,D,eps)
 def nuisance(target):
  k=target/B if B else 0
  return k*vertex[0],k*vertex[1],-k*eps,k*eps
 t0,t1=math.radians(t0),math.radians(t1)
 z00,z01,e00,e01=nuisance(-delta/2)
 z10,z11,e10,e11=nuisance(delta/2)
 h=5.
 y0=h*math.cos(t0)+z00*math.sin(t0)+e00
 y1=h*math.cos(t1)+z01*math.sin(t1)+e01
 hp=(y0-z10*math.sin(t0)-e10)/math.cos(t0)
 y0p=hp*math.cos(t0)+z10*math.sin(t0)+e10
 y1p=(hp-delta)*math.cos(t1)+z11*math.sin(t1)+e11
 assert hp-delta>0 and max(abs(y0-y0p),abs(y1-y1p))<1e-10
 return {"no_closure":{"h":[h,h],"z":[z00,z01],"e":[e00,e01]},"closure":{"h":[hp,hp-delta],"z":[z10,z11],"e":[e10,e11]},"identical_observations":[y0,y1],"max_difference":max(abs(y0-y0p),abs(y1-y1p))}
def main():
 rows=[]; collisions={}
 for name,t0,t1,Z,D,eps,delta in CASES:
  B,S,E,v=bound(t0,t1,Z,D,eps)
  check=independent_lp(t0,t1,Z,D,eps)
  assert abs(B-check)<1e-9
  status="distinguishable" if delta>2*B+1e-12 else "ambiguous"
  if status=="ambiguous":collisions[name]=collision(t0,t1,Z,D,eps,delta)
  rows.append(dict(case=name,theta0_deg=t0,theta1_deg=t1,Z_mm=Z,D_mm=D,eps_mm=eps,closure_mm=delta,geometric_bound_mm=S,noise_bound_mm=E,critical_mm=2*B,lp_critical_mm=2*check,margin_mm=delta-2*B,status=status))
 with (ROOT/"raw_cases.csv").open("w",newline="") as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 out={"run":"E002-285","data_type":"deterministic synthetic; no human RGB/reference","model":"u_t=h_t*cos(theta_t)+z_t*sin(theta_t)+e_t","theorem":"delta>2(S+E) iff fixed closure vs no-change disjoint","cases":rows,"collisions":collisions,"failed_gates":["no empirical Z/D/eps","no human paired reference","no device/participant holdout","no field-level novelty"]}
 (ROOT/"results.json").write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps({"cases":len(rows),"collisions":len(collisions),"statuses":[r["status"] for r in rows]}))
if __name__=="__main__":main()
