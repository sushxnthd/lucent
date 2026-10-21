"""Exact box-shutter transfer calculations. Standard library only."""
def wasserstein_box(w1,w2,center_offset=0.0):
    assert w1>0 and w2>0
    d=abs(w1-w2); c=abs(center_offset)
    if d==0 or c>=d/2: return c
    return d/4+c*c/d

def native_fraction(interval,center,width):
    a,b=interval
    assert b>=a and width>0
    left,right=center-width/2,center+width/2
    return max(0.,min(b,right)-max(a,left))/width

def false_negative_max(short_width,long_width):
    assert 0<short_width<=long_width
    return (long_width-short_width)/(2*long_width)

def false_positive_min(short_width,long_width):
    assert 0<short_width<=long_width
    return short_width/long_width
