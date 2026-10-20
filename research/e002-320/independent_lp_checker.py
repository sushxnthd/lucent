"""Independent linear programming and threshold Monte Carlo for E002-320.
Requires scipy. Does not import the analytic model module.
"""
from fractions import Fraction as F
from scipy.optimize import linprog
import random,json
from pathlib import Path
rng=random.Random(731)
maxerr=0.
for _ in range(90):
    P=rng.randint(4,12);E=rng.randint(1,P);N=rng.randint(2,5)
    kept=[i for i in range(N) if rng.random()>.2] or [0]
    y=[];A=[];b=[]
    for i in kept:
        m=F(rng.randint(0,10),10);y.append(m)
        row=[0.]*(N*P)
        for j in range(i*P,i*P+E): row[j]=1./E
        A.extend([row,[-v for v in row]])
        b.extend([float(m+F(1,10)),-float(m-F(1,10))])
    lo=E*sum(max(F(0),z-F(1,10)) for z in y)/F(N*P)
    hi=(N*P-len(kept)*E+E*sum(min(F(1),z+F(1,10)) for z in y))/F(N*P)
    obj=[1./(N*P)]*(N*P)
    rl=linprog(obj,A_ub=A,b_ub=b,bounds=(0,1),method="highs")
    rh=linprog([-v for v in obj],A_ub=A,b_ub=b,bounds=(0,1),method="highs")
    assert rl.success and rh.success
    err=max(abs(rl.fun-float(lo)),abs(-rh.fun-float(hi)))
    assert err<1e-8
    maxerr=max(maxerr,err)
rng=random.Random(852)
for _ in range(300):
    P=rng.randint(4,12);E=rng.randint(1,P);N=rng.randint(2,8)
    theta=F(rng.randint(1,9),10);eta=F(rng.randint(0,10),100)
    c=[F(rng.randint(0,100),100) for _ in range(N*P)]
    kept=[i for i in range(N) if rng.random()>.25]
    ys=[]
    for i in kept:
        m=sum(c[i*P:i*P+E],F(0))/E
        ys.append(m+eta*F(rng.randint(-10,10),10))
    lower=E*sum(max(F(0),(max(F(0),z-eta)-theta)/(1-theta)) for z in ys)/F(N*P)
    upper=(N*P-len(kept)*E+E*sum(min(F(1),min(F(1),z+eta)/theta) for z in ys))/F(N*P)
    actual=F(sum(z>=theta for z in c),N*P)
    assert lower<=actual<=upper,(lower,actual,upper)
print(json.dumps({"LP_burden_trials":90,"max_lp_discrepancy":maxerr,"threshold_occupancy_trials":300,"violations":0},indent=2))
