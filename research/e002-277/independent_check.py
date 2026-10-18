"""Independent projection/Schur-complement check; no experiment.py imports."""
import json,math,pathlib
import numpy as np
from scipy.special import erfinv
HERE=pathlib.Path(__file__).resolve().parent
def verify(d):
 md=d['metadata'];n=md['n'];sig=md['edge_sigma_px'];tau=md['common_bias_tau_px'];tol=md['tolerance_px']
 assert n==60 and md['reps_per_condition']==12000 and len(d['rows'])==10
 hold=[]
 for r in d['rows']:
  t=np.linspace(-r['alpha_rad'],r['alpha_rad'],n)
  Z=np.column_stack((np.cos(t),np.sin(t)))
  e=np.ones(n)-Z@np.linalg.lstsq(Z,np.ones(n),rcond=None)[0]
  v=sig**2/float(e@e);dv=2*v+2*tau*tau*(1-r['phi']);av=v+tau*tau
  prob=math.erf(tol/math.sqrt(2*dv))
  assert abs(r['edge_radius_variance']-v)<1e-9
  assert abs(r['delta_variance']-dv)<1e-9
  assert abs(r['absolute_variance']-av)<1e-9
  assert abs(r['predicted_delta_pass']-prob)<1e-10
  assert abs(r['empirical_delta_pass']-prob)<.02
  assert abs(r['empirical_delta_variance']/dv-1)<.06
  assert abs(r['empirical_absolute_variance']/av-1)<.06
  assert r['predicted_gate']==(prob>=md['target_success'])
  if r['split']=='predeclared_synthetic_holdout':hold.append((r['alpha_rad'],r['phi']))
 assert hold==[(.9,.84),(.9,.96),(1.1,.75),(1.1,.9)]
 t=np.linspace(-.9,.9,n);Z=np.column_stack((np.cos(t),np.sin(t)))
 e=np.ones(n)-Z@np.linalg.lstsq(Z,np.ones(n),rcond=None)[0]
 v=sig**2/float(e@e)
 limit=tol**2/(2*erfinv(.75)**2)
 pmin=1-(limit-2*v)/(2*tau*tau)
 assert abs(d['coherence_boundary']['required_phi']-pmin)<1e-9
 assert abs(d['coherence_boundary']['maximum_delta_t_at_T_1sec']+math.log(pmin))<1e-9
 assert d['nonidentifiability']['same_frames_max_error']==0
 assert d['nonidentifiability']['delta_A']!=d['nonidentifiability']['delta_B']
 assert d['wildcard']['correlated_edge_variance']>d['wildcard']['independent_edge_variance']
if __name__=='__main__':
 d=json.loads((HERE/'RESULTS.json').read_text());verify(d)
 for k in ['predicted_delta_pass','delta_variance','empirical_delta_pass','required_phi']:
  copy=json.loads(json.dumps(d))
  if k=='required_phi':copy['coherence_boundary'][k]+=.02
  else:copy['rows'][6][k]+=.15
  try:verify(copy)
  except AssertionError:continue
  raise AssertionError('Undetected mutation '+k)
 print('PASS: 10 independently checked conditions, 4 mutations rejected')
