import csv,math
from pathlib import Path
rows=list(csv.DictReader(Path("research/e002-203/selected_trial_marginals.csv").open()))
assert len(rows)==15
L=[int(r["left_valid"]) for r in rows]
R=[int(r["right_valid"]) for r in rows]
counts=[sum(v>=570 for v in L),sum(v>=570 for v in R),
        sum(max(a,b)>=570 for a,b in zip(L,R)),
        sum(min(a,b)>=570 for a,b in zip(L,R))]
assert counts==[11,10,11,10]
assert max(counts[:3])<math.ceil(.75*len(rows))
print("PASS verified 15-trial marginal ceiling",counts)
