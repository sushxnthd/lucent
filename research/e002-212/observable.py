from math import pi,asin,sqrt

def area(r,h):
    if h<=-r:return 0.
    if h>=r:return pi*r*r
    return r*r*(pi/2+asin(h/r))+h*sqrt(r*r-h*h)

def ratio(r,h):
    return area(r,h)/area(1.,h)

def projective_ratio(r,k):
    return r*r*((1-k*k)/(1-k*k*r*r))**1.5
