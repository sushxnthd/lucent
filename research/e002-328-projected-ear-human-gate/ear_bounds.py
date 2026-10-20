from math import dist, inf
PAIRS=((1,5),(2,4),(0,3))
def ear_interval(points,eps):
    if len(points)!=6 or any(len(p)!=2 for p in points): raise ValueError("six 2D points required")
    if not 0<=eps<inf: raise ValueError("invalid eps")
    a,b,w=(dist(points[i],points[j]) for i,j in PAIRS)
    if w==0 and eps==0: raise ValueError("EAR undefined")
    lo=(max(0,a-2*eps)+max(0,b-2*eps))/(2*(w+2*eps))
    hi=(a+b+4*eps)/(2*(w-2*eps)) if w>2*eps else inf
    return lo,hi
def closure_interval(rlo,rhi,olo,ohi):
    if not (0<=rlo<=rhi and 0<olo<=ohi): raise ValueError("invalid intervals")
    return max(0.,1-rhi/olo),min(1.,max(0.,1-rlo/ohi))
def decision(interval,theta):
    lo,hi=interval
    return "CLOSED" if lo>theta else "OPEN" if hi<theta else "ABSTAIN"
def example(eps):
    p=((0.,0.),(9.,3.),(21.,3.),(30.,0.),(21.,-3.),(9.,-3.))
    return decision(closure_interval(*ear_interval(p,eps),.3,.3),.3)
if __name__=="__main__":
    for e in (.12,.124):
        print(e,example(e))
