"""E002-382 ideal scalar shutter model; synthetic, not human/RGB evidence."""
import math,random,json
from pathlib import Path

def edge_bound(b,w,v):
    if not (0<=b<=1 and w>0 and v>0):raise ValueError
    q=v*w
    if q<=1 and b<=1-q/2:return max(0.,b-q/2)
    return max(0.,1-math.sqrt(2*q*(1-b)))

def gap_bound(l,r,h,v):
    q=h*v
    return max(0.,l-q,r-q,(l+r-q)/2)

def qualify(b1,b2,w,h,v,theta,eps=0.,clock=0.,calibrated=True):
    vals=[b1,b2,w,h,v,theta,eps,clock]
    if (not calibrated or any(x is None or not math.isfinite(x) for x in vals)
        or not(0<=b1<=1 and 0<=b2<=1 and 0<=theta<=1)
        or w<=0 or h<0 or v<=0 or eps<0 or clock<0):
        return {'status':'ABSTAIN','reason':'invalid or unavailable calibration'}
    l=edge_bound(max(0.,b1-eps),w,v)
    r=edge_bound(max(0.,b2-eps),w,v)
    minimum=gap_bound(l,r,h+clock,v)
    return {'status':'CERTIFIED_GAP_ONLY' if minimum>theta else 'ABSTAIN',
            'lower_aperture':round(minimum,12),'margin':round(minimum-theta,12)}

def independently_invert_mean(b,w,v):
    def mean(y):
        r=(1-y)/v
        return y+v*w/2 if r>=w else (y*r+v*r*r/2+w-r)/w
    if mean(0)>=b:return 0.
    lo,hi=0.,1.
    for _ in range(80):
        mid=(lo+hi)/2
        if mean(mid)<b:lo=mid
        else:hi=mid
    return (lo+hi)/2

def independent_witness(b,w,v,h,theta,n=20000):
    y=independently_invert_mean(b,w,v)
    def left(t):return min(1.,y+v*(w-t))
    def right(t):return min(1.,y+v*t)
    def avg(f):
        dt=w/n
        return (0.5*(f(0)+f(w))+sum(f(i*dt) for i in range(1,n)))*dt/w
    return {'edge':y,'left_mean':avg(left),'right_mean':avg(right),
            'min_gap':max(0.,y-v*h/2),
            'closed_duration_s':max(0.,h-2*(y-theta)/v)}

def run():
    v,w,b,theta,F=60.,.01,.995,.2,1/30
    h=F-w
    tests={'nominal':qualify(b,b,w,h,v,theta),
           'actual_plus_1ms':qualify(b,b,w,h+.001,v,theta),
           'mean_error_nominal':qualify(b,b,w,h,v,theta,eps=.002),
           'mean_error_plus_0_3ms':qualify(b,b,w,h+.0003,v,theta,eps=.002)}
    assert [x['status'] for x in tests.values()]==['CERTIFIED_GAP_ONLY','ABSTAIN','CERTIFIED_GAP_ONLY','ABSTAIN'],tests
    witness=independent_witness(b,w,v,h+.001,theta)
    assert abs(witness['left_mean']-b)<1e-8 and abs(witness['right_mean']-b)<1e-8
    assert witness['min_gap']<theta and witness['closed_duration_s']>0
    assert qualify(b,b,w,h,v,theta,clock=.001)['status']=='ABSTAIN'
    assert qualify(b,b,w,h,v,theta,calibrated=False)['status']=='ABSTAIN'
    assert qualify(b,b,w,float('nan'),v,theta)['status']=='ABSTAIN'
    assert qualify(b,b,w,h,v,theta,eps=.1)['status']=='ABSTAIN'
    rng=random.Random(382)
    hidden=bad=nominal_bad=0
    for i in range(2000):
        vv=rng.uniform(30,100); ww=rng.uniform(.004,.014)
        bb=rng.uniform(.985,.999);hh=rng.uniform(.014,.042);tt=rng.uniform(.1,.4)
        yy=independently_invert_mean(bb,ww,vv)
        is_hidden=max(0,yy-vv*hh/2)<tt
        hidden+=is_hidden
        bad+=is_hidden and qualify(bb,bb,ww,hh,vv,tt)['status']=='CERTIFIED_GAP_ONLY'
        nominal_h=max(0,hh-rng.uniform(0,.003))
        nominal_bad+=is_hidden and qualify(bb,bb,ww,nominal_h,vv,tt)['status']=='CERTIFIED_GAP_ONLY'
    assert bad==0
    result={'frozen_predictions':tests,'actual_hidden_closure_witness':witness,
            'nominal_gap_s':h,'actual_gap_s':h+.001,
            'critical_gap_s':2*(edge_bound(b,w,v)-theta)/v,
            'critical_gap_mean_error_s':2*(edge_bound(b-.002,w,v)-theta)/v,
            'randomized_unseen_trials':2000,'hidden_closure_witnesses':hidden,
            'timestamp_aware_false_certificates':bad,
            'nominal_timestamp_false_certificates':nominal_bad,
            'scope':'Only blind intervals for ideal exposure-average scalar aperture, independently calibrated V; no human or RGB evidence.'}
    Path(__file__).with_name('e002_382_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
