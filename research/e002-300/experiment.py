"""E002-300 exact PERCLOS interval calculator. No external dependencies."""
from fractions import Fraction as F
import random, json

def bounds(theta,durations,lows,highs,total):
    assert 0<theta<1 and total>=sum(durations)>0
    assert len(durations)==len(lows)==len(highs)
    assert all(0<=lo<=hi<=1 for lo,hi in zip(lows,highs))
    lower=sum(d*max(F(0),(lo-theta)/(1-theta)) for d,lo in zip(durations,lows))/total
    upper=(total-sum(durations)+sum(d*min(F(1),hi/theta) for d,hi in zip(durations,highs)))/total
    return lower,upper

def run():
    theta,mu,p0=F(4,5),F(2,25),F(1,5)
    threshold=(1-p0)/(1-mu/theta)
    assert threshold==F(8,9)
    result={}
    for rho in [F(7,8),F(8,9),F(9,10),F(1,2),F(1)]:
        a,b=bounds(theta,[rho],[mu],[mu],F(1))
        result[str(rho)]={"lower":str(a),"upper":str(b),"certify":b<=p0}
    rng=random.Random(300)
    for _ in range(500):
        th=F(rng.randint(1,99),100)
        ds=[F(rng.randint(1,10),100) for _ in range(3)]
        ls=[F(rng.randint(0,50),100) for _ in ds]
        us=[l+F(rng.randint(0,int((1-l)*100)),100) for l in ls]
        a,b=bounds(th,ds,ls,us,F(1))
        assert 0<=a<=b<=1
        _,b2=bounds(th,ds,ls,[min(F(1),u+F(1,100)) for u in us],F(1))
        assert b2>=b
    print(json.dumps({"status":"conditional synthetic","coverage_transition":str(threshold),
                      "cases":result,"randomized_checks":500,"human_data":False},indent=2))
if __name__=="__main__":run()
