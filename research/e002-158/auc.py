import numpy as np
from scipy.stats import rankdata
def auc(p,n):
 a=np.r_[np.asarray(p,dtype=float),np.asarray(n,dtype=float)]
 k=len(p);j=len(n)
 if k==0 or j==0:return float("nan")
 return float((rankdata(a,method="average")[:k].sum()-k*(k+1)/2)/(k*j))
def check():
 assert auc([2,3],[0,1])==1
 assert auc([0,1],[2,3])==0
 assert auc([1,1],[1,1])==.5
