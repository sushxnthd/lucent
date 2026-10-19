from fractions import Fraction as F
L=F(24)
T=F(1,48)
center=F(1,2)
minimum=center-L*T/4
maximum=center+L*T/4
assert minimum==F(3,8)
assert maximum==F(5,8)
assert minimum!=center
print("PASS: exact shutter-mean counterexample")
