"""Independent gap-occupancy check, no dependency on model.py."""
import json,math,random
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent
def B(E,V,m):
 return min(1.,math.sqrt(2*V*E*m) if m<=V*E/2 else m+V*E/2)
def occupancy(E0,E1,G,U,D,m0,m1,theta):
 b0,b1=B(E0,U,m0),B(E1,D,m1)
 return max(0.,G-max(0.,theta-b0)/U-max(0.,theta-b1)/D)
def sample(E0,E1,G,U,D,m0,m1,theta,n=10000):
 b0,b1=B(E0,U,m0),B(E1,D,m1)
 t=(np.arange(n)+.5)*G/n
 return G*np.count_nonzero(np.minimum(1.,np.minimum(b0+U*t,b1+D*(G-t)))>=theta)/n
def run():
 random.seed(322);maximum=0.
 for i in range(500):
  p=(random.uniform(.003,.03),random.uniform(.003,.03),random.uniform(.001,.06),random.uniform(2,22),random.uniform(2,22),random.uniform(.0001,.08),random.uniform(.0001,.08))
  theta=random.uniform(.02,.98)
  a,b=occupancy(*p,theta),sample(*p,theta)
  maximum=max(maximum,abs(a-b))
  assert abs(a-b)<=p[2]/10000+1e-12
 print(json.dumps({'pass':True,'n_cases':500,'max_error_s':maximum},indent=2))
if __name__=='__main__':run()
