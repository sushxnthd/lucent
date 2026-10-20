"""E002-318 synthetic projective conic and differential-optics gauge.
Restricted coplanar concentric pupil/iris under one homography. Not a
calibrated model of real corneal refraction or consumer-camera RGB.
"""
import numpy as np

def circle_conic(radius):
    assert radius > 0
    return np.diag([1.0, 1.0, -float(radius)**2])

def project_conic(conic, H):
    inv = np.linalg.inv(H)
    return inv.T @ conic @ inv

def random_homography(rng):
    theta = rng.uniform(-1.2,1.2)
    co,si=np.cos(theta),np.sin(theta)
    rot=np.array([[co,-si],[si,co]])
    stretch=np.array([[rng.uniform(.65,1.7),rng.uniform(-.3,.3)],
                      [0.,rng.uniform(.65,1.7)]])
    H=np.eye(3)
    H[:2,:2]=rot@stretch
    H[:2,2]=rng.uniform(-.25,.25,size=2)
    H[2,:2]=rng.uniform(-.09,.09,size=2)
    return H

def conic_radius_ratio(pupil, iris):
    """Existing Wang/Chern/Alexa 2019 projective invariant, NOT NEW."""
    eig=np.linalg.eigvals(np.linalg.solve(iris,pupil))
    if np.max(np.abs(np.imag(eig)))>1e-7:
        raise ValueError("Complex generalized eigenvalues: abstain")
    v=np.sort(np.abs(np.real(eig)))
    if np.any(v<=0): raise ValueError("Degenerate conic: abstain")
    return float(np.sqrt(v[0]/np.mean(v[1:])))

def true_ratio_interval(p0,p1,rho):
    assert p0>0 and p1>0 and 0<rho<=1
    Q=p1/p0
    return rho*Q,Q/rho

def certify_increase(p0,p1,rho):
    return true_ratio_interval(p0,p1,rho)[0]>1

def synthetic_rgb(pupil,iris,n=128):
    coords=np.linspace(-2,2,n)
    x,y=np.meshgrid(coords,coords)
    pts=np.stack([x,y,np.ones_like(x)],axis=-1)
    cp=np.einsum('...i,ij,...j->...',pts,pupil,pts)
    ci=np.einsum('...i,ij,...j->...',pts,iris,pts)
    out=np.empty((n,n,3),dtype=np.float64)
    out[:]=[.90,.86,.81]
    out[ci<0]=[.34,.43,.28]
    out[cp<0]=[.10,.09,.08]
    return out

def full_image_world(q_true,m,H,n=128):
    q_effective=q_true*m
    assert 0<q_effective<1
    return synthetic_rgb(project_conic(circle_conic(q_effective),H),
                         project_conic(circle_conic(1),H),n)
