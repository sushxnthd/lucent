import numpy as np
from itertools import combinations
from fractions import Fraction
from interval_instrument import interval

def vertex_check(y,h,n,lo,hi,eta):
    rows=[];rhs=[]
    for i in range(len(y)):
        rows.extend(([h[i],n[i]],[-h[i],-n[i]]));rhs.extend((y[i]+eta[i],-y[i]+eta[i]))
    rows.extend(([0,1],[0,-1]));rhs.extend((hi,-lo))
    A=np.array(rows);b=np.array(rhs);v=[]
    for i,j in combinations(range(len(b)),2):
        M=A[[i,j]]
        if abs(np.linalg.det(M))<1e-9:continue
        x=np.linalg.solve(M,b[[i,j]])
        if np.all(A@x<=b+1e-8):v.append(x[0])
    return min(v),max(v)

def run():
    A=Fraction(6,100);eta=Fraction(1,100)
    for B in [Fraction(4,100),Fraction(49,1000),Fraction(5,100),Fraction(55,1000)]:
        r=interval([float(A)]*2,[1,1],[[1,1],[1,-1]],[-float(B),-.02],[float(B),.02],[float(eta)]*2)
        assert abs(r["lower"]-float(A-B-eta))<1e-9
        assert abs(r["upper"]-float(A+B+eta))<1e-9
    rng=np.random.default_rng(1327)
    for i in range(200):
        h=rng.normal(size=5);n=rng.normal(size=5)
        a=rng.uniform(-.1,.1);beta=rng.uniform(-.03,.03)
        eta=rng.uniform(.02,.05,size=5);y=a*h+beta*n+rng.uniform(-eta,eta)
        x=interval(y,h,n.reshape(-1,1),[-.05],[.05],eta)
        lo,hi=vertex_check(y,h,n,-.05,.05,eta)
        assert abs(lo-x["lower"])<1e-7 and abs(hi-x["upper"])<1e-7
    for i in range(400):
        h=rng.normal(size=7);N=rng.normal(size=(7,3));beta=rng.uniform(-.1,.1,3)
        alpha=rng.uniform(-.1,.1);eta=rng.uniform(.003,.03,7)
        y=alpha*h+N@beta+rng.uniform(-eta,eta)
        x=interval(y,h,N,[-.1]*3,[.1]*3,eta)
        assert x["lower"]-1e-7<=alpha<=x["upper"]+1e-7
        for key in ("witness_lower","witness_upper"):
            w=np.array(x[key]);assert np.all(np.abs(y-np.column_stack((h,N))@w)<=eta+1e-7)
    assert interval([.06,.06],[1,1],[[1],[1]],[-np.inf],[np.inf],[.01,.01])["status"]=="unbounded"
    print("PASS: 4 rational, 200 independent vertex, 400 random feasible, 1 gauge")
if __name__=="__main__":run()
