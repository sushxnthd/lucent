"""Independent discretized LP checker for E002-321, synthetic only."""
import json,math,random
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

def endpoint(E,L,mu):
    return min(1.,math.sqrt(2*L*E*mu) if mu<=L*E/2 else mu+L*E/2)

def analytic(P,E,L,mu):
    return min(1.,endpoint(E,L,mu)+L*(P-E)/2)

def lp(P,E,L,mu,ne=100,ng=100):
    G=P-E
    x=np.r_[np.linspace(-E,0,ne+1),np.linspace(0,G,ng+1)[1:],np.linspace(G,G+E,ne+1)[1:]]
    row=[];col=[];data=[];rhs=[]
    def add(entries,b):
        j=len(rhs);rhs.append(b)
        for k,v in entries.items():
            row.append(j);col.append(k);data.append(v)
    for i in range(len(x)-1):
        d=L*(x[i+1]-x[i])
        add({i:1.,i+1:-1.},d);add({i:-1.,i+1:1.},d)
    add({i:(.5 if i in (0,ne) else 1.)*E/ne for i in range(ne+1)},mu*E)
    j=ne+ng
    add({j+i:(.5 if i in (0,ne) else 1.)*E/ne for i in range(ne+1)},mu*E)
    A=coo_matrix((data,(row,col)),shape=(len(rhs),len(x))).tocsr()
    obj=np.zeros(len(x));obj[ne+ng//2]=-1.
    res=linprog(obj,A_ub=A,b_ub=np.array(rhs),bounds=(0,1),method="highs")
    assert res.success,res.message
    return -res.fun

def verify():
    cases=[(1/30,.01,12,.01),(1/30,1/60,12,.01),(1/24,.008,10,.005),(.1,.02,4,.08),(.05,.02,5,.01),(.03,.015,2,.1)]
    errs=[]
    for p,e,l,m in cases:
        diff=abs(lp(p,e,l,m)-analytic(p,e,l,m))
        assert diff<4e-4,(p,e,l,m,diff)
        errs.append(diff)
    random.seed(321)
    for i in range(500):
        p=random.uniform(.018,.12);e=random.uniform(.2,.9)*p
        l=random.uniform(.5,25);m=random.uniform(.00001,.2)
        b=endpoint(e,l,m)
        area=b*b/(2*l) if b<=l*e else b*e-l*e*e/2
        assert area/e<=m+1e-12
    held=analytic(1/24,.008,10,.005)
    assert abs(held-.19661760458079525)<1e-13
    assert .19<held<.20
    baseline=analytic(1/30,.01,12,.01)
    missing=analytic(2/30,.01,12,.01)
    assert missing>baseline
    return {"pass":True,"LP_cases":len(cases),"witness_checks":500,"max_abs_LP_error":max(errs),"frozen_synthetic_boundary":held,"missingness_boundary":missing}
if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
