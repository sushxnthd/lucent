# E002-379 independent standard-library synthetic instrument
import math, random, json
A=12000.0;e=0.005;H=7/300;theta=.2
def aperture(t):
    depth=.85;T=math.pi*depth/50
    for j in range(5):
        s=t-(.08+.20*j)
        if 0<=s<=T:return 1-depth*math.sin(math.pi*s/T)**2
    return 1.0
def speed_bound(t,z,k):
    return max(abs(z[i+k]-z[i])/(t[i+k]-t[i])+A*(t[i+k]-t[i])/2+2*e/(t[i+k]-t[i]) for i in range(len(t)-k))
def run(rate,noise='zero',seed=379):
    rng=random.Random(seed)
    t=[i/rate for i in range(rate+1)]
    z=[aperture(x) for x in t]
    if noise=='alternating':z=[v+e*(-1)**i for i,v in enumerate(z)]
    if noise=='uniform':z=[v+rng.uniform(-e,e) for v in z]
    bounds=[(speed_bound(t,z,k),k) for k in range(1,17)]
    adjacent=bounds[0][0];best,k=min(bounds)
    assert best>=50-1e-8
    return {'rate':rate,'noise':noise,'adjacent':adjacent,'multiscale':best,'best_k':k,
            'adjacent_cert':adjacent*H<2*(1-theta),
            'multiscale_cert':best*H<2*(1-theta)}
results=[run(rate,noise) for rate in (240,600,800,1200,2400) for noise in ('zero','alternating','uniform')]
r={x['rate']:x for x in results if x['noise']=='zero'}
assert not r[240]['adjacent_cert']
assert r[800]['adjacent_cert']
assert not r[2400]['adjacent_cert'] and r[2400]['multiscale_cert']
print(json.dumps({'status':'PASS','runs':len(results),'frozen_crossing':[r[i] for i in (240,800,2400)]},indent=2))
