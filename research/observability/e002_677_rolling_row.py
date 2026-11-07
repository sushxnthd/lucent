from fractions import Fraction as F
"""E002-677: adversarial rolling-row timestamp mismatch, exact arithmetic."""
V=F(30); tau=F(3,10)
rows=[]
for nominal_ms in (30,35,40,45,50):
    for skew_ms in (0,5,10,15):
        nominal=F(nominal_ms,1000)
        actual=F(nominal_ms+2*skew_ms,1000)
        naive_excludes=V*nominal < 2*(1-tau)
        hidden_possible=V*actual >= 2*(1-tau)
        corrected_excludes=V*actual < 2*(1-tau)
        assert not (corrected_excludes and hidden_possible)
        rows.append((nominal_ms,skew_ms,naive_excludes,hidden_possible))
violations=[r for r in rows if r[2] and r[3]]
assert len(rows)==20 and len(violations)==10
assert (40,10,True,True) in violations
print("cases",len(rows),"false_nominal_certificates",len(violations))
print("witness nominal_gap_ms=40 row_skew_each_end_ms=10 actual_gap_ms=60")
