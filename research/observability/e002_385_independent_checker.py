"""E002-385 independent shutter-geometry audit. No human data."""
import numpy as np
F=1/30;w=.01;H=F-w;v=40;c=(w+F)/2
a=lambda t:np.minimum(1,.19+v*np.abs(np.asarray(t)-c))
# Independently integrate physical aperture, not the compact simulator formula.
means=[]
for s in (0,F):
    t=np.linspace(s,s+w,100001)
    means.append(float(np.trapezoid(a(t),t)/w))
assert max(means)-min(means)<1e-12
assert abs(means[0]-.8526527777777778)<1e-9
assert abs(a(np.array([c]))[0]-.19)<1e-12
def end_lower(y,e):
    b=max(0,y-e)
    if 1-b<=v*w/2:return max(0,1-np.sqrt(2*v*w*(1-b)))
    return max(0,b-v*w/2)
def bound(y,e):
    L,R=[end_lower(x,e) for x in y]
    t=np.linspace(0,H,20001)
    return float(np.maximum(L-v*t,R-v*(H-t)).min())
# Clean hidden cannot certify, while a correlated +.06 optical bias creates a false certificate.
q=.0019816776917358503
assert bound(means,q)<=.2
assert bound([x+.06 for x in means],q)>.2
assert bound([x+.06 for x in means],.06) <=.2
assert bound([1.,1.],q)>.2
print('PASS: exact-integral cross-check, gap cone, nuisance collision, oracle abstention')
