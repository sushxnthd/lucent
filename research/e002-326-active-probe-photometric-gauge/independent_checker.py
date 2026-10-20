"""Independent NumPy brute-grid checker; never imports model.py."""
import json,random
from fractions import Fraction as F
from pathlib import Path
import numpy as np

def ol(x,E,lo,hi):
    return np.maximum(0.,np.minimum(x+E,hi)-np.maximum(x,lo))

def brute(s,E,D,tp,d,tc,A,B,eta,n=30001):
    x=s+np.linspace(-D,D,n)
    p=ol(x,E,tp,tp+d)/E;nu=ol(x,E,0,tc)/E
    return float(np.min(A*p-B*nu)-B*np.max(nu)-2*eta)

def collision(s,E,D,tp,d,tc,A,B,eta):
    x=s+np.linspace(-D,D,10001)
    p=ol(x,E,tp,tp+d)/E;nu=ol(x,E,0,tc)/E
    return max(-B*nu.max()-eta,np.min(A*p-B*nu)-eta)<=min(B*nu.max()+eta,np.max(A*p+B*nu)+eta)+1e-12

def main():
    f=json.loads(Path("FROZEN_PREDICTION.json").read_text())
    z={k:float(F(v)) for k,v in f["holdout_instrument"].items()}
    A=z["A"];B=z["B"];eta=z["eta"];E=z["E"];D=z["Delta"];tp=z["tau_p"];d=z["pupil_duration"];tc=z["tau_c"]
    critical=tc+D-E*(A-2*eta)/(2*B)
    assert abs(critical-float(F(f["predicted_critical_start_seconds"])))<1e-14
    checks=[]
    for t in f["holdout_tests"]:
        s=float(F(t["s"]));margin=brute(s,E,D,tp,d,tc,A,B,eta)
        decision="CERTIFY" if margin>1e-12 else "ABSTAIN"
        assert decision==t["prediction"]
        assert collision(s,E,D,tp,d,tc,A,B,eta)!=(decision=="CERTIFY")
        checks.append({"s":s,"margin":margin,"actual":decision})
    rng=random.Random(326);maxgap=0.
    for _ in range(250):
        E=rng.uniform(.006,.04);D=rng.uniform(0,.008);tp=rng.uniform(.13,.30)
        d=rng.uniform(.15,.4);tc=rng.uniform(.05,.40);s=rng.uniform(.1,.55)
        A=rng.uniform(.03,.2);B=rng.uniform(.01,.2);eta=rng.uniform(0,.02)
        k=[-D,D]
        for t in (0.,tc,tp,tp+d):
            for x in (t-s,t-s-E):
                if -D<=x<=D:k.append(x)
        v=s+np.array(k);p=ol(v,E,tp,tp+d)/E;nu=ol(v,E,0,tc)/E
        exact=float(np.min(A*p-B*nu)-B*np.max(nu)-2*eta)
        approx=brute(s,E,D,tp,d,tc,A,B,eta,n=10001)
        assert approx>=exact-1e-11
        maxgap=max(maxgap,approx-exact)
    ts=np.linspace(0,1,2001)
    pupil=.08*np.exp(-((ts-.34)/.055)**2)
    baseline=np.stack([.45+.04*np.sin(ts*7),.5+.03*np.cos(ts*9),.55+.01*np.sin(ts*3)],axis=1)
    sig=np.array([.7,.9,.5])
    world1=baseline+np.outer(pupil,sig)
    world2=baseline+np.outer(-pupil,sig)+2*np.outer(pupil,sig)
    gauge=float(np.max(np.abs(world1-world2)))
    assert gauge<3e-16
    result={"holdout":checks,"critical_start_seconds":critical,
            "randomized_cases":250,"max_grid_approximation_gap":maxgap,
            "full_rgb_smooth_gauge_max_difference":gauge,
            "human_rgb_reference_validation":"NOT_PERFORMED","tests":"PASS"}
    Path("results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
