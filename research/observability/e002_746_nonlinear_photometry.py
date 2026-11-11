"""E002-746: seeded synthetic nonlinear image-to-aperture falsification; NOT human data."""
import random,json
R=random.Random(746)
N=20000
counts={'total':N,'false_naive':0,'false_conservative':0,'naive_exclusions':0,'conservative_exclusions':0,'hidden_closures':0}
# Normalized aperture a in [0,1], seconds, V aperture/second.
# Feasible V-Lipschitz paths with a hidden zero exist iff a0+a1<=V*dt.
# Camera intensity B=a**gamma; gamma is unknown but constrained to [.55,2.2].
for _ in range(N):
    a0=R.uniform(.05,1);a1=R.uniform(.05,1)
    V=R.uniform(5,20);dt=R.uniform(.005,.11)
    if abs(a0-a1)>V*dt: dt=abs(a0-a1)/V+.00001
    gamma=R.uniform(.55,2.2)
    b0=a0**gamma;b1=a1**gamma
    hidden=a0+a1<=V*dt
    counts['hidden_closures']+=hidden
    naive=b0+b1>V*dt
    low0=min(b0**(1/.55),b0**(1/2.2))
    low1=min(b1**(1/.55),b1**(1/2.2))
    conservative=low0+low1>V*dt
    counts['naive_exclusions']+=naive
    counts['conservative_exclusions']+=conservative
    counts['false_naive']+=naive and hidden
    counts['false_conservative']+=conservative and hidden
assert counts['false_conservative']==0
assert counts['false_naive']>0
print(json.dumps(counts,sort_keys=True))
