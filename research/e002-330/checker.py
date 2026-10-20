from itertools import permutations
from math import ceil,inf
def B(s,a):
 k=ceil((len(s)+1)*(1-a))
 return sorted(s)[k-1] if k<=len(s) else inf
v=[1,2,3,4,5]
p=list(permutations(v))
assert sum(x[-1]<=B(x[:-1],.2) for x in p)==96
assert B([0]*18,.05)==inf
assert B([0]*19,.05)==0
print("PASS: 96/120 exact rank outcomes; 95% requires >=19 calibration participants")