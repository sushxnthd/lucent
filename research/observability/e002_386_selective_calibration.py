"""E002-386 synthetic selective-risk validation. Not human/physical-camera evidence."""
import json
from pathlib import Path
import numpy as np
from scipy.stats import beta
SEED=20261023
F,W,V,THETA=1/30,.01,40.,.2
H=F-W
CENTER=(F+W)/2
ALPHA,DELTA=.02,.05
MARGINS=(0.,.04,.08,.12,.16,.22,.26,.30)
QUALITIES=(.30,.50,.75,1.)
CANDIDATES=tuple((m,q) for m in MARGINS for q in QUALITIES)
def exposure_mean_left(min_aperture):
    minimum=np.asarray(min_aperture,dtype=float)
    crossing=np.clip(CENTER-(1-minimum)/V,0,W)
    return (crossing+(minimum+V*CENTER)*(W-crossing)-V*(W**2-crossing**2)/2)/W
def simulate(n,rng,unseen=False):
    hidden=rng.random(n)>=.35
    amin=rng.uniform(.17,.195,n)
    ref=np.where(hidden,exposure_mean_left(amin),1.)
    ref2=np.column_stack((ref,ref))
    bad=hidden&(rng.random(n)<.05)
    shifted=hidden&(rng.random(n)<.12) if unseen else np.zeros(n,dtype=bool)
    bad &= ~shifted
    bias=rng.uniform(-.002,.002,n)
    bias=np.where(bad,rng.uniform(.07,.14,n),bias)
    bias=np.where(shifted,rng.uniform(.18,.26,n),bias)
    quality=rng.uniform(0,.6,n)
    quality=np.where(bad,rng.uniform(.25,1,n),quality)
    observed=np.clip(ref2+bias[:,None]+rng.uniform(-.002,.002,(n,2)),0,1)
    return {'hidden':hidden,'reference':ref2,'observed':observed,'quality':quality,
            'bad':bad,'shifted':shifted,'min_aperture':np.where(hidden,amin,1.)}
def margin(observed,error=.002):
    mu=np.maximum(0.,observed-error)
    d=np.where(1-mu<=V*W/2,np.sqrt(2*V*W*np.maximum(0.,1-mu)),1-mu+V*W/2)
    lower=np.clip(1-d,0,1)
    left,right=lower[:,0],lower[:,1]
    return np.maximum.reduce([left-V*H,right-V*H,(left+right-V*H)/2])-THETA
def candidate_masks(score,quality):
    return np.stack([(score>=m)&(quality<=q) for m,q in CANDIDATES],axis=0)
def upper_bound(errors,total,delta=DELTA/len(CANDIDATES)):
    if total==0 or errors==total: return 1.
    return float(beta.ppf(1-delta,errors+1,total-errors))
def calibrate(dataset):
    masks=candidate_masks(margin(dataset['observed']),dataset['quality'])
    counts=masks.sum(axis=1)
    errors=(masks&dataset['hidden'][None,:]).sum(axis=1)
    bounds=np.array([upper_bound(int(e),int(n)) for e,n in zip(errors,counts)])
    eligible=np.flatnonzero((bounds<=ALPHA)&(counts>0))
    selected=(sorted(eligible,key=lambda j:(-int(counts[j]),float(bounds[j]),
                                           -CANDIDATES[j][0],CANDIDATES[j][1]))[0]
              if len(eligible) else None)
    return {'selected':None if selected is None else int(selected),
            'counts':counts,'errors':errors,'bounds':bounds}
def evaluate(dataset,chosen):
    s=margin(dataset['observed'])
    naive=s>0
    issued=np.zeros(len(s),dtype=bool) if chosen is None else (
        (s>=CANDIDATES[chosen][0])&(dataset['quality']<=CANDIDATES[chosen][1]))
    def row(mask):
        n=int(mask.sum());e=int((mask&dataset['hidden']).sum())
        return {'issued':n,'false':e,'risk':e/n if n else None,
                'issue_fraction':n/len(mask)}
    return {'naive':row(naive),'selected':row(issued),
            'bad_issued':int((issued&dataset['bad']).sum()),
            'shift_issued':int((issued&dataset['shifted']).sum())}
