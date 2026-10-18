def required_duty(y,p,eta,tau):
    a=max(0,y-eta)
    b=min(1,y+eta)
    v=b**(1/p)-a
    return (1-tau)/(1-v) if v<1 else float('inf')

if __name__=='__main__':
    assert abs(required_duty(.25,2,0,.1)-1.2)<1e-12
    assert abs(required_duty(.25,1,.01,.1)-45/49)<1e-12
    for y,p,eta in ((.25,1,0),(.25,1,.01),(.25,2,0),(.25,2,.01),(.216,3,0)):
        r=required_duty(y,p,eta,.1)
        print(y,p,eta,r,r<=1)
