import math
s=lambda t: math.sin(2*math.pi*1.3*t)+.31*math.sin(2*math.pi*3.7*t+.2)
u=[i/30 for i in range(150)]
pairs=[(.07,.03),(.02,.08),(-.04,.14)]
w=[[s(t-d-tau) for t in u] for d,tau in pairs]
e=[max(abs(a-b) for a,b in zip(w[0],v)) for v in w[1:]]
assert max(e)<1e-12
for f in (1,2,5):
 print(f,1000*math.acos(.7)/(2*math.pi*f),math.cos(2*math.pi*f*.05))
print('gauge_max_error',max(e))
