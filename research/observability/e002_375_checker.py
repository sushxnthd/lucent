from fractions import Fraction as Q
import random
def overlap(a,b,c,d):
 return max(Q(0),min(b,d)-max(a,c))
def maximum(D,F,w,p):
 return max(overlap(p,p+D,k*F,k*F+w) for k in range(-2,int((p+D)//F)+3))
def law(D,F,w):
 return min(w,max(Q(0),(D-F+w)/2))
rng=random.Random(375); checks=0
for fps,target in [(25,Q(10,1000)),(20,Q(9,1000)),(10,Q(0))]:
 F=Q(1,fps);w=Q(10,1000);D=Q(58,1000);q=law(D,F,w)
 assert q==target
 p=w-q if 0<q<w else (w if q==0 else Q(0))
 assert maximum(D,F,w,p)==q
 checks+=2
 for _ in range(10000):
  p=F*Q(rng.randrange(1000000),1000000)
  assert maximum(D,F,w,p)>=q
  checks+=1
print('PASS',checks)
