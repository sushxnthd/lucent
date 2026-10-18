import math,json
from experiment import H
from pathlib import Path
N=16384; C=.12; eta=.005
cases=[("same",100,1/120,0,.6),("offset5",100,1/120,.005,.6),
("offset2p5",100,1/120,.0025,.6),("offset10",100,1/120,.01,.6),
("exp10",100,1/100,.005,.6),("matched120",120,1/120,.004,.6),
("holdout117",117,1/90,.0031,.55)]
def run():
 out=[]
 for name,f,T,d,a in cases:
  h=H(f,T,d,a);b=a*math.sin(math.pi*f*T)/(math.pi*f*T)
  g=math.pi*f*d
  v=[math.log1p(b*math.cos(2*math.pi*i/N+g))-math.log1p(b*math.cos(2*math.pi*i/N-g)) for i in range(N)]
  pairs=[v[(i*7919+17)%N]-v[(i*37+11)%N] for i in range(N)]
  out.append(dict(id=name,H=h,pair_bound=2*h,minimum=min(v),maximum=max(v),false_pair=sum(x-4*eta<=-C for x in pairs)))
 Path(__file__).with_name("results.json").write_text(json.dumps(out,indent=2)+"\n")
 return out
if __name__=="__main__":print(run())
