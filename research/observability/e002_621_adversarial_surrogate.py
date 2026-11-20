"""E002-621: seeded adversarial piecewise-linear scalar aperture surrogate.
Synthetic model only; not physical or human validation.
"""
import random
import json

def excludes(m1,m2,t1,t2,g,v,c):
    a=max(0,m1-v*t1/2)
    b=max(0,m2-v*t2/2)
    return max(0,a-c)+max(0,b-c)>v*g

def run(n=100000,seed=621):
    r=random.Random(seed)
    exclusions=hidden=errors=0
    for _ in range(n):
        v=r.uniform(1,300);t1=r.uniform(.002,.05)
        g=r.uniform(0,.07);t2=r.uniform(.002,.05);c=r.uniform(0,2)
        ts=[0,t1/2,t1,t1+g/2,t1+g,t1+g+t2/2,t1+g+t2]
        x=[r.uniform(0,6)]
        for i in range(1,7):
            x.append(max(0,x[-1]+r.uniform(-v*(ts[i]-ts[i-1]),v*(ts[i]-ts[i-1]))))
        m1=(x[0]+2*x[1]+x[2])/4
        m2=(x[4]+2*x[5]+x[6])/4
        # Independent conservative nuisance envelopes.
        m1=max(0,m1-r.uniform(0,.4));m2=max(0,m2-r.uniform(0,.4))
        V=v*r.uniform(1,1.5);G=g+r.uniform(0,.003)
        T1=t1+r.uniform(0,.003);T2=t2+r.uniform(0,.003)
        C=c+r.uniform(0,.3)
        decision=excludes(m1,m2,T1,T2,G,V,C)
        event=min(x[2],x[3],x[4])<=c
        exclusions+=decision;hidden+=event;errors+=decision and event
    assert errors==0
    # Mean-as-endpoint substitution falsely excludes at this boundary.
    assert excludes(3,3,0,0,.02,100,1)
    assert not excludes(3,3,.02,.02,.02,100,1)
    return dict(seed=seed,trials=n,conditional_exclusions=exclusions,
        hidden_trajectories=hidden,false_exclusions=errors,
        abstentions=n-exclusions,evidence='synthetic scalar surrogate only')

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
