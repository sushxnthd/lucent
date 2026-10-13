import csv,math,pathlib
p=pathlib.Path(__file__).parent/"PAIRS.csv"
r=list(csv.DictReader(p.open()))
T=math.log(1.05)
def label(x):return (x>=T)-(x<=-T)
expected={1:(4420,162),5:(4092,302),15:(3740,377),30:(3345,357)}
for lag,(n,d) in expected.items():
 s=[x for x in r if int(x["lag"])==lag]
 a=[label(float(x["dPn"])/2) for x in s]
 b=[label(float(x["dq"])) for x in s]
 c=[label((float(x["dPn"])+float(x["dE"])-float(x["dD"]))/2) for x in s]
 assert sum(x==y for x,y in zip(a,b))==n
 assert sum(x==y and x!=z for x,y,z in zip(a,b,c))==d
assert len(r)==17903
print("Independent counts verified")
