from fractions import Fraction as F
import sympy as s
x=[F(0),F(1,3),F(2,3),F(1)]
a=[F(0),F(9,10),F(0),F(1,10)]
b=[F(11,20),F(0),F(9,20),F(0)]
m=lambda w,k:sum((v*t**k for v,t in zip(w,x)),F(0))
for k in (0,2,3):
    assert m(a,k)==m(b,k)
assert m(a,1)-m(b,1)==F(1,10)
mat=s.Matrix([[1]*4,[s.Rational(z.numerator,z.denominator)**2 for z in x],[s.Rational(z.numerator,z.denominator)**3 for z in x]])
assert len(mat.nullspace())==1
assert m(a,2)==F(1,5) and m(a,3)==F(2,15)
print('Exact collision, moments and symbolic nullspace: PASS')
