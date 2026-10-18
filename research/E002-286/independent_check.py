"""Independent direct-pmf verification (does not import experiment.py)."""
from decimal import Decimal,getcontext
from math import factorial
getcontext().prec=55
D=Decimal
def pmf(m,k):return (-m).exp()*m**k/D(factorial(k))
def acc(T,lam0=D('.2'),lam1=D('.4'),p=D(1),nu=D(0)):
    a=T*(p*lam0+nu);b=T*(p*lam1+nu)
    return (D(1)+sum(abs(pmf(a,k)-pmf(b,k)) for k in range(400))/2)/2
rows=[
(2,.6104955409592089,.5961686589052786),
(3,.6238087120909122,.612192995053416),
(5,.6648765163165231,.6400678188977351),
(10,.7192865553147595,.6966578821375548),
(30,.8461048561085491,.8110645736274265),
(60,.9249536335237911,.8920917163502571),
(120,.9790545930114781,.9603296416072655)]
for t,a,b in rows:
    assert abs(float(acc(D(t)))-a)<1e-12
    assert abs(float(acc(D(t),p=D('.8'),nu=D(1)/60))-b)<1e-12
lo,hi=D('.1'),D('120')
for _ in range(110):
    m=(lo+hi)/2
    if acc(m)<D('.9'):lo=m
    else:hi=m
assert abs(float((lo+hi)/2)-47.59902643196009)<1e-7
assert D('.2')*D(1)==D('.4')*D('.5')
for bad in [.5,.67,.75]:
    assert abs(float(acc(D(5)))-bad)>1e-4
print('PASS: 14 numerical comparisons, exact collision, independent T90, 3 mutations')
