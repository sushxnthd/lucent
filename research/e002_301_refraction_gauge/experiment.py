import numpy as np
from scipy.linalg import eigvals
rng=np.random.default_rng(301)
def c(r):return np.diag([1.,1.,-r*r])
def t(C,H):
 J=np.linalg.inv(H);return J.T@C@J
def ratio(P,I):
 a=eigvals(P,I).real
 i,j,k=min([(0,1,2),(0,2,1),(1,2,0)],key=lambda x:abs(a[x[0]]-a[x[1]]))
 return np.sqrt(a[k]/((a[i]+a[j])/2))
e=0.
for _ in range(1000):
 q=rng.uniform(.25,.7);k=rng.uniform(.97,1.03)
 H=np.eye(3);H[:2,:2]=rng.normal(size=(2,2))+2*np.eye(2)
 H[:2,2]=rng.uniform(-.5,.5,2);H[2,:2]=rng.uniform(-.25,.25,2)
 I=t(c(1),H);P=t(c(q),H@np.diag([k,k,1]))
 e=max(e,abs(ratio(P,I)-q*k))
assert e<1e-9
print('1000 synthetic conic trials passed',e)
