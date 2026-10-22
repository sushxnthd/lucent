"""Independent checker of E002-365: exact fractions, random LPs, nullspace collisions."""
from fractions import Fraction as Q
import numpy as np
from scipy.optimize import linprog

def moment(path,window):
    return sum((max(Q(0),min(b,window[1])-max(a,window[0])) for a,b in path),Q(0))
A=[(Q(0),Q(2,5)),(Q(3,5),Q(1))]
B=[(Q(0),Q(1,5)),(Q(2,5),Q(3,5)),(Q(4,5),Q(1))]
W=[(Q(0),Q(3,5)),(Q(2,5),Q(1))]
assert sum((b-a for a,b in A),Q(0))==Q(4,5)
assert sum((b-a for a,b in B),Q(0))==Q(3,5)
checks=0
for w in W:
    assert moment(A,w)==moment(B,w)==Q(2,5)
    checks+=1

for j in range(500):
    rng=np.random.default_rng(j)
    L,M,R=rng.uniform(.05,1,size=3)
    l,m,r=rng.uniform(0,1,size=3)*[L,M,R]
    y1=l+m; y2=m+r
    mlo=max(0.,y1-L,y2-R); mhi=min(M,y1,y2)
    for sign,target in [(1,y1+y2-mhi),(-1,y1+y2-mlo)]:
        sol=linprog(sign*np.ones(3),A_eq=[[1,1,0],[0,1,1]],b_eq=[y1,y2],bounds=[(0,L),(0,M),(0,R)],method='highs')
        assert sol.success and abs(sum(sol.x)-target)<1e-7
        checks+=1

for seed in range(150):
    rng=np.random.default_rng(seed+2000)
    n=int(rng.integers(3,12)); m=int(rng.integers(1,n))
    K=rng.integers(0,2,size=(m,n)).astype(float)
    if not K.any():continue
    w=np.ones(n)
    h=w-K.T@np.linalg.lstsq(K.T,w,rcond=None)[0]
    if np.linalg.norm(h)>1e-7:
        assert np.linalg.norm(K@h)<1e-7
        x0=.5*np.ones(n); x1=x0+(.4/np.max(np.abs(h)))*h
        assert min(x1)>-1e-7 and max(x1)<1+1e-7
        assert np.allclose(K@x0,K@x1,atol=1e-7)
        assert abs(w@(x0-x1))>1e-7
        checks+=1

# Independently assemble 7-row shutter matrix (no imports from model.py).
windows=[]
for k in range(31):
    for off in np.arange(7)*.004:
        a=k/30.+off
        if a<1.-1e-10:windows.append((a,min(1.,a+.010)))
edges=np.unique(np.round(np.r_[0.,1.,np.array(windows).ravel()],12))
widths=np.diff(edges)
M=np.array([[max(0.,min(b,r)-max(a,l)) for l,r in zip(edges[:-1],edges[1:])] for a,b in windows])
assert np.all(M.sum(axis=0)>1e-10)
y=M@(.5*np.ones(len(widths)))
vals=[]
for sign in (1,-1):
    result=linprog(sign*widths,A_eq=M,b_eq=y,bounds=(0,1),method='highs')
    assert result.success and np.max(np.abs(M@result.x-y))<1e-7
    vals.append(widths@result.x)
assert abs(vals[0]-.430333333333333)<1e-7 and abs(vals[1]-.569666666666667)<1e-7
checks+=1
print('independent checks passed:',checks,'full coverage interval:',vals)
