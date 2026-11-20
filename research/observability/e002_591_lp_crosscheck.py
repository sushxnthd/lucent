#!/usr/bin/env python3
"""Independent finite-grid LP sanity check; not proof of the continuous theorem."""
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
import numpy as np
import json


def optimize(c,tau,d,L,n,k):
    m=round(d*n)
    assert abs(m/n-d)<1e-12 and 0<=k<=n-m
    obj=np.ones(n+1)/n
    obj[0]/=2;obj[-1]/=2
    A=lil_matrix((2*n,n+1))
    for i in range(n):
        A[2*i,i]=-1;A[2*i,i+1]=1
        A[2*i+1,i]=1;A[2*i+1,i+1]=-1
    bounds=[(0.,1.)]*(n+1)
    bounds[0]=bounds[-1]=(c,c)
    for i in range(k,k+m+1):bounds[i]=(0.,tau)
    result=linprog(-obj,A_ub=A.tocsr(),b_ub=np.full(2*n,L/n),bounds=bounds,method='highs')
    if not result.success:raise RuntimeError('LP infeasible: '+result.message)
    return -result.fun


def main():
    tests=[('half-zero-d10',.5,0.,.1,2.5,400,80,.5),
           ('half-zero-d25',.5,0.,.25,4.,400,50,.5),
           ('fifth-zero-d10',.2,0.,.1,80/81,400,81,.2),
           ('half-partial-d30',.5,.1,.3,81/23,400,46,.5)]
    out=[]
    for name,c,tau,d,L,n,k,expected in tests:
        v=optimize(c,tau,d,L,n,k)
        tol=1e-9 if name!='half-partial-d30' else .003
        assert v<=expected+1e-8 and abs(v-expected)<tol,(name,v,expected)
        out.append({'case':name,'grid_nodes':n+1,'max_mean':round(v,9),'target':expected})
    print(json.dumps({'experiment':'E002-591','independent_lp':'PASS',
                      'evidence_tier':'NUMERICAL_GRID_SANITY_ONLY','cases':out},sort_keys=True))

if __name__=='__main__':main()
