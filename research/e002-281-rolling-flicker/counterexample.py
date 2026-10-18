from fractions import Fraction as F
P=F(1,30);T=F(1,120);d=F(1,80)
assert d>T and d+T<P
b=[F(1),F(1),F(1,2),F(1)]
world_blink=[(F(3,5)*x,F(9,20)) for x in b]
world_flicker=[(F(3,5)*x,F(9,20)) for x in b]
assert world_blink==world_flicker
print('two-patch exact equivalence; not full-frame equivalence')
