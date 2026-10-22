from fractions import Fraction as Q
import random
A=Q(12000);e=Q(1,200);d=Q(1,800);m=Q(30)
z0=Q(2,5)+e
z1=Q(2,5)+m*d-e
obs=(z1-z0)/d
cert=abs(obs)+A*d/2+2*e/d
truth=m+A*d/2
assert obs==Q(22)
assert cert==truth==Q(75,2)
rng=random.Random(379)
for _ in range(3000):
    dt=Q(1,rng.randint(100,5000))
    lhs=(A*dt/2+2*e/dt)**2-4*A*e
    rhs=(A*dt/2-2*e/dt)**2
    assert lhs==rhs and lhs>=0
print('PASS E002-379 exact quadratic witness and 3000 uncertainty identities')
