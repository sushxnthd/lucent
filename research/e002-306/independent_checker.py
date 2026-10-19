"""Independent arbitrary precision checker. Does not import experiment."""
from fractions import Fraction as Q
import mpmath as m
import json
m.mp.dps=65
assert Q(25)**2-Q(7)**2==Q(24)**2
assert Q(25)-Q(24)==1==2*Q(1,2)
assert Q(25)**2-Q(15)**2==Q(20)**2
assert Q(17)**2-Q(15)**2==Q(8)**2
assert abs((Q(25)-Q(20))-(Q(17)-Q(8)))==2*Q(2)
def s(R,a):return a*a/(R+m.sqrt(R*R-a*a))
def p(R,a,x):return m.sqrt(R*R-x*x)-m.sqrt(R*R-a*a)
for j in range(200):
    R=m.mpf(12)+m.mpf(j+1)/11
    S=R*(m.mpf("1.001")+m.mpf(j%17)/100)
    a=R*(m.mpf(".1")+m.mpf(j%19)/22)
    if a>=R:continue
    full=abs(s(R,a)-s(S,a))
    sample=max(abs(p(R,a,a*m.mpf(k)/100)-p(S,a,a*m.mpf(k)/100)) for k in range(-100,101))
    assert abs(full-sample)<m.mpf("1e-55")
def root(R,eta,q):
    return m.findroot(lambda al:s(R,R*m.sin(al))-s(R*(1+q),R*m.sin(al))-2*eta,(m.mpf(".5"),m.mpf(".85")))
assert abs(root(m.mpf(25),m.mpf(".3"),m.mpf(".1"))*180/m.pi-m.mpf("38.30020125198"))<m.mpf("1e-9")
R=m.mpf("19.7");eta=m.mpf(".22");q=m.mpf(".08")
alpha=root(R,eta,q)
assert abs(alpha*180/m.pi-m.mpf("40.37258267723268"))<m.mpf("1e-10")
checks=[]
for deg,pred in [(m.mpf("37.37258267723268"),False),(m.mpf("43.37258267723268"),True)]:
    a=R*m.sin(deg*m.pi/180)
    gap=s(R,a)-s(R*(1+q),a)
    actual=bool(gap>2*eta)
    assert actual==pred
    checks.append({"angle_deg":float(deg),"gap_px":str(gap)[:24],"prediction":pred,"observed":actual})
print(json.dumps({"rational_witnesses":2,"high_precision_trials":200,"mutation_checks":4,"unseen_synthetic_holdout":checks,"passed":True,"human_validation":False},indent=2))
