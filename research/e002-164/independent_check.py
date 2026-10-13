"""Independent exact-rational checker for E002-164; no fold function import."""
from fractions import Fraction
from pathlib import Path
import json,math
r=json.loads(Path(__file__).with_name("RESULTS.json").read_text())
rows=[{i:Fraction(1,3),i+90:Fraction(1,3),i+180:Fraction(1,3)} for i in range(90)]
assert len({min(row) for row in rows})==90
x=[Fraction(3)+Fraction(9,10)*Fraction(k,90) for k in range(270)]
y=[sum(x[j]*v for j,v in row.items()) for row in rows]
assert (y[89]-y[0])/Fraction(89,30)==Fraction(3,10)
for i in range(90):
    for j,k in ((i,i+90),(i,i+180)):
        v={j:Fraction(1),k:Fraction(-1)}
        assert all(sum(row.get(a,0)*b for a,b in v.items())==0 for row in rows)
for z in (complex(-.5,math.sqrt(3)/2),complex(-.5,-math.sqrt(3)/2)):
    assert abs(1+z+z*z)<1e-14
assert r["rank"]==90 and r["nullity"]==180
assert r["slope_retention"]==1/3
print("PASS independent matrix, 180 null vectors and two harmonic zeros")
