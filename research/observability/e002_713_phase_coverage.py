"""E002-713: exact phase-coverage audit for repeated shutters.
Synthetic instrument validation only; NOT human evidence.
Run: python research/observability/e002_713_phase_coverage.py
"""
from fractions import Fraction as F
from itertools import product

def union_length(intervals):
    """Exact measure of union of half-open intervals in [0,1)."""
    seg = sorted((max(F(0),a), min(F(1),b)) for a,b in intervals if b>a)
    total=F(0); right=F(0)
    for a,b in seg:
        if b <= a: continue
        if a > right:
            total += b-a
            right=b
        elif b > right:
            total += b-right
            right=b
    return total

def phase_detection(phases, width):
    """Fraction of closure onset phases seen by at least one ideal instantaneous sample.
    Each sample at phase p detects a closure lasting width for onset in (p-width,p].
    """
    assert F(0)<=width<=F(1)
    intervals=[]
    for p in phases:
        p=F(p)%1
        a=p-width
        if a<0:
            intervals.extend([(F(0),p),(a+1,F(1))])
        else:
            intervals.append((a,p))
    return union_length(intervals)

def test():
    assert phase_detection([F(0)],F(1,5))==F(1,5)
    assert phase_detection([F(0)]*5,F(1,5))==F(1,5)
    assert phase_detection([F(i,5) for i in range(5)],F(1,5))==1
    assert phase_detection([F(0),F(1,2)],F(1,5))==F(2,5)
    assert phase_detection([],F(1,5))==0
    # Exhaustive discrete cross-check: rational boundaries; midpoint of each cell.
    for bits in product(range(4),repeat=3):
        phases=[F(i,4) for i in bits]
        for width in [F(1,8),F(1,4),F(3,8)]:
            exact=phase_detection(phases,width)
            brute=sum(any(0 < (p-F(k,64))%1 <= width for p in phases) for k in range(64))
            # Discrete 64-grid can land on interval endpoints: bound error by 2n/64.
            assert abs(exact-F(brute,64))<=F(6,64),(bits,width,exact,brute)
    return True

if __name__=="__main__":
    test()
    w=F(1,10)
    print("E002-713 synthetic exact phase coverage")
    for name,phases in [
        ("repeated fixed phase",[F(0)]*10),
        ("ten evenly spaced phases",[F(i,10) for i in range(10)]),
        ("ten phases in first quarter",[F(i,40) for i in range(10)]),
    ]:
        print(name, str(phase_detection(phases,w)))
    print("PASS: rational invariants and exhaustive discrete cross-check")
