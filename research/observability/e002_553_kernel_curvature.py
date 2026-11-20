#!/usr/bin/env python3
"""E002-553 exact shutter-kernel curvature envelope. Mathematical instrument model only."""
from dataclasses import dataclass
from fractions import Fraction as F
import json

def Q(v):
    if isinstance(v,(bool,float)) or not isinstance(v,(F,int,str)):
        raise ValueError("exact rational required")
    return F(v)

@dataclass(frozen=True)
class Pulse:
    start:F
    end:F
    weight:F
    def __post_init__(self):
        if not all(isinstance(v,F) for v in (self.start,self.end,self.weight)):
            raise ValueError("Pulse requires Fractions")
        if self.end<=self.start or self.weight<=0: raise ValueError("invalid pulse")

@dataclass(frozen=True)
class Kernel:
    start:F
    end:F
    pulses:tuple[Pulse,...]
    def __post_init__(self):
        if self.end<=self.start or not self.pulses: raise ValueError("invalid exposure")
        if sum((p.weight for p in self.pulses),F(0))!=1: raise ValueError("unnormalized kernel")
        last=self.start
        for p in sorted(self.pulses,key=lambda p:p.start):
            if p.start<last or p.end>self.end: raise ValueError("overlap/outside support")
            last=p.end
    def moments(self):
        mu=sum((p.weight*(p.start+p.end)/2 for p in self.pulses),F(0))
        sec=sum((p.weight*(p.start*p.start+p.start*p.end+p.end*p.end)/3 for p in self.pulses),F(0))
        return mu,sec-mu*mu
    def quadratic_mean(self,a,b,c):
        mu,var=self.moments()
        return a*(var+mu*mu)+b*mu+c

def boxcar(start,end):
    a,b=Q(start),Q(end)
    return Kernel(a,b,(Pulse(a,b,F(1)),))

def two_pulse(start,end,width):
    a,b,w=map(Q,(start,end,width))
    if 2*w>b-a: raise ValueError("pulse overlap")
    return Kernel(a,b,(Pulse(a,a+w,F(1,2)),Pulse(b-w,b,F(1,2))))

def lower_at(t,k0,k1,m0,m1,A,e0=F(0),e1=F(0)):
    t,m0,m1,A,e0,e1=map(Q,(t,m0,m1,A,e0,e1))
    if A<0 or e0<0 or e1<0: raise ValueError("invalid bounds")
    c0,v0=k0.moments();c1,v1=k1.moments();D=c1-c0
    if D<=0 or not(c0<=t<=c1): raise ValueError("outside kernel centers")
    s=(t-c0)/D
    B0=m0-e0-A*v0/2;B1=m1-e1-A*v1/2
    return (1-s)*B0+s*B1-A*D*D*s*(1-s)/2

def minimum_gap(k0,k1,m0,m1,A,gap_start,gap_end,e0=F(0),e1=F(0)):
    m0,m1,A,lo,hi,e0,e1=map(Q,(m0,m1,A,gap_start,gap_end,e0,e1))
    c0,v0=k0.moments();c1,v1=k1.moments()
    if lo>=hi or k0.end>lo or k1.start<hi or c0>=c1: raise ValueError("invalid dark gap")
    D=c1-c0;B0=m0-e0-A*v0/2;B1=m1-e1-A*v1/2
    ts=[lo,hi]
    if A>0:
        sstar=F(1,2)-(B1-B0)/(A*D*D)
        ts.append(max(lo,min(hi,c0+D*sstar)))
    return min((lower_at(t,k0,k1,m0,m1,A,e0,e1),t) for t in ts)

REQUIRED_GATES=("independent_anatomy","linear_optical_transfer","authenticated_shutter_kernel",
"certified_continuous_acceleration","authenticated_clock","bounded_geometry",
"brightness_stability","blur_calibration","gaze_control","glasses_control","missingness_control")

def adjudicate(k0,k1,m0,m1,A,lo,hi,theta,gates,errors=(F(0),F(0))):
    if not isinstance(gates,dict) or any(gates.get(g) is not True for g in REQUIRED_GATES):
        return {"decision":"ABSTAIN_UNCALIBRATED","reason":"missing independently authenticated nuisance gate"}
    try:
        low,t=minimum_gap(k0,k1,m0,m1,A,lo,hi,*errors);theta=Q(theta)
        if not 0<=theta<=1: raise ValueError("invalid threshold")
    except (ValueError,TypeError,ZeroDivisionError) as ex:
        return {"decision":"ABSTAIN_UNCALIBRATED","reason":str(ex)}
    return {"decision":"CONDITIONAL_INSTRUMENT_EXCLUSION_ONLY" if low>theta else "HIDDEN_CLOSURE_NOT_EXCLUDED",
            "lower":str(low),"argmin_time":str(t),"evidence_tier":"MATHEMATICAL_CONDITIONAL_ONLY"}

def demo():
    k0=two_pulse("-1/2","0","1/20");k1=two_pulse("1","3/2","1/20")
    b0=boxcar("-1/2","0");b1=boxcar("1","3/2")
    m0=k0.quadratic_mean(F(1),F(-1),F(1,4));m1=k1.quadratic_mean(F(1),F(-1),F(1,4))
    correct,t=minimum_gap(k0,k1,m0,m1,F(2),F(0),F(1))
    wrong,_=minimum_gap(b0,b1,m0,m1,F(2),F(0),F(1))
    assert (m0,m1,correct,wrong,t)==(F(46,75),F(46,75),F(0),F(3,100),F(1,2))
    return {"model":"synthetic_two_pulse_shutter","m0":str(m0),"m1":str(m1),
      "variance_true":str(k0.moments()[1]),"variance_boxcar":str(b0.moments()[1]),
      "actual_min":"0","theta":"1/50","invalid_boxcar_lower":str(wrong),
      "correct_kernel_lower":str(correct),"false_exclusion_under_misdeclared_boxcar":wrong>F(1,50),
      "kernel_aware_abstains":correct<=F(1,50),"evidence_tier":"EXACT_SYNTHETIC_ONLY"}

if __name__=="__main__":
    print(json.dumps(demo(),indent=2,sort_keys=True))
