"""Sharp two-anchor clock-lag certificate; synthetic model only."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ClockGate:
    t0: float
    t1: float
    anchor_error0: float
    anchor_error1: float
    drift_lipschitz: float
    rgb_event_error: float
    reference_event_error: float
    def __post_init__(self):
        assert self.t1>self.t0
        assert min(self.anchor_error0,self.anchor_error1,self.drift_lipschitz,self.rgb_event_error,self.reference_event_error)>=0
    def bound(self,t):
        if not self.t0<=t<=self.t1:
            raise ValueError("outside sync anchors: abstain, recalibrate")
        u=(t-self.t0)/(self.t1-self.t0)
        return ((1-u)*self.anchor_error0+u*self.anchor_error1+
                self.drift_lipschitz*min(t-self.t0,self.t1-t)+
                self.rgb_event_error+self.reference_event_error)
    def interval(self,observed_lag,t):
        b=self.bound(t)
        return observed_lag-b,observed_lag+b
    def classify(self,observed_lag,t):
        lo,hi=self.interval(observed_lag,t)
        return "positive" if lo>0 else ("negative" if hi<0 else "abstain")
def extremal_witness(g,t,sign):
    if sign not in (-1,1): raise ValueError(sign)
    return sign*g.bound(t)
if __name__=="__main__":
    import json
    g=ClockGate(0,10,.004,.004,.001,.006,.010)
    print(json.dumps({"at_0":g.bound(0),"at_5":g.bound(5),"at_10":g.bound(10),
      "lag_0.024_at_5":g.classify(.024,5),"lag_0.026_at_5":g.classify(.026,5)},indent=2))
