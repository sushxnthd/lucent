"""Exact rational single-exposure active-probe observability boundary."""
from fractions import Fraction as F

def overlap(s,E,delta,lo,hi):
    return max(F(0),min(s+delta+E,hi)-max(s+delta,lo))

def candidates(s,E,Delta,tp,duration,tc):
    xs={-Delta,Delta}
    for t in (F(0),tc,tp,tp+duration):
        for v in (t-s,t-s-E):
            if -Delta<=v<=Delta:xs.add(v)
    return sorted(xs)

def evaluate(s,E,Delta,tp,duration,tc,A,B,eta):
    assert E>0 and Delta>=0 and duration>0 and tc>=0
    assert A>=0 and B>=0 and eta>=0
    vals=[]
    for delta in candidates(s,E,Delta,tp,duration,tc):
        p=overlap(s,E,delta,tp,tp+duration)/E
        n=overlap(s,E,delta,F(0),tc)/E
        vals.append((p,n))
    max_n=max(n for p,n in vals)
    alt_lo=min(A*p-B*n for p,n in vals)-eta
    alt_hi=max(A*p+B*n for p,n in vals)+eta
    null_lo=-B*max_n-eta;null_hi=B*max_n+eta
    margin=alt_lo-null_hi
    assert alt_hi>=null_lo
    return {"margin":margin,"certify":margin>0,
            "null_interval":(null_lo,null_hi),
            "alt_interval":(alt_lo,alt_hi),
            "nuisance_max":max_n,"candidates":len(vals)}

def critical_start(E,Delta,tc,A,B,eta):
    assert B>0 and 0<A-2*eta<2*B
    return tc+Delta-E*(A-2*eta)/(2*B)
