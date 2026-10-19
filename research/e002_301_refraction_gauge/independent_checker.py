import sympy as s
from fractions import Fraction as F
H=s.Matrix([[2,1,1],[1,3,2],[s.Rational(1,5),-s.Rational(1,7),1]])
q=s.Rational(2,5);k=s.Rational(103,100)
K=s.diag(k,k,1); Ci=H.inv().T*s.diag(1,1,-1)*H.inv()
A=(H*K).inv().T*s.diag(1,1,-q*q)*(H*K).inv()
B=H.inv().T*s.diag(1,1,-(k*q)**2)*H.inv()
assert s.simplify(A*k*k-B)==s.zeros(3) # homogeneous conic equality
z=s.symbols('z')
p=s.factor((A-z*Ci).det()/(-Ci.det()))
assert s.factor(p/((z-1/k**2)**2*(z-q**2))) in (1,-1)
d=F(3,100); c=(1+d)/(1-d)
assert c==F(103,97)
assert F(26,25)<c and F(53,50)<c<F(107,100)
print('independent exact rational checker PASSED')
