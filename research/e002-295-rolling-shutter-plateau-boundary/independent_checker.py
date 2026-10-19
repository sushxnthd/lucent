from fractions import Fraction as F
def px(y,H,v,T,tau,A,B):
 k=1-v*tau;h=k*H/2
 f=max(F(0),min(F(1),F(1,2)+(k*y-h)/(v*T)))
 return A+B*f
H=F(40);T=F(1,50);tau=F(1,50000);v1=F(3000);v2=F(4000)
w1=v1*T/(1-v1*tau);w2=v2*T/(1-v2*tau)
A1=F(3,10);B1=F(2,5);B2=B1*w2/w1;A2=A1+(B1-B2)/2
assert w1>H and w2>H and 0<=A2<A2+B2<=1
for i in range(401):
 y=H*i/400
 assert px(y,H,v1,T,tau,A1,B1)==px(y,H,v2,T,tau,A2,B2)
for v in [F(50),F(300),F(800),F(1600),F(3000)]:
 for T0 in [F(1,50),F(1,120),F(1,90)]:
  for t0 in [F(1,50000),F(7,500000),F(1,100000)]:
   w=v*T0/(1-v*t0)
   assert w/(T0+t0*w)==v
vc=F(48)/(F(1,90)+F(48)*F(7,500000))
assert F(3500)<vc<F(4500)
# Deliberate mutation: identical contrast cannot hide two different ramp widths.
assert px(H/4,H,v1,T,tau,A1,B1)!=px(H/4,H,v2,T,tau,A1,B1)
print('PASS: 401 exact pixel equalities; 45 rational inversions; frozen crossing; mutation rejected; vcrit=',vc)