"""Independent minimal checker for Lucent E002-367."""
from fractions import Fraction as F
import math
import numpy as np
from scipy.optimize import linprog
a,b=F(9,20),F(1,2)
assert a*F(20,19)==b*F(18,19)==F(9,19)
assert a*(1+F(4,95))+F(1,200)==b*(1-F(4,95))-F(1,200)
checks=2
for amp in (.005,.03,.15,.35):
    for freq in (.5,2,7):
        ph=np.linspace(0,2*math.pi,150001)
        observed=np.max(abs(amp*2*math.pi*freq*np.cos(ph)/(1+amp*np.sin(ph))))
        exact=2*math.pi*freq*amp/math.sqrt(1-amp*amp)
        assert abs(observed-exact)<2e-7
        checks+=1
rng=np.random.default_rng(3672)
for _ in range(500):
    t=rng.uniform(-1,1);c=math.cos(t);s=math.sin(t)
    H=np.array([[1.1*c,-.8*s,rng.uniform(-.3,.3)],
      [1.1*s,.8*c,rng.uniform(-.3,.3)],
      [rng.uniform(-.1,.1),rng.uniform(-.1,.1),1.]])
    J=np.linalg.inv(H)
    P=J.T@np.diag([1,1,-.52**2])@J
    I=J.T@np.diag([1,1,-1])@J
    eig=np.linalg.eigvals(np.linalg.solve(P,I))
    assert sum(abs(eig-1)<1e-9)==2 and min(abs(eig-1/.52**2))<1e-9
    checks+=1
t=np.arange(21)/10
assert max(abs(np.sin(2*math.pi*2*t)-np.sin(2*math.pi*8*t+math.pi)))<1e-12
checks+=1
print("minimal checker passed",checks,"tests; full independent suite in reproducibility ZIP")
