#!/usr/bin/env python3
"""Synthetic interval-decision stress test; NOT human or instrument evidence."""
import random, json

def decision(left,right,threshold,gap,speed):
    (ll,lh),(rl,rh),(cl,ch),(tl,th),(vl,vh)=left,right,threshold,gap,speed
    if min(ll,rl,tl,vl)<0 or tl<=0 or vl<=0 or any(lo>hi for lo,hi in (left,right,threshold,gap,speed)):
        return 'INVALID'
    if ll<=ch or rl<=ch: return 'ABSTAIN'
    # Never certify when any nuisance-compatible endpoints violate the speed model.
    if max(abs(ll-rh),abs(lh-rl))>vl*tl: return 'ABSTAIN'
    # Minimum required closure travel versus maximum possible speed*time.
    if (ll-ch)+(rl-ch)>vh*th: return 'EXCLUDE'
    return 'ABSTAIN'

def main():
    rng=random.Random(371)
    counts={'EXCLUDE':0,'ABSTAIN':0,'INVALID':0}
    unsafe=0
    for i in range(20000):
        L=rng.uniform(.2,5);R=rng.uniform(.2,5);c=0.;T=rng.uniform(.01,.12);V=rng.uniform(40,300)
        e=rng.uniform(0,.2);dt=rng.uniform(0,.004);dv=rng.uniform(0,15)
        d=decision((max(0,L-e),L+e),(max(0,R-e),R+e),(c,c),(max(.0001,T-dt),T+dt),(max(.001,V-dv),V+dv))
        counts[d]+=1
        feasible=abs(L-R)<=V*T and L+R<=V*T
        if feasible and d=='EXCLUDE': unsafe+=1
        assert not(feasible and d=='EXCLUDE'),(i,L,R,T,V)
    assert decision((2,2),(2,2),(0,0),(.04,.04),(100,100))=='ABSTAIN'
    assert decision((1,1),(4,4),(0,0),(.01,.01),(100,100))=='ABSTAIN'
    print(json.dumps({'tier':'synthetic interval stress only','seed':371,'cases':20000,'counts':counts,'false_exclusions_among_feasible':unsafe,'limitations':'No human velocity certification or real shutter timestamps; only conservative mathematical safety checked.'},indent=2))
if __name__=='__main__': main()
