"""E002-384 frozen synthetic instrument: frame-vs-clip calibration and selective certification.
Run: python e002_384_clip_calibration.py --output DIR
Synthetic-only: no human measurements, no camera hardware.
"""
import argparse, json, math
from pathlib import Path
import numpy as np

SEED = 20261023
N_CAL, N_ID, N_SHIFT, FRAMES = 500, 1000, 1000, 60
FPS, W, V, THRESH = 30.0, 0.010, 40.0, 0.20
N_EXPOSURE = 41  # 0.25 ms integration grid

def aperture(t, centers, plateaus):
    # piecewise-linear, exactly V-Lipschitz, independent ground truth
    t = np.asarray(t)
    a = np.ones_like(t, dtype=float)
    ramp = .95/V
    for c,p in zip(centers,plateaus):
        # down ramp, closed plateau, up ramp
        q = np.abs(t-c)-p/2
        event = np.clip(q/ramp, 0, 1)
        a = np.minimum(a, .05+.95*event)
    return a

def endpoint_lower(b, e):
    b = np.maximum(0, np.asarray(b)-e)
    eta = 1-b
    d = np.where(eta <= V*W/2, np.sqrt(2*V*W*eta), eta+V*W/2)
    return np.maximum(0, 1-np.minimum(1,d))

def wilson(k,n):
    if n==0:return [None,None]
    z=1.959963984540054
    p=k/n; d=1+z*z/n
    c=(p+z*z/(2*n))/d
    h=z*math.sqrt((p*(1-p)+z*z/(4*n))/n)/d
    return [float(c-h),float(c+h)]

def synth(rng, n, shifted):
    starts = np.arange(FRAMES)/FPS
    # Instrument observes shutter-average f(aperture), not f(shutter-average aperture).
    offsets = np.linspace(0,W,N_EXPOSURE)
    ests = np.empty((n,FRAMES)); truth = np.empty_like(ests)
    mins = np.empty((n,FRAMES-1)); speeds = np.empty(n)
    glare_flags = np.empty((n,FRAMES),dtype=bool)
    for i in range(n):
        # 3 blinks/2 s, separated so no overlapping ramps
        centers=np.array([.32,.94,1.57])+rng.uniform(-.09,.09,3)
        plateaus=rng.uniform(.004,.055,3)
        tt=starts[:,None]+offsets[None,:]
        aa=aperture(tt,centers,plateaus)
        truth[i]=np.trapezoid(aa,offsets,axis=1)/W
        # Physical camera: nonlinear photometric transfer BEFORE shutter integration.
        z=np.trapezoid(aa**.8,offsets,axis=1)/W
        shared=rng.normal(0,.0035)
        ar=np.zeros(FRAMES)
        for j in range(1,FRAMES):ar[j]=.78*ar[j-1]+rng.normal(0,.0022)
        white=rng.normal(0,.0017,FRAMES)
        # Rare correlated gain/glare outliers; independent clip selection.
        glare=rng.random(FRAMES)<(.025 if shifted else .006)
        glare_flags[i]=glare
        bursts=glare*rng.choice([-1,1],FRAMES)*rng.uniform(.018,.050,FRAMES)
        shift=(.021 if shifted else 0)
        zobs=np.clip(z+shared+ar+white+bursts+shift,0,1)
        ests[i]=zobs**(1/.8)
        # Exact piecewise-linear gap minimum: evaluate gap boundaries and blink centers.
        for j in range(FRAMES-1):
            left=starts[j]+W;right=starts[j+1]
            candidates=[left,right]
            for c,p in zip(centers,plateaus):
                candidates += [x for x in (c-p/2,c+p/2,c) if left<=x<=right]
            mins[i,j]=float(aperture(np.array(candidates),centers,plateaus).min())
        speeds[i]=V
    return dict(est=ests,truth=truth,mins=mins,glare=glare_flags,speed=speeds)

