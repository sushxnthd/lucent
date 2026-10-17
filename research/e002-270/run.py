#!/usr/bin/env python3
"""E002-270 synthetic reference-missingness boundary; no human data."""
import json, math, pathlib
FPS=60; N=300; ARTIFACT_MM=1.6
ref=[3+.24*math.sin(2*math.pi*.6*i/FPS) for i in range(N)]
def avg(x): return sum(x)/len(x)
def sd(x): return math.sqrt(avg([(v-avg(x))**2 for v in x]))
def metrics(pred,valid):
 x=[pred[i] for i in range(N) if valid[i]]
 y=[ref[i] for i in range(N) if valid[i]]
 r=avg([(u-avg(x))*(v-avg(y)) for u,v in zip(x,y)])/(sd(x)*sd(y))
 return dict(valid_frames=len(x),correlation=r,amplitude_ratio=sd(x)/sd(y),
  nrmse=math.sqrt(avg([(u-v)**2 for u,v in zip(x,y)]))/sd(y),
  rmse_mm=math.sqrt(avg([(u-v)**2 for u,v in zip(x,y)])))
def passed(m):
 return m['correlation']>=.75 and .75<=m['amplitude_ratio']<=1.25 and m['nrmse']<=.70
def mse_interval(pred,valid,lo,hi):
 assert lo<=hi
 observed=sum((pred[i]-ref[i])**2 for i in range(N) if valid[i])
 low=high=observed
 for i in range(N):
  if valid[i]: continue
  p=pred[i]
  low+=max(lo-p,0,p-hi)**2
  high+=max((p-lo)**2,(p-hi)**2)
 return [low/N,high/N]
trials=[]
for missing in (15,30,60):
 bad=set(range(120,120+missing))
 pred=[v+(ARTIFACT_MM if i in bad else 0) for i,v in enumerate(ref)]
 targeted=[i not in bad for i in range(N)]
 placebo=[not (i<missing) for i in range(N)]
 full=[True]*N
 a,b,c=metrics(pred,targeted),metrics(pred,placebo),metrics(pred,full)
 interval=mse_interval(pred,targeted,2.5,3.5)
 assert passed(a) and not passed(b) and not passed(c)
 assert interval[0]-1e-10<=c['rmse_mm']**2<=interval[1]+1e-10
 trials.append(dict(missing_frames=missing,missing_fraction=missing/N,
  rgb_only_admission_same=True,targeted_mask=a,placebo_mask=b,
  complete_reference=c,targeted_pass=passed(a),placebo_pass=passed(b),
  full_pass=passed(c),conditional_mse_interval_mm2_given_reference_range_2p5_to_3p5=interval))
result=dict(run='E002-270',source_type='SYNTHETIC_ONLY',camera_fps=FPS,
 frames_per_window=N,injected_rgb_only_artifact_mm=ARTIFACT_MM,
 frozen_gates=dict(correlation_min=.75,amplitude_ratio_min=.75,
  amplitude_ratio_max=1.25,nrmse_max=.70),trials=trials,
 theorem='Unknown missing references imply unbounded full-grid MSE without independent finite range. Bounded-range interval is sharp.',
 human_waveform_certified=False,product_certificate=False)
p=pathlib.Path(__file__).parent
(p/'RESULTS_REPLAY.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'run':'E002-270','trials':len(trials),
 'masked_passes':sum(t['targeted_pass'] for t in trials),
 'full_passes':sum(t['full_pass'] for t in trials)},sort_keys=True))
