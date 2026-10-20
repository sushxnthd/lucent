import random,math,json
from fractions import Fraction
from pathlib import Path
rng=random.Random(328)
def norm(a,b): return math.hypot(a[0]-b[0],a[1]-b[1])
def ear(p): return (norm(p[1],p[5])+norm(p[2],p[4]))/(2*norm(p[0],p[3]))
def bounds(p,e):
    a,b,w=norm(p[1],p[5]),norm(p[2],p[4]),norm(p[0],p[3])
    return (max(0,a-2*e)+max(0,b-2*e))/(2*(w+2*e)),(a+b+4*e)/(2*(w-2*e))
def witness(p,e,upper):
    q=[list(z) for z in p]
    for i,j in [(1,5),(2,4),(0,3)]:
        dx,dy=p[j][0]-p[i][0],p[j][1]-p[i][1]
        r=math.hypot(dx,dy);ux,uy=dx/r,dy/r
        expand=upper if (i,j)!=(0,3) else not upper
        sign=1 if expand else -1
        q[i][0]-=sign*e*ux;q[i][1]-=sign*e*uy
        q[j][0]+=sign*e*ux;q[j][1]+=sign*e*uy
    return ear(q)
worst=0.
for k in range(2000):
    w=rng.uniform(10,80);a=rng.uniform(2,12);b=rng.uniform(2,12)
    e=rng.uniform(.001,min(.49,a/4,b/4,w/8))
    p=[(0.,0.),(w*.25,a/2),(w*.75,b/2),(w,0.),(w*.75,-b/2),(w*.25,-a/2)]
    lo,hi=bounds(p,e)
    loww,highw=witness(p,e,False),witness(p,e,True)
    worst=max(worst,abs(lo-loww),abs(hi-highw))
    assert abs(lo-loww)<1e-12 and abs(hi-highw)<1e-12
    for _ in range(20):
        q=[]
        for x,y in p:
            radius=e*math.sqrt(rng.random());ang=2*math.pi*rng.random()
            q.append((x+radius*math.cos(ang),y+radius*math.sin(ang)))
        assert lo-1e-12<=ear(q)<=hi+1e-12
crit=(Fraction(21,100)*30-6)/(2+2*Fraction(21,100))
assert crit==Fraction(15,121)
assert (Fraction(6)+2*crit)/(30-2*crit)==Fraction(21,100)
def cls(e):
    return "CLOSED" if 1-(6+2*e)/(30-2*e)/.3>.3 else "ABSTAIN"
assert cls(.12)=="CLOSED" and cls(.124)=="ABSTAIN"
result={"status":"PASS","randomized_geometries":2000,"randomized_interior_checks":40000,"extremal_witness_checks":4000,"max_witness_abs_error":worst,"critical_epsilon_exact":str(crit),"critical_epsilon_decimal":float(crit),"at_0.12":cls(.12),"at_0.124":cls(.124),"human_data_tested":False}
Path(__file__).with_name("checker_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
