from fractions import Fraction as F
import json
N=90
a=[[F(3)]*N,[F(4)]*N,[F(5)]*N]
b=[[F(5)]*N,[F(4)]*N,[F(3)]*N]
fold=lambda x:[sum((x[s][i] for s in range(3)),F(0))/3 for i in range(N)]
assert a!=b and fold(a)==fold(b)==[F(4)]*N
for i in range(N):
 d=[F(int(j==i)) for j in range(N)]
 z=[F(0)]*N
 assert fold([d,[-v for v in d],z])==z
 assert fold([z,d,[-v for v in d]])==z
print(json.dumps({"raw_samples":270,"released_rows":90,"rank":90,
"nullity":180,"counterexample_A":[3,4,5],"counterexample_B":[5,4,3],
"same_folded_label":4,"exact_kernel_checks":180,"human_data":False},indent=2))
