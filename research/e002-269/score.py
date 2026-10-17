#!/usr/bin/env python3
"""E002-269: reference-blind five-second admission and complete-denominator scoring.

Diagnostic evaluator only. Human product certification requires an independent
clock/source audit that no SHA-256 digest or manifest string can establish.
"""
import argparse
import hashlib
import json
import math
import pathlib
import random
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research' / 'e002-267'))
sys.path.insert(0, str(ROOT / 'research' / 'e002-268'))
from evaluate import load, fit, corr, sd, avg, lag, FEATURES, G, admit_provenance
from strict_gate import blind_windows, verify_human_source


def percentile(xs, p):
    if not xs: return None
    s = sorted(xs)
    return s[min(len(s)-1, max(0, math.floor(p*(len(s)-1)))]


def score(rows, manifest, raw_path=None, clock_evidence_path=None):
    # Metadata admission is necessary for schema consistency, not sufficient
    # for physiological clock/source truth. Human bytes are checked separately.
    admit_provenance(manifest, rows)
    human = manifest.get('data_type') == 'human'
    verified_bytes = verify_human_source(manifest, raw_path, clock_evidence_path)
    fps = float(manifest['camera_fps'])
    blind = blind_windows(rows, fps)
    if not blind: raise ValueError('NO_TEST_WINDOWS')
    # The uncertainty budget must be independent of the pupil waveform under test.
    u = manifest.get('independent_clock_error_bound_s')
    if u is not None:
        u = float(u)
        if not math.isfinite(u) or u < 0: raise ValueError('BAD_CLOCK_BOUND')
    tr = [r for r in rows if r['split']=='train' and r['valid_ref']=='1']
    if len(tr)<20: raise ValueError('NO_TRAIN_CALIBRATION')
    models={k:fit([r[k] for r in tr],[r['reference_mm'] for r in tr]) for k in FEATURES}
    groups=defaultdict(list)
    for r in rows:
        if r['split']=='test': groups[(r['participant_id'],r['session_id'])].append(r)
    chunks={}
    for (p,s),g in groups.items():
        g=sorted(g,key=lambda r:r['t_rgb_s'])
        if len({r['t_rgb_s'] for r in g}) != len(g):raise ValueError('DUPLICATE_TIMESTAMP')
        start=g[0]['t_rgb_s']
        for r in g:
            key=(p,s,int((r['t_rgb_s']-start+1e-8)//5))
            chunks.setdefault(key,[]).append(r)
    windows=[]
    for key, admit in sorted(blind.items()):
        p,s,wi=key
        chunk=chunks[key]
        w=dict(participant=p,session=s,window=wi,admitted=bool(admit),
               accurate=False,scorable=False,reason='RGB_QUALITY_REJECTED')
        if not admit:
            windows.append(w);continue
        valid=[r for r in chunk if r['valid_ref']=='1']
        if len(valid) < .8*round(5*fps):
            w['reason']='REFERENCE_UNSCORABLE';windows.append(w);continue
        ref=[r['reference_mm'] for r in valid]
        if sd(ref)<1e-12:
            w['reason']='CONSTANT_REFERENCE';windows.append(w);continue
        metrics={}
        for f in FEATURES:
            a,b=models[f]
            pred=[a*r[f]+b for r in valid]
            metrics[f]=dict(r=corr(pred,ref),amplitude=sd(pred)/sd(ref),
                nrmse=math.sqrt(avg([(x-y)**2 for x,y in zip(pred,ref)]))/sd(ref))
        pred=[models['rgb_ratio'][0]*r['rgb_ratio']+models['rgb_ratio'][1] for r in valid]
        r_pred=metrics['rgb_ratio']['r']
        nuisances=[v['r'] for k,v in metrics.items() if k!='rgb_ratio' and v['r'] is not None]
        nuisance=max(nuisances) if nuisances else -1.0
        measured_lag=lag(pred,ref,[r['t_rgb_s'] for r in valid],fps)
        clock_ok=u is not None and measured_lag is not None and measured_lag+u<=G['lag_s']+1e-12
        a=metrics['rgb_ratio']['amplitude'];e=metrics['rgb_ratio']['nrmse']
        accurate=(r_pred is not None and r_pred>=G['r'] and clock_ok and
                  G['amp_lo']<=a<=G['amp_hi'] and e<=G['nrmse'] and
                  r_pred>=nuisance+G['nuisance_margin'])
        w.update(scorable=True,accurate=bool(accurate),reason='PASS' if accurate else 'WAVEFORM_OR_CLOCK_FAIL',
                 metrics=metrics,nuisance_r=nuisance,measured_lag_s=measured_lag,
                 clock_error_bound_s=u,lag_certified=clock_ok)
        windows.append(w)
    admitted=[w for w in windows if w['admitted']]
    scored=[w for w in admitted if w['scorable']]
    passed=sum(w['accurate'] for w in admitted)
    # Bootstrap participants, retaining every admitted window and every failure.
    by_p=defaultdict(list)
    for w in windows: by_p[w['participant']].append(w)
    ids=sorted(by_p)
    rng=random.Random(269)
    acc_samples=[];r_samples=[]
    for _ in range(2000):
        draw=[w for _ in ids for w in by_p[rng.choice(ids)]]
        a=[w for w in draw if w['admitted']]
        if not a: acc_samples.append(0.0);continue
        acc_samples.append(sum(w['accurate'] for w in a)/len(a))
        # Do not pretend missing reference is a high correlation.
        r_values=[w['metrics']['rgb_ratio']['r'] for w in a if w['scorable'] and
                  w['metrics']['rgb_ratio']['r'] is not None]
        if r_values:r_samples.append(avg(r_values))
    tr_all=[r for r in rows if r['split']=='train']
    test=[r for r in rows if r['split']=='test']
    holdouts={k:bool(tr_all and test and set(r[k] for r in tr_all).isdisjoint(set(r[k] for r in test)))
              for k in ('device','lighting','glasses')}
    holdouts['participant']=not bool(set(r['participant_id'] for r in tr_all) &
                                   set(r['participant_id'] for r in test))
    coverage=len(admitted)/len(windows)
    accuracy=passed/len(admitted) if admitted else 0
    r_ci=[percentile(r_samples,.025),percentile(r_samples,.975)] if r_samples else None
    acc_ci=[percentile(acc_samples,.025),percentile(acc_samples,.975)] if acc_samples else None
    statistical_candidate=bool(human and verified_bytes and u is not None and
        len(ids)>=8 and accuracy>=G['min_accuracy'] and coverage>=G['min_coverage'] and
        r_ci and r_ci[0]>=G['r'] and all(holdouts.values()))
    return dict(run='E002-269',source_type=manifest['data_type'],
        human_bytes_hash_verified=verified_bytes,clock_error_bound_s=u,
        test_participants=len(ids),test_windows=len(windows),blind_admitted=len(admitted),
        blind_coverage=coverage,scorable_admitted=len(scored),
        unscorable_admitted=len(admitted)-len(scored),passed=passed,
        conditional_accuracy=accuracy,participant_bootstrap_accuracy_ci95=acc_ci,
        participant_bootstrap_mean_r_ci95=r_ci,holdouts=holdouts,
        statistical_candidate=statistical_candidate,
        product_certificate=False,
        certification_blocker='REQUIRES_EXTERNAL_INDEPENDENT_CLOCK_AND_REFERENCE_LINEAGE_AUDIT',
        windows=windows)


def main():
    a=argparse.ArgumentParser()
    a.add_argument('--csv',required=True);a.add_argument('--manifest',required=True)
    a.add_argument('--out',required=True);a.add_argument('--raw');a.add_argument('--clock')
    x=a.parse_args()
    rows=load(x.csv);manifest=json.loads(pathlib.Path(x.manifest).read_text())
    out=score(rows,manifest,x.raw,x.clock)
    out['input_sha256']={k:hashlib.sha256(pathlib.Path(v).read_bytes()).hexdigest()
         for k,v in (('csv',x.csv),('manifest',x.manifest))}
    pathlib.Path(x.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='windows'},indent=2,sort_keys=True))

if __name__=='__main__':main()
