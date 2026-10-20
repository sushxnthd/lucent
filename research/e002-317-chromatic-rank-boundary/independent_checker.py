"""Independent synthetic checker; no imports from model/derivation. NumPy required."""
import json,math,random
from fractions import Fraction
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
rng=np.random.default_rng(20261020)
def interval(y,a,b,eta):
    b0=b/np.linalg.norm(b)
    u=a-np.dot(a,b0)*b0
    d=np.linalg.norm(u)
    if d<1e-12: return None
    hhat=float(np.dot(u,y)/d**2)
    q=y-np.dot(y,b0)*b0-hhat*u
    rho=float(np.linalg.norm(q))
    if rho>eta+1e-10: return {'falsified':True,'rho':rho}
    w=math.sqrt(max(0,eta*eta-rho*rho))/d
    return {'lo':max(0,hhat-w),'hi':min(1,hhat+w),'hhat':hhat,'d':d}
a=[Fraction(1)]*3;b=[Fraction(2)]*3
assert [Fraction(3,5)*v for v in a]==[Fraction(1,5)*v+Fraction(1,5)*w for v,w in zip(a,b)]
a=np.array([1.,.5,.2]);b=np.array([.2,.4,.8])
va=.5*a+.2*b;vb=.4*a+.2*b
assert np.linalg.norm(np.cross(a,b))>.1 and np.allclose(va,(va/vb)*vb,atol=1e-15)
pred=json.loads((P/'FROZEN_PREDICTION.json').read_text())
eta=pred['parameters']['eta'];delta=pred['parameters']['observed_aperture_change']
critical=math.degrees(math.asin(2*eta/delta))
assert abs(critical-pred['prediction']['critical_angle_degrees'])<1e-12
angles={}
for deg in pred['parameters']['angles_degrees']:
    a=np.array([1.,0.,0.]);theta=math.radians(deg)
    b=np.array([math.cos(theta),math.sin(theta),0.])
    x=interval(.45*a+.2*b,a,b,eta);y=interval((.45+delta)*a+.8*b,a,b,eta)
    status='CERTIFY_INCREASE' if y['lo']>x['hi'] else 'ABSTAIN'
    assert status==pred['prediction'][str(deg)+'_degrees']
    angles[str(deg)]=status
endpoints=0;maxerr=0
for _ in range(1000):
    a=rng.normal(size=3);b=rng.normal(size=3)
    if np.linalg.norm(np.cross(a,b))<.05:continue
    h=float(rng.uniform(.2,.8));z=float(rng.uniform(-2,2));eta=float(rng.uniform(.005,.05))
    e=rng.normal(size=3);e=e/np.linalg.norm(e)*float(rng.uniform(0,eta))
    y=h*a+z*b+e
    out=interval(y,a,b,eta)
    assert not out.get('falsified',False) and out['lo']-1e-9<=h<=out['hi']+1e-9
    for hs in [out['lo'],out['hi']]:
        zs=float(np.dot(b,y-hs*a)/np.dot(b,b))
        residual=np.linalg.norm(y-hs*a-zs*b)
        assert residual<=eta+1e-9
        if 0<hs<1:maxerr=max(maxerr,abs(residual-eta))
        endpoints+=1
assert interval(np.array([.5,.1,.05]),np.array([1.,0,0]),np.array([0.,1.,0]),.01)['falsified']
a=np.array([.8,.25,.12]);b=np.array([.2,.65,.2]);signal=.42*a+.18*b
psf=np.array([1.,3.,6.,3.,1.]);psf/=psf.sum()
band=np.ones(17)/17
image=np.stack([np.convolve(band*s,psf,'full') for s in signal])
assert np.allclose(image.sum(axis=1),signal,atol=1e-14)
assert np.allclose((1.7*image).sum(axis=1)/1.7,signal,atol=1e-14)
assert np.linalg.norm(np.cross(a,b))>0 and np.linalg.matrix_rank(np.array([[a[0],b[0]]]))==1
print(json.dumps({'status':'PASS_SYNTHETIC_ONLY','critical_angle_degrees':critical,'angles':angles,'endpoint_witnesses':endpoints,'max_unclipped_endpoint_error':maxerr,'exact_rank_collision':True,'gain_collision':True,'controls':'PASS','human':'NOT_RUN'},indent=2))
