"""E002-724: preregistered physical shutter experiment schedule; no measured data."""
import argparse,csv,hashlib,json,random
from pathlib import Path

RATES=(15,24,30,60)
NUISANCES=('baseline','dim','bright','blur','gaze','glasses','occlusion')
PHASES=16

def build(seed,replicates):
    if replicates<1 or replicates>1000: raise ValueError('replicates must be 1..1000')
    rows=[]
    for rate in RATES:
        for nuisance in NUISANCES:
            for rep in range(replicates):
                for phase in range(PHASES):
                    rows.append(dict(trial_id=f'P{rate}-{nuisance}-{rep:03d}-{phase:02d}',
                        target_fps=rate,nuisance=nuisance,replicate=rep,
                        phase_fraction=f'{phase}/16',
                        ground_truth_source='independent_sensor',
                        reference_status='UNMEASURED',
                        certificate_status='ABSTAIN_UNCALIBRATED'))
    rng=random.Random(seed)
    rng.shuffle(rows)
    for order,row in enumerate(rows): row['randomized_order']=order
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,required=True)
    p.add_argument('--replicates',type=int,default=2);p.add_argument('--output',required=True)
    a=p.parse_args(); rows=build(a.seed,a.replicates)
    dest=Path(a.output)
    if dest.exists(): p.error('refusing to overwrite existing manifest')
    with dest.open('x',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    digest=hashlib.sha256(dest.read_bytes()).hexdigest()
    print(json.dumps(dict(trials=len(rows),sha256=digest,seed=a.seed,replicates=a.replicates)))

if __name__=='__main__':
    assert len(build(0,2))==4*7*2*16
    assert build(42,1)==build(42,1)
    assert len({r['trial_id'] for r in build(1,2)})==len(build(1,2))
    main()
