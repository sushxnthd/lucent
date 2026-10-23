from fractions import Fraction as Q

def qualify(F,w,D,m,rows):
    F,w,D,m=map(Q,(F,w,D,m))
    if not (F>0 and 0<w<=F and D>=m>0 and m<=w):
        return {"status":"ABSTAIN","reason":"invalid timing"}
    arcs=[]
    for row in rows:
        if not row.get("valid",False):continue
        if not all(k in row for k in ("offset","uncertainty","contrast","error")):continue
        d,t,c,e=(Q(row[k]) for k in ("offset","uncertainty","contrast","error"))
        if t<0 or c<=0 or e<0 or c*m<=2*e*w:continue
        L=D+w-2*m-2*t
        if L>=F:return {"status":"CERTIFIED"}
        if L>0:
            start=(d+m-D+t)%F
            end=start+L
            if end<=F:arcs.append((start,end))
            else:arcs.extend([(start,F),(Q(0),end-F)])
    arcs.sort()
    reach=Q(0)
    for a,b in arcs:
        if a>reach:return {"status":"ABSTAIN","reason":"uncovered phase"}
        reach=max(reach,b)
    return {"status":"CERTIFIED" if reach>=F else "ABSTAIN"}

if __name__=="__main__":
    F=Q(1,30);w=Q(1,100);D=Q(15,1000);m=Q(4,1000)
    rows=[dict(valid=True,offset=Q(i,200),uncertainty=Q(0),contrast=Q(2,5),error=Q(1,200)) for i in range(5)]
    assert qualify(F,w,D,m,rows)["status"]=="CERTIFIED"
    rows[0]["valid"]=rows[-1]["valid"]=False
    assert qualify(F,w,D,m,rows)["status"]=="ABSTAIN"
    print("row qualification gates PASS")