def product_decision(*,known_device,timing_calibrated,frames_complete,
                     score,quality,candidate,validation_status='synthetic_only'):
    if validation_status!='paired_human_independent': return 'ABSTAIN_NO_HUMAN_VALIDATION'
    if not known_device: return 'ABSTAIN_UNSEEN_DEVICE'
    if not timing_calibrated: return 'ABSTAIN_TIMING'
    if not frames_complete: return 'ABSTAIN_MISSINGNESS'
    if candidate is None: return 'ABSTAIN_NO_VALID_CALIBRATION'
    if not np.isfinite(score) or not np.isfinite(quality): return 'ABSTAIN_INVALID_MEASUREMENT'
    m,q=CANDIDATES[candidate]
    return 'STATISTICAL_RISK_QUALIFIED' if score>=m and quality<=q else 'ABSTAIN_LOW_CONFIDENCE'
def run(seed=SEED,ncal=6000,ntest=30000,noracle=500000,reps=100):
    rng=np.random.default_rng(seed)
    cal=simulate(ncal,rng)
    frozen=calibrate(cal)
    iid=evaluate(simulate(ntest,rng),frozen['selected'])
    shifted=evaluate(simulate(ntest,rng,unseen=True),frozen['selected'])
    oracle=simulate(noracle,rng)
    masks=candidate_masks(margin(oracle['observed']),oracle['quality'])
    oracle_counts=masks.sum(axis=1)
    oracle_errors=(masks&oracle['hidden'][None,:]).sum(axis=1)
    oracle_risks=oracle_errors/np.maximum(oracle_counts,1)
    oracle_lower=np.where(oracle_errors==0,0.,
        beta.ppf(.0005,oracle_errors,oracle_counts-oracle_errors+1))
    oracle_upper=np.where(oracle_errors==oracle_counts,1.,
        beta.ppf(.9995,oracle_errors+1,oracle_counts-oracle_errors))
    certain_covered,certain_fail,ambiguous=0,0,0
    for k in range(reps):
        cc=calibrate(simulate(ncal,np.random.default_rng(seed+1000+k)))
        if np.all(cc['bounds']>=oracle_upper): certain_covered+=1
        elif np.any(cc['bounds']<oracle_lower): certain_fail+=1
        else: ambiguous+=1
    selected=frozen['selected']
    base=dict(known_device=True,timing_calibrated=True,frames_complete=True,
              score=.5,quality=.1,candidate=selected)
    result={'experiment':'E002-386','seed':seed,'synthetic_only':True,
            'n_calibration':ncal,'n_test_per_condition':ntest,
            'alpha':ALPHA,'delta':DELTA,'candidate_count':len(CANDIDATES),
            'selected':None if selected is None else {
                'index':selected,'margin':CANDIDATES[selected][0],
                'quality':CANDIDATES[selected][1],
                'cal_issued':int(frozen['counts'][selected]),
                'cal_errors':int(frozen['errors'][selected]),
                'simultaneous_upper_risk':float(frozen['bounds'][selected])},
            'iid':iid,'unseen_device_if_gate_bypassed':shifted,
            'oracle_n':noracle,
            'oracle_selected_risk_estimate':None if selected is None else float(oracle_risks[selected]),
            'oracle_selected_99_9pct_ci':None if selected is None else [
                float(oracle_lower[selected]),float(oracle_upper[selected])],
            'replicate_simultaneous_coverage':{
                'reps':reps,'definitely_covered':certain_covered,
                'definitely_failed':certain_fail,
                'indeterminate_due_to_oracle_mc':ambiguous},
            'product_gates':{
                'synthetic_only':product_decision(**base),
                'hypothetically_validated':product_decision(**base,validation_status='paired_human_independent'),
                'unknown_device':product_decision(**{**base,'known_device':False},validation_status='paired_human_independent'),
                'unknown_timing':product_decision(**{**base,'timing_calibrated':False},validation_status='paired_human_independent'),
                'missing_frames':product_decision(**{**base,'frames_complete':False},validation_status='paired_human_independent')}}
    return result
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--out',default=None)
    args=p.parse_args()
    output=json.dumps(run(),indent=2,sort_keys=True)
    if args.out: Path(args.out).write_text(output+'\n')
    print(output)
