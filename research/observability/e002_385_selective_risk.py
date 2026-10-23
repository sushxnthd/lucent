"""E002-385 compact reproducible synthetic test; seed 20261023. No human data."""
import json, numpy as np
R=np.random.default_rng(20261023);F=1/30;W=.01;V=40.;H=F-W
c=(W+F)/2;k=.81/V
b=(min(c-k,W)+((W-max(c-k,0))*(1+(.19+V*(c-W)))/2))/W
def make(counts):
    kinds=np.concatenate([np.full(n,s,dtype='U12') for s,n in counts]);R.shuffle(kinds)
    true=np.where(kinds[:,None]=='open',1.,b);true=np.broadcast_to(true,(len(kinds),2)).copy()
    est=np.clip(true+R.uniform(-.002,.002,true.shape)+.06*(kinds=='shifted')[:,None],0,1)
    return kinds,true,est
def cert(est,e):
    a=np.maximum(0,est-e);d=np.where(1-a<=V*W/2,np.sqrt(2*V*W*np.maximum(0,1-a)),1-a+V*W/2)
    lo=np.maximum(0,1-np.minimum(1,d));L,T=lo[:,0],lo[:,1]
    return np.maximum.reduce([L-V*H,T-V*H,(L+T-V*H)/2])>.2
cal=make([('open',500),('hidden',500)]);q=float(np.quantile(np.max(np.abs(cal[2]-cal[1]),axis=1),.99,method='higher'))
sets={'heldout':[('open',500),('hidden',9400),('shifted',100)],'unseen_device':[('open',500),('hidden',9200),('shifted',300)],'clean_control':[('open',500),('hidden',9500)]}
cohorts={s:make(c) for s,c in sets.items()}
output={'q_clip99':q,'conditions':{}}
for name,(k,t,e) in cohorts.items():
    error=np.max(np.abs(e-t),axis=1);naive=cert(e,q);flags=R.random(len(k))<np.where(k=='shifted',.8,.02)
    flagged=naive&~flags;oracle=cert(e,error[:,None]+1e-12)
    row=lambda mask:{'issued':int(mask.sum()),'false':int((mask&(k!='open')).sum())}
    output['conditions'][name]={'coverage':float(np.mean(error<=q)),'naive':row(naive),'flagged':row(flagged),'oracle':row(oracle),'product':{'issued':0,'reason':'no independently validated hard optical bound'}}
print(json.dumps(output,indent=2))
