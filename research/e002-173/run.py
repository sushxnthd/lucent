import csv,sys
from certificate import joint
rows=list(csv.DictReader(open(sys.argv[1])))
for lag in (1,5,15,30):
 s=[r for r in rows if int(r["lag"])==lag]
 for e in (0,.005,.01,.02,.05):
  n=sum(joint(float(r["dPn"])/2,float(r["dq"]),e) for r in s)
  print(lag,e,len(s),n,n/len(s))
