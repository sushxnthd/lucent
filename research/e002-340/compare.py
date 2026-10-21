from model import qnorm
for p in ((1,3,7),(1,2,8),(2,5,8),(1,2,3)):
    q=min(qnorm(p,t) for t in (.11,.27,.65,1.35))
    print(p,q,q/2)
