import math
from experiment import H
f,T,d,a=117,1/90,.0031,.55
w=2*math.pi*f
def avg(t,p):
 return (math.sin(w*(t+T)+p)-math.sin(w*t+p))/(w*T)
v=[]
for i in range(4096):
 p=2*math.pi*i/4096
 v.append(math.log((1+a*avg(d/2,p))/(1+a*avg(-d/2,p))))
h=H(f,T,d,a)
assert abs(min(v)+h)<1e-5 and abs(max(v)-h)<1e-5
print("independent heldout integral check passed")
