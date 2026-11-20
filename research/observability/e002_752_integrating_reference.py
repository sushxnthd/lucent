"""E002-752: exact rational phase sweep of an ideal integrating reference detector.
Synthetic only; samples integrate [k,k+exposure], firing at occupancy >= threshold.
"""
from fractions import Fraction as F

def overlap(a,b,c,d):
    return max(F(0), min(b,d)-max(a,c))

def detected(phase,duration,exposure,threshold):
    return any(overlap(phase,phase+duration,F(k),F(k)+exposure)>=threshold*exposure for k in range(-1,4))

def sweep(duration,exposure,threshold,n=10000):
    return sum(detected(F(i,n),duration,exposure,threshold) for i in range(n))

if __name__=="__main__":
    for exposure in (F(1,4),F(1,2),F(1)):
        for threshold in (F(1,4),F(1,2),F(3,4)):
            for duration in (F(1,4),F(1,2),F(3,4),F(1)):
                count=sweep(duration,exposure,threshold)
                assert 0<=count<=10000
                if duration<threshold*exposure: assert count==0
                print(f"{duration},{exposure},{threshold},{count}")
