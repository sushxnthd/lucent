"""Independent QR-nullspace oracle and sharp collision."""
import numpy as np
from scipy.linalg import null_space
from model import design,qnorm
rng=np.random.default_rng(340)
checks=0
for p in ((1,3,7),(1,2,8),(2,5,8),(1,2,3)):
    for tau in (.11,.27,.65,1.35):
        s,n=design(p,tau)
        assert abs(np.linalg.norm(null_space(n.T).T@s)-qnorm(p,tau))<1e-9
        checks+=1
for _ in range(500):
    n=rng.normal(size=(12,4))
    s=rng.normal(size=12)
    c=np.linalg.lstsq(n,s,rcond=None)[0]
    q=s-n@c
    y0=n@c+q/2
    y1=s-q/2
    assert np.linalg.norm(y0-y1)<1e-11
    assert abs(np.linalg.norm(null_space(n.T).T@s)-np.linalg.norm(q))<1e-11
    checks+=1
print("PASS",checks)
