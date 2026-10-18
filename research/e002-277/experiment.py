"""E002-277 synthetic conditional temporal aperture/coherence experiment."""
import json, math, pathlib
import numpy as np
from scipy.stats import norm
HERE=pathlib.Path(__file__).resolve().parent
SEED=2772026;N=60;SIGMA=.5;TAU=1.2;TOL=1.;TARGET=.75;REPS=12000
DEVELOPMENT=[(.7,.8),(.9,.8),(.9,.9),(1.1,.9),(1.1,.98),(1.4,.75)]
HOLDOUT=[(.9,.84),(.9,.96),(1.1,.75),(1.1,.9)]
def design(alpha):
 t=np.linspace(-alpha,alpha,N)
 return np.stack((np.ones(N),np.cos(t),np.sin(t)),axis=1)
def predicted(alpha,phi):
 X=design(alpha)
 v=float(SIGMA**2*np.linalg.inv(X.T@X)[0,0])
 dv=2*v+2*TAU**2*(1-phi); av=v+TAU**2
 prob=float(2*norm.cdf(TOL/math.sqrt(dv))-1)
 z=float(norm.ppf((1+TARGET)/2))
 pmin=1-(TOL**2/z**2-2*v)/(2*TAU**2)
 return dict(alpha_rad=alpha,arc_deg=2*alpha*180/math.pi,phi=phi,
             edge_radius_variance=v,absolute_variance=av,delta_variance=dv,
             predicted_delta_pass=prob,predicted_absolute_pass=float(2*norm.cdf(TOL/math.sqrt(av))-1),
             minimum_phi_for_75pct=pmin,predicted_gate=prob>=TARGET)
def simulate(alpha,phi,rng):
 X=design(alpha);w=np.linalg.solve(X.T@X,X.T)[0]
 beta0=np.array([20.,1.5,-.9]);beta1=np.array([20.7,-1.2,1.8])
 u=rng.normal(size=(REPS,2));b0=TAU*u[:,0]
 b1=TAU*(phi*u[:,0]+math.sqrt(1-phi**2)*u[:,1])
 e0=rng.normal(0,SIGMA,size=(REPS,N));e1=rng.normal(0,SIGMA,size=(REPS,N))
 y0=(X@beta0)[None,:]+b0[:,None]+e0
 y1=(X@beta1)[None,:]+b1[:,None]+e1
 fit0=y0@w;fit1=y1@w
 de=(fit1-fit0)-(beta1[0]-beta0[0]);ae=fit0-beta0[0]
 unchanged=(b1-b0)+(e1-e0)@w
 return dict(empirical_delta_pass=float(np.mean(abs(de)<=TOL)),
             empirical_absolute_pass=float(np.mean(abs(ae)<=TOL)),
             empirical_delta_variance=float(np.var(de,ddof=1)),
             empirical_absolute_variance=float(np.var(ae,ddof=1)),
             unchanged_false_change_gt_1px=float(np.mean(abs(unchanged)>TOL)),
             simulation_repetitions=REPS)
def main():
 rng=np.random.default_rng(SEED);rows=[]
 for split,configs in [('development',DEVELOPMENT),('predeclared_synthetic_holdout',HOLDOUT)]:
  for a,phi in configs:
   rows.append(dict(split=split,**predicted(a,phi),**simulate(a,phi,rng)))
 pcrit=predicted(.9,.9)['minimum_phi_for_75pct']
 X=design(.8)
 a0=X@np.array([20.,2.,-1.]);a1=X@np.array([20.5,-2.,1.])
 b0=X@np.array([19.,2.,-1.])+1
 b1=X@np.array([21.,-2.,1.])-.5
 same=float(max(np.max(abs(a0-b0)),np.max(abs(a1-b1))))
 assert same==0
 X=design(1.1);vi=float(SIGMA**2*np.linalg.inv(X.T@X)[0,0])
 out=dict(metadata=dict(seed=SEED,source='synthetic edge-coordinate instrument model ONLY',
           n=N,edge_sigma_px=SIGMA,common_bias_tau_px=TAU,tolerance_px=TOL,
           target_success=TARGET,reps_per_condition=REPS,
           independent_reference='known simulated pupil-radius change',
           test_freeze='DEVELOPMENT and HOLDOUT specified before outcomes'),
          rows=rows,
          coherence_boundary=dict(alpha_rad=.9,required_phi=pcrit,
             maximum_delta_t_at_T_1sec=float(-math.log(pcrit))),
          nonidentifiability=dict(delta_A=.5,delta_B=2.,same_frames_max_error=same),
          wildcard=dict(spatial_exchangeable_rho=.1,alpha_rad=1.1,
             independent_edge_variance=vi,correlated_edge_variance=.9*vi+.1*SIGMA**2))
 (HERE/'RESULTS.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
 print(json.dumps(dict(holdout=[(r['alpha_rad'],r['phi'],r['predicted_delta_pass'],r['empirical_delta_pass']) for r in rows if r['split']=='predeclared_synthetic_holdout'],coherence=out['coherence_boundary']),indent=2))
if __name__=='__main__':main()
