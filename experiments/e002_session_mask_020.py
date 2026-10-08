"""E002-020: exact randomization and session-shared missingness adversary.
SYNTHETIC ONLY. No human/phone data. Run: python experiments/e002_session_mask_020.py
Requires numpy. Predeclared seed and 500 Monte Carlo draws per cell.
"""
import itertools, json
import numpy as np
T=np.arange(101)*0.05
def wave(t,r):
    return 0.5+0.08*np.sin(2*np.pi*t/5)+0.03*np.sin(4*np.pi*t/5)+(r-1)*0.00005*t/5+0.00005*r*np.sin(3.2*t+0.4)
def center(y):return y-np.median(y[T<=0.40])
def score(g):
    def d(a,b):return np.sqrt(np.mean((a-b)**2))
    wi=[d(a,b) for x in (g[:3],g[3:]) for a,b in itertools.combinations(x,2)]
    be=[d(a,b) for a in g[:3] for b in g[3:]]
    return float(np.median(be)/np.median(wi))
def perm(g):
    observed=score(g)
    unpaired=[score([g[i] for i in range(6) if i in x]+[g[i] for i in range(6) if i not in x]) for x in map(set,itertools.combinations(range(6),3))]
    paired=[score([g[r+3*b[r]] for r in range(3)]+[g[r+3*(1-b[r])] for r in range(3)]) for b in itertools.product((0,1),repeat=3)]
    return dict(O4=observed,unpairedExactP=float(np.mean(np.array(unpaired)>=observed-1e-10)),pairedExactP=float(np.mean(np.array(paired)>=observed-1e-10)))
def mask(rng,p):
    m=rng.random(101)>=p
    m[0]=m[-1]=True
    return m
def guard(m):
    t=T[m]
    return bool(np.max(np.diff(t))<=0.200000001 and np.mean(np.min(abs(T[:,None]-t[None,:]),axis=1)<=0.1000000001)>=0.8)
def curves(ms):
    return [center(np.interp(T,T[m],wave(T[m],i%3))) for i,m in enumerate(ms)]
def run(n=500,seed=20261008):
    ma=np.arange(101)%4!=1;mb=np.arange(101)%4!=2
    ma[[0,-1]]=True;mb[[0,-1]]=True
    periodic=perm(curves([ma]*3+[mb]*3))
    rng=np.random.default_rng(seed)
    rows=[]
    for p in (0.05,0.10,0.20):
        for mechanism in ('session_shared','replicate_independent'):
            accepted=passes=0;ratios=[]
            for _ in range(n):
                if mechanism=='session_shared':
                    a,b=mask(rng,p),mask(rng,p)
                    ms=[a]*3+[b]*3
                else:ms=[mask(rng,p) for _ in range(6)]
                if not all(guard(m) for m in ms):continue
                accepted+=1
                s=score(curves(ms));ratios.append(s);passes+=s>1.25
            rows.append(dict(dropout=p,mechanism=mechanism,accepted=accepted,trials=n,falseO4Passes=passes,rate=passes/accepted if accepted else None,medianO4=float(np.median(ratios)) if ratios else None))
    return dict(experiment='E002-020',data='SYNTHETIC IDENTICAL LATENT WAVEFORMS',seed=seed,periodic=periodic,maskOnlyLabelAccuracy=float(np.mean([int(m[1]==(i>=3)) for i,m in enumerate([ma]*3+[mb]*3)])),nonperiodic=rows,
      caution='No human effect; exact randomization assumes label exchangeability, violated by condition-specific masks. Monte Carlo rates describe only this constructed null.')
if __name__=='__main__':
    z=run()
    assert z['periodic']['unpairedExactP']==0.1
    assert z['periodic']['pairedExactP']==0.25
    print(json.dumps(z,indent=2))
