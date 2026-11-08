"""E002-716: conservative blinded replay gate. No physiological validation implied."""
import csv, json, math, argparse
FLAGS=('geometry_valid','photometry_valid','clock_valid','exposure_valid','missingness_valid','blur_valid','gaze_valid','glasses_valid','velocity_independent')
NUM=('aperture0_lower','aperture1_lower','velocity_upper','delta_upper')
REQ=('trial_id','participant_id','split','reference_closure','reference_valid')+NUM+FLAGS
def evaluate(rows):
    ids=set(); people={}; out=[]
    for r in rows:
        if any(k not in r for k in REQ): raise ValueError('missing column')
        tid,pid,split=(r[k].strip() for k in ('trial_id','participant_id','split'))
        if not tid or not pid or tid in ids or split not in ('calibration','heldout'): raise ValueError('bad id or split')
        ids.add(tid); people.setdefault(pid,set()).add(split)
        if any(r[k].strip() not in ('0','1') for k in FLAGS+('reference_valid','reference_closure')): raise ValueError('nonbinary flag')
        vals=[float(r[k]) for k in NUM]
        if not all(math.isfinite(v) and v>=0 for v in vals): raise ValueError('invalid bound')
        a0,a1,v,dt=vals
        cert=all(r[k].strip()=='1' for k in FLAGS) and v*dt<a0+a1
        out.append((split,cert,r['reference_valid'].strip()=='1',int(r['reference_closure']),tid))
    if any(len(s)>1 for s in people.values()): raise ValueError('participant leakage')
    held=[x for x in out if x[0]=='heldout']; scored=[x for x in held if x[2]]
    ex=[x for x in scored if x[1]]; failures=[x[4] for x in ex if x[3]]
    return dict(heldout_total=len(held),heldout_scored=len(scored),heldout_exclusions=len(ex),
        false_exclusions=len(failures),false_exclusion_trial_ids=failures,
        heldout_abstentions=sum(not (x[1] and x[2]) for x in held),reference_indeterminate=len(held)-len(scored),
        status=('FALSIFIED' if failures else 'INSUFFICIENT_EVIDENCE' if not ex else 'NO_OBSERVED_FALSIFICATION'),
        warning='No physiological validation follows from zero observed failures; nonzero exclusions are not a calibrated sample-size guarantee.')
def selftest():
    b=dict.fromkeys(REQ,'1'); b.update(trial_id='a',participant_id='p',split='heldout',aperture0_lower='1',aperture1_lower='1',velocity_upper='1',delta_upper='1')
    assert evaluate([b])['status']=='FALSIFIED'
    assert evaluate([dict(b,delta_upper='2')])['heldout_exclusions']==0
    assert evaluate([dict(b,clock_valid='0')])['heldout_exclusions']==0
    assert evaluate([dict(b,reference_valid='0')])['heldout_scored']==0
    for bad in ([b,dict(b,trial_id='b',split='calibration')],[dict(b,velocity_upper='nan')]):
        try: evaluate(bad)
        except ValueError: pass
        else: raise AssertionError('invalid trial accepted')
    print('PASS: six replay self-tests')
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('csv',nargs='?'); p.add_argument('--selftest',action='store_true'); a=p.parse_args()
    if a.selftest: selftest()
    elif a.csv:
        with open(a.csv,newline='',encoding='utf8') as f: print(json.dumps(evaluate(csv.DictReader(f)),indent=2))
    else: p.error('provide CSV or --selftest')
