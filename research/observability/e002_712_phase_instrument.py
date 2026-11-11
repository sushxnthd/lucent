"""E002-712 synthetic phase experiment; not human calibration."""
import argparse, json, random

def triangle(t, center, halfwidth):
    return max(0.0, 1.0-abs(t-center)/halfwidth)

def integrate_deficit(start, duration, center, halfwidth):
    end=start+duration
    cuts=sorted(set([start,end]+[x for x in (center-halfwidth,center,center+halfwidth) if start<x<end]))
    return sum((b-a)*(triangle(a,center,halfwidth)+triangle(b,center,halfwidth))/2 for a,b in zip(cuts,cuts[1:]))

def trial(seed, n, shutter, halfwidth, noise, phase_span, offset):
    rng=random.Random(seed)
    false_exclusions=0; detections=0; ambiguous=0
    for _ in range(n):
        phase=rng.uniform(-phase_span/2,phase_span/2)
        deficit=integrate_deficit(phase,shutter,0.0,halfwidth)/shutter
        lo=deficit-noise-abs(offset)
        hi=deficit+noise+abs(offset)
        if lo>0: detections+=1
        elif hi<0: false_exclusions+=1
        else: ambiguous+=1
    return dict(seed=seed,n=n,detect=detections,ambiguous=ambiguous,false_exclusions=false_exclusions,status='SYNTHETIC_ONLY')

def selftest():
    assert abs(integrate_deficit(-1,2,0,0.5)-0.5)<1e-12
    assert integrate_deficit(2,1,0,0.5)==0
    assert abs(integrate_deficit(-0.25,0.5,0,0.5)-0.375)<1e-12
    assert trial(3,100,1,0.2,0,4,0)['ambiguous']>0
    assert trial(3,100,1,0.2,1,4,0)['detect']==0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=712);p.add_argument('--n',type=int,default=10000)
    a=p.parse_args();selftest()
    print(json.dumps({'test':'PASS','ideal':trial(a.seed,a.n,1,.2,0,4,0),'bounded_nuisance':trial(a.seed,a.n,1,.2,.05,4,.05),'unbounded_nuisance':trial(a.seed,a.n,1,.2,1,4,0)},sort_keys=True))
