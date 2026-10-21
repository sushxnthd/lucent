"""Independent shutter-transfer checker; run python independent_checker.py."""
import random,math,json
from instrument import *
rng=random.Random(35120261022)
for _ in range(300):
    a=rng.uniform(.001,.04);b=rng.uniform(.001,.04);c=rng.uniform(-.03,.03)
    n=4000
    numerical=sum(abs((a-b)*((i+.5)/n-.5)-c) for i in range(n))/n
    assert abs(wasserstein_box(a,b,c)-numerical)<5e-7
for _ in range(1500):
    a=rng.uniform(.001,.04);b=rng.uniform(.001,.04);v=rng.uniform(.1,30)
    # Exact Lipschitz witness f(t)=v*abs(t) for concentric shutters.
    assert abs(v*abs(a-b)/4-v*wasserstein_box(a,b))<1e-12
for _ in range(1500):
    a=rng.uniform(.004,.06);b=rng.uniform(.0002,a)
    assert abs(native_fraction((b/2,a/2),0,a)-false_negative_max(b,a))<1e-12
    assert native_fraction((b/2,a/2),0,b)==0
    assert abs(native_fraction((-b/2,b/2),0,a)-false_positive_min(b,a))<1e-12
    assert abs(native_fraction((-b/2,b/2),0,b)-1)<1e-12
print('PASS: 300 W1 numerical, 1500 sharp Lipschitz witness, 1500 binary constructions')
