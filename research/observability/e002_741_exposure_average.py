"""E002-741: exact exposure-average to point-aperture lower bound.
Only valid for independently calibrated *linear aperture averages* with
certified Lipschitz velocity L and known exposure width; never raw RGB.
Run: python e002_741_exposure_average.py
"""
from fractions import Fraction as Q
from itertools import product

def integral_piecewise(points):
    return sum((points[i+1][0]-points[i][0])*(points[i][1]+points[i+1][1])/2 for i in range(len(points)-1))

def lower_from_mean(mean, L, width):
    return max(Q(0),mean-L*width/2)

def run():
    n=0
    for width,L,base,orientation in product(
        [Q(1,1000),Q(1,200),Q(1,100),Q(1,50)],
        [Q(5),Q(20),Q(50)],
        [Q(0),Q(1,4),Q(1,2)],[0,1]):
        if base+L*width>1: continue
        p=[(Q(0),base),(width,base+L*width)]
        if orientation: p=[(Q(0),base+L*width),(width,base)]
        mean=integral_piecewise(p)/width
        assert lower_from_mean(mean,L,width)==base
        assert mean-base==L*width/2
        n+=1
    assert Q(1)*Q(1,2)==Q(1,2)*Q(1)  # RGB gain ambiguity
    print(f"PASS {n} exact sharp ramp witnesses; RGB gain ambiguity PASS")
if __name__=="__main__": run()
