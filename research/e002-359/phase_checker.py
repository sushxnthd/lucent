"""Independent phase-minimum checker for E002-359."""
import math, random
rng=random.Random(359)
def overlap(a,b,c,d): return max(0,min(b,d)-max(a,c))
for _ in range(1000):
 F=rng.uniform(10,60); w=rng.uniform(.1*F,F); D=rng.uniform(.01*F,F)
 x=max(0,D-(F-w))
 t=w-x/2 if x else w+(F-w-D)/2
 f=[overlap(k*F,k*F+w,t,t+D)/w for k in range(-2,4)]
 assert abs(math.sqrt(sum(v*v for v in f))-x/(math.sqrt(2)*w))<1e-12
print("PASS: 1000 exact constructed phase minima; human NOT RUN")
