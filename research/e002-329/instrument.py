"""E002-329: conditional projective conic and area laws. NumPy required."""
import numpy as np

def circle(radius):
    assert radius > 0
    return np.diag([1.,1.,-radius**2])

def transform(C,H):
    J=np.linalg.inv(H)
    return J.T@C@J

def conic_ratio(Cp,Ci):
    v=np.linalg.eigvals(np.linalg.solve(Ci,Cp))
    assert np.max(np.abs(np.imag(v)))<1e-7
    v=np.real(v)
    pairs=[(abs(v[0]-v[1]),2),(abs(v[0]-v[2]),1),(abs(v[1]-v[2]),0)]
    single=min(pairs)[1]
    double=np.mean(np.delete(v,single))
    return float(np.sqrt(v[single]/double))

def area_ratio(rho,q):
    assert 0<rho<1 and abs(q)<1
    return rho*((1-q*q)/(1-q*q*rho*rho))**.75

def qcritical(rho,delta):
    assert 0<rho<1 and 0<delta<1
    a=(1-delta)**(4/3)
    return float(np.sqrt((1-a)/(1-a*rho*rho)))

def sign_gate(d,B):
    assert B>=0
    return "DILATION" if d>B else ("CONSTRICTION" if d < -B else "ABSTAIN")
