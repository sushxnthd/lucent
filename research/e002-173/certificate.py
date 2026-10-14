import math
T=math.log(1.05)
def certificate(v,e):
    assert 0<=e<1
    h=2*math.log((1+e)/(1-e))
    lo,hi=v-h,v+h
    if lo>T:return 1
    if hi<-T:return -1
    if -T<lo and hi<T:return 0
    return None
def joint(a,b,e):
    x,y=certificate(a,e),certificate(b,e)
    return x is not None and x==y
