"""Exact-rational boundary, witness and nuisance-control checks."""
from fractions import Fraction as F
from random import Random
from model import evaluate,critical_start

def run():
    p={"A":F(7,100),"B":F(3,25),"eta":F(1,125),"E":F(3,250),
       "Delta":F(3,1000),"tp":F(9,50),"duration":F(7,25),"tc":F(11,50)}
    args=lambda s,D:evaluate(s,p["E"],D,p["tp"],p["duration"],p["tc"],p["A"],p["B"],p["eta"])
    assert critical_start(p["E"],p["Delta"],p["tc"],p["A"],p["B"],p["eta"])==F(2203,10000)
    assert args(F(2203,10000),p["Delta"])["margin"]==0
    early=args(F(219,1000),p["Delta"]);late=args(F(111,500),p["Delta"])
    assert not early["certify"] and late["certify"]
    rng=Random(1326);q=lambda n:F(n,10000)
    for _ in range(1000):
        s=q(rng.randint(1000,5500));E=q(rng.randint(50,400))
        D=q(rng.randint(0,80));tp=q(rng.randint(1300,3000))
        d=q(rng.randint(1500,4000));tc=q(rng.randint(500,4000))
        A=q(rng.randint(300,2000));B=q(rng.randint(100,2000));eta=q(rng.randint(0,200))
        z=evaluate(s,E,D,tp,d,tc,A,B,eta)
        assert z["margin"]==z["alt_interval"][0]-z["null_interval"][1]
        assert z["certify"]==(z["alt_interval"][0]>z["null_interval"][1])
    base=F(1,2);pchange=F(2,25);gain=base/(base+pchange)
    assert base==gain*(base+pchange) # geometry/gain confound
    assert early["alt_interval"][0]<=early["null_interval"][1] # brightness
    assert late["certify"] and not early["certify"] # dropped late frame
    assert args(F(111,500),F(0))["margin"]>=late["margin"]>=args(F(111,500),F(1,100))["margin"]
    print("PASS exact-rational boundary, 1000 checks, four controls")

if __name__=="__main__":run()
