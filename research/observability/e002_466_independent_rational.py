#!/usr/bin/env python3
"""Independent exact rational E002-466 check, no JS imports or floating point."""
from fractions import Fraction as F

def main():
    start, end, width, step, floor = F(0), F(2,5), F(1,10), F(1,20), F(3,20)
    phases = [F(-3,10) + i * step for i in range(24)]
    def overlap(t):
        return max(F(0), min(end, t+width) - max(start,t))
    positive = [i for i,t in enumerate(phases) if overlap(t)/(end-start) > floor]
    first,last = positive[0],positive[-1]
    naive_start = (phases[first-1]+width,phases[first]+width)
    naive_end = (phases[last],phases[last+1])
    assert not (naive_start[0] <= start <= naive_start[1])
    assert not (naive_end[0] <= end <= naive_end[1])
    dead_zone = floor * (end-start)
    safe_start = (naive_start[0]-dead_zone,naive_start[1])
    safe_end = (naive_end[0],naive_end[1]+dead_zone)
    assert safe_start[0] <= start <= safe_start[1]
    assert safe_end[0] <= end <= safe_end[1]
    assert dead_zone == F(3,50)
    print('E002-466 independent exact-rational PASS')
    print('naive start/end', naive_start, naive_end)
    print('safe start/end', safe_start, safe_end)
    print('dead zone',dead_zone)

if __name__ == '__main__':
    main()