def summarize(name, data, q_frame, q_clip):
    err=np.abs(data['est']-data['truth']); n=err.shape[0]
    coverage={}
    for label,q in [('frame99',q_frame),('clip95',q_clip)]:
        good=err<=q
        all_good=good.all(axis=1)
        gap_low_l=endpoint_lower(data['est'][:,:-1],q)
        gap_low_r=endpoint_lower(data['est'][:,1:],q)
        H=1/FPS-W
        lower=np.maximum.reduce([gap_low_l-V*H, gap_low_r-V*H,(gap_low_l+gap_low_r-V*H)/2])
        cert=lower>THRESH
        actual_hidden=data['mins']<=THRESH
        false=cert & actual_hidden
        # Unknown camera shift, optical glare, or invalid calibration => production gate abstains.
        domain_valid = (name != 'unseen_camera')
        candidate_eligible=cert & domain_valid & (~data['glare'][:,:-1]) & (~data['glare'][:,1:])
        # Finite-sample residual quantiles are NOT hard optical bounds. Fail closed.
        hard_optical_bound_validated=False
        gate_cert=candidate_eligible & hard_optical_bound_validated
        coverage[label]={
            'error_bound':float(q),
            'covered_frames':int(good.sum()),'total_frames':int(good.size),
            'frame_coverage':float(good.mean()),
            'fully_covered_clips':int(all_good.sum()),'total_clips':int(n),
            'clip_coverage':float(all_good.mean()),
            'clip_coverage_wilson95':wilson(int(all_good.sum()),n),
            'naive_certified_gaps':int(cert.sum()),
            'naive_false_certified_gaps':int(false.sum()),
            'naive_false_certified_clips':int(false.any(axis=1).sum()),
            'naive_certified_clip_count':int(cert.any(axis=1).sum()),
            'candidate_eligible_gaps_before_hard_bound_gate':int(candidate_eligible.sum()),
            'hard_optical_bound_validated':bool(hard_optical_bound_validated),
            'gated_certified_gaps':int(gate_cert.sum()),
            'gated_false_certified_gaps':int((gate_cert & actual_hidden).sum()),
            'gated_abstention_fraction':float(1-gate_cert.mean()),
            'actual_hidden_gap_count':int(actual_hidden.sum())
        }
    return coverage

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='.')
    args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(SEED)
    cal=synth(rng,N_CAL,False)
    residual=np.abs(cal['est']-cal['truth'])
    qf=float(np.quantile(residual,.99,method='higher'))
    qc=float(np.quantile(residual.max(axis=1),.95,method='higher'))
    idtest=synth(rng,N_ID,False)
    shift=synth(rng,N_SHIFT,True)
    results={
        'seed':SEED,'sample_sizes':{'calibration_clips':N_CAL,'in_domain_clips':N_ID,'unseen_camera_clips':N_SHIFT,'frames_per_clip':FRAMES},
        'instrument':{'fps':FPS,'exposure_s':W,'reference_integral_grid_points':N_EXPOSURE,'aperture_speed_limit_per_s':V,'closure_threshold':THRESH,'response_gamma':.8},
        'calibration':{'frame99':qf,'clip95':qc,'frame99_calibration_coverage':float((residual<=qf).mean()),'clip95_calibration_coverage':float((residual.max(axis=1)<=qc).mean())},
        'in_domain':summarize('in_domain',idtest,qf,qc),
        'unseen_camera':summarize('unseen_camera',shift,qf,qc),
        'limits':'All data synthetic; fixed camera response and known physiological speed; no hardware or human validation; quantile envelopes are statistical, not deterministic.'
    }
    (out/'e002_384_results.json').write_text(json.dumps(results,indent=2)+'\n')
    # Save small, self-contained audit samples, not private human recordings.
    np.savez_compressed(out/'e002_384_audit_sample.npz',
        calibration_residual=residual[:10],
        in_domain_aperture_truth=idtest['truth'][:10],
        in_domain_aperture_est=idtest['est'][:10],
        in_domain_gap_min=idtest['mins'][:10],
        unseen_aperture_truth=shift['truth'][:10],
        unseen_aperture_est=shift['est'][:10])
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
