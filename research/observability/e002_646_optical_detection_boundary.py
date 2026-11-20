"""E002-646: Exact optical-detection boundary under bounded pulse contrast.

Timing intersection alone does not imply detection. For a rectangular pulse,
exposure E and pulse P, normalized contrast is C*|E intersect P|/|E|.
All quantities here are exact rationals, with no camera physiology assumed.
"""
from fractions import Fraction as F
from itertools import product

def overlap(a,b,c,d):
    return max(F(0), min(b,d)-max(a,c))

def classify(exposure, pulse, contrast_lo, contrast_hi, threshold):
    a,b=map(F,exposure); c,d=map(F,pulse)
    lo,hi,t=F(contrast_lo),F(contrast_hi),F(threshold)
    if not (a<b and c<d and 0<=lo<=hi and t>=0):
        return "INVALID"
    q=overlap(a,b,c,d)/(b-a)
    if q*lo>t:
        return "GUARANTEED_DETECT"
    if q*hi<=t:
        return "GUARANTEED_UNDETECTABLE"
    return "ABSTAIN"

def tests():
    assert classify((0,10),(4,6),0,1,F(1,10))=="ABSTAIN"
    assert classify((0,10),(4,6),1,1,F(1,10))=="GUARANTEED_DETECT"
    assert classify((0,10),(4,6),1,1,F(1,5))=="GUARANTEED_UNDETECTABLE"
    assert classify((0,10),(11,12),1,1,0)=="GUARANTEED_UNDETECTABLE"
    assert classify((0,10),(4,6),0,1,0)=="ABSTAIN"
    assert classify((0,0),(4,6),0,1,0)=="INVALID"
    n=0
    for start,width,cl,ch,thr in product(range(-2,13),range(1,7),[0,F(1,4),1],[F(1,4),1,2],[0,F(1,10),F(1,2)]):
        if cl>ch: continue
        decision=classify((0,10),(start,start+width),cl,ch,thr)
        q=overlap(F(0),F(10),F(start),F(start+width))/10
        assert (decision=="GUARANTEED_DETECT")== (q*cl>thr)
        assert (decision=="GUARANTEED_UNDETECTABLE")== (q*ch<=thr)
        n+=1
    return n

if __name__=="__main__":
    print("PASS",tests(),"exact-rational cases")
