"""E002-745 fixed-seed synthetic held-out shutter-gap test; no human or instrument evidence."""
import random, csv, argparse
from pathlib import Path
SEED=745
def trial(rng,program):
    gap=rng.uniform(.015,.055) if program=='A' else rng.uniform(.035,.085)
    v=rng.uniform(.5,1.)
    center=rng.uniform(0,gap)
    floor=rng.choice([0.,rng.uniform(.001,.02)])
    a0=floor+v*center; a1=floor+v*(gap-center)
    e0=rng.uniform(-.003,.003);e1=rng.uniform(-.003,.003)
    l0=max(0,a0+e0-.003);l1=max(0,a1+e1-.003)
    D=gap+.002
    return dict(program=program,gap=gap,a0=a0,a1=a1,l0=l0,l1=l1,D=D,hidden=int(floor==0.),exclude=int(l0+l1>D),naive=int(a0+e0+a1+e1>.35/30))
def run(n=10000):
    rng=random.Random(SEED)
    a=[trial(rng,'A') for _ in range(n)];b=[trial(rng,'B') for _ in range(n)]
    def stats(rows):
        return {k:sum(r[k] for r in rows) for k in ('hidden','exclude','naive')} | {'false_exclusions':sum(r['hidden'] and r['exclude'] for r in rows),'naive_false_exclusions':sum(r['hidden'] and r['naive'] for r in rows)}
    return a,b,stats(a),stats(b)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=10000);p.add_argument('--csv',type=Path)
    args=p.parse_args();a,b,sa,sb=run(args.n)
    print('seed',SEED,'calibration',sa,'heldout',sb)
    assert sa['false_exclusions']==sb['false_exclusions']==0
    if args.csv:
        with args.csv.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=b[0]);w.writeheader();w.writerows(b)
