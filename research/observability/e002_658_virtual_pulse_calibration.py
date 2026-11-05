"""E002-658: deterministic virtual LED pulse-phase shutter calibration.
Synthetic only; no measured camera data or human eyelid inference.
"""
from fractions import Fraction as F

def shutter_kernel(kind, bins=20):
    offsets=[F(2*i+1-bins,2*bins) for i in range(bins)]
    if kind=='uniform': weights=[F(1,bins)]*bins
    elif kind=='late': weights=[F(1,5) if i>=bins-5 else F(0) for i in range(bins)]
    elif kind=='early': weights=[F(1,5) if i<5 else F(0) for i in range(bins)]
    else: raise ValueError(kind)
    return offsets,weights

def pulse_scan(offsets, weights):
    return [sum(w for o,w in zip(offsets,weights) if o==phase) for phase in offsets]

def first_moment(offsets,weights):
    return sum(w*abs(o) for o,w in zip(offsets,weights))

def main():
    V=F(4); exposure=F(1,5); threshold=F(7,25)
    def aperture(t): return F(1,5)+V*abs(t)
    for kind in ('uniform','late','early'):
        offsets,weights=shutter_kernel(kind)
        scan=pulse_scan(offsets,weights)
        assert scan==weights and sum(scan)==1
        moment=first_moment(offsets,scan)
        observed=sum(w*aperture(exposure*o) for o,w in zip(offsets,weights))
        certified=observed-V*exposure*moment
        naive=observed-V*exposure*F(1,4)
        assert certified==F(1,5), (kind,certified)
        if kind!='uniform': assert naive>threshold and certified<threshold
        else: assert naive==certified
        print(kind,'moment=',float(moment),'observed=',float(observed),
              'rectangular_bound=',float(naive),'calibrated_bound=',float(certified))
    offsets,weights=shutter_kernel('late')
    scan=pulse_scan(offsets,weights)
    assert all(x==0 for x in scan[:15]) and sum(scan[15:])==1
    print('PASS: 3 exact kernels; omitted-phase calibration fails to identify late response')

if __name__=='__main__': main()
