"""Isolated wildcard: rowwise skip-NaN means need not preserve session mean."""
from fractions import Fraction
g=[[Fraction(1),Fraction(1)],[Fraction(1),Fraction(1)],[None,Fraction(9)]]
raw=[v for a in g for v in a if v is not None]
fold=[sum(a[i] for a in g if a[i] is not None)/sum(a[i] is not None for a in g) for i in range(2)]
assert sum(raw)/len(raw)==Fraction(13,5)
assert sum(fold)/len(fold)==Fraction(7,3)
assert sum(raw)/len(raw)-sum(fold)/len(fold)==Fraction(4,15)
print("PASS missingness counterexample")
