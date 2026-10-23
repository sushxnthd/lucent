"""Conservative camera qualification; not a human blink or fatigue detector."""
from fractions import Fraction as Q

def qualify(F,w,m,rows):
    try:
        F,w,m=map(Q,(F,w,m))
        if not (F>0 and 0<m<=w<=F):return {"status":"ABSTAIN","reason":"invalid shutter"}
        segments=[];qualified=0
        for r in rows:
            keys=("offset","onset_delay","uncertainty","duration_lower","contrast_lower","residual_bound")
            if not r.get("valid",False) or any(k not in r for k in keys):continue
            d,t,u,D,c,e=(Q(r[k]) for k in keys)
            if u<0 or D<m or c<=0 or e<0 or c*m<=2*e*w:continue
            qualified+=1
            L=D+w-2*m-2*u
            if L>=F:return {"status":"CERTIFIED","scope":"row-event only"}
            if L<0:continue
            a=(d-t+m-D+u)%F;b=a+L
            if b<=F:segments.append((a,b))
            else:segments.extend([(a,F),(Q(0),b-F)])
        reach=Q(0)
        for a,b in sorted(segments):
            if a>reach:return {"status":"ABSTAIN","reason":"uncovered phase","qualified_rows":qualified}
            reach=max(reach,b)
        if reach>=F:return {"status":"CERTIFIED","scope":"row-event only","qualified_rows":qualified}
        return {"status":"ABSTAIN","reason":"missing optical or temporal calibration","qualified_rows":qualified}
    except (ValueError,TypeError,KeyError,ZeroDivisionError):
        return {"status":"ABSTAIN","reason":"invalid calibration"}

def run():
    def rows(alpha,u=Q(0)):
        return [dict(valid=True,offset=Q(i,200),onset_delay=alpha*Q(i,200),
                     uncertainty=u,duration_lower=Q(15,1000),
                     contrast_lower=Q(3,5),residual_bound=Q(1,100)) for i in range(5)]
    F,w,m=Q(1,30),Q(1,100),Q(4,1000)
    assert qualify(F,w,m,rows(Q(18,100)))["status"]=="CERTIFIED"
    assert qualify(F,w,m,rows(Q(19,100)))["status"]=="ABSTAIN"
    assert qualify(F,w,m,rows(Q(18,100),Q(1,5000)))["status"]=="ABSTAIN"
    assert qualify(F,w,m,rows(Q(0))[:2])["status"]=="ABSTAIN"
    assert qualify(F,w,m,rows(Q(0),Q(0))[:2])["status"]=="ABSTAIN"
    print("E002-381 product abstention gates PASS")
if __name__=="__main__":run()
