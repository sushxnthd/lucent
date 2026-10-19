"""E002-302: exact sign certificate and participant-level split conformal."""
from math import ceil,inf,log

def sign_certificate(z0,z1,threshold):
    s=log(z1/z0)
    if s>threshold:return 1
    if s<-threshold:return -1
    return 0

def threshold(scores,alpha=.05):
    n=len(scores)
    k=ceil((n+1)*(1-alpha)-1e-12)
    return (sorted(scores)[k-1] if k<=n else inf)

def participant_scores(pairs):
    out={}
    for p,z0,z1,d0,d1 in pairs:
        residual=abs(log(z1/z0)-log(d1/d0))
        out[p]=max(out.get(p,0),residual)
    return out

if __name__=="__main__":
    assert sign_certificate(1,1.1,.05)==1
    assert sign_certificate(1,1.02,.05)==0
    assert threshold(list(range(19)),.05)==18
    assert threshold(list(range(18)),.05)==inf
    print("core verification passed")
