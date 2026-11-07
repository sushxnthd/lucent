"""E002-654: synthetic sharp shutter-gap falsification. Not human evidence."""
from itertools import product

def envelope(a,b,T,V,t):
    return max(0.,a-V*t,b-V*(T-t))

def certificate(a,b,T,V,err=0.,clock=0.):
    """Point-sample model only. Not valid for exposure-integrated observations."""
    if min(a,b,T,V)<0 or err<0 or clock<0: return 'ABSTAIN_INVALID'
    if V==0: return 'CERTIFIED' if min(a,b)>err else 'ABSTAIN'
    return 'CERTIFIED' if a+b-2*err>V*(T+clock) else 'ABSTAIN'

def run():
    cases=0
    for a,b,V,T in product([.1,.3,.7],[.1,.4,.8],[.5,1.,2.],[.1,.3,.7,1.,2.,4.]):
        if a+b<=V*T+1e-12:
            t=a/V
            assert t<=T+1e-12 and envelope(a,b,T,V,t)<1e-10
        else:
            assert min(envelope(a,b,T,V,T*i/1000) for i in range(1001))>0
        if certificate(a,b,T,V)=='CERTIFIED': assert a+b>V*T
        cases+=1
    assert certificate(.5,.5,.9,1)=='CERTIFIED'
    assert certificate(.5,.5,.9,1,err=.06)=='ABSTAIN'
    assert certificate(.5,.5,.9,1,clock=.11)=='ABSTAIN'
    assert certificate(.5,.5,1.,1.)=='ABSTAIN'
    print(f'PASS: {cases} synthetic sharpness cases; uncertainty/equality controls')

if __name__=='__main__': run()
