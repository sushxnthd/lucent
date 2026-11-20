"""Exact phase-coverage test for an ideal point-sampled reference detector.

A closure pulse of width d occurs at phase p within a period h=1.
Samples occur at integer times; endpoints count as detected.
No analog bandwidth, noise or eyelid physiology is modeled.
"""
from fractions import Fraction

def detected(phase, width):
    return phase + width >= 1 or phase == 0

def sweep(n=10000):
    widths=[Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1),Fraction(5,4)]
    for w in widths:
        count=sum(detected(Fraction(i,n),w) for i in range(n))
        expected=n if w>=1 else min(n, (n*w).numerator//(n*w).denominator+1)
        assert count==expected,(w,count,expected)
        print(f'd_over_h={w} detected={count}/{n} missed={n-count}/{n}')
    for w in widths[:3]:
        p=(1-w)/2
        assert not detected(p,w)
    print('PASS: exact phase enumeration and adversarial missed pulses')
if __name__=='__main__': sweep()
