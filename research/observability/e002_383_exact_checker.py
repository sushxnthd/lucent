"""E002-383 independent exact synthetic RGB collision checker."""
import math
import numpy as np
from scipy.integrate import quad

v=60.0;w=.01;h=1/30-w;b=.99;theta=.2
y=1-math.sqrt(2*v*w*(1-b))
t0=(1-y)/v
m=((2/(3*v))*(1-y**1.5)+(w-t0))/w
m2=quad(lambda s:math.sqrt(min(1,y+v*s)),0,w,points=[t0])[0]/w
assert abs(m-m2)<1e-12
a0=m*m
minimum=y-v*h/2
assert minimum<theta<a0
naive_lower=1-math.sqrt(2*v*w*(1-m))-v*h/2
assert naive_lower>theta
rng=np.random.default_rng(38383)
C=rng.uniform(.1,.5,(24,40,3))
O=rng.uniform(.5,.9,(24,40,3))
moving=C+m*(O-C)
constant=C+math.sqrt(a0)*(O-C)
assert np.max(np.abs(moving-constant))<3e-16
print(dict(true_minimum=minimum,naive_lower=naive_lower,
           constant_nonclosure=a0,shutter_sqrt_mean=m,
           max_rgb_difference=float(np.max(np.abs(moving-constant)))))
