from fractions import Fraction
r=Fraction(1,2)
assert (1-r)/(1+r)==Fraction(1,3)
delta=Fraction(6,100)
exc=Fraction(25,100)
assert (2*exc-delta)/(2*exc+delta)==Fraction(11,14)
print('PASS exact rational boundary; human validation NOT RUN')
