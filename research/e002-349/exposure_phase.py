"""Lucent E002-349: finite-exposure event observability. Conditional model only."""
def overlap(s,D,t,w):
    return max(0.0,min(s+D,t+w)-max(s,t))

def minimax_overlap(D,F,w):
    if not (0<w<=F and D>=0): raise ValueError("invalid camera")
    return min(w,max(0.0,(D-F+w)/2))

def sharp_boundary(F,w,eps):
    if not (0<w<=F and eps>=0): raise ValueError("invalid")
    return float("inf") if eps>=.5 else F-w+4*eps*w

def detector_boundary(F,w,q,eps):
    if not (0<w<=F and 0<=q<=1 and eps>=0): raise ValueError("invalid")
    return float("inf") if q+eps>1 else F-w+2*(q+eps)*w

def identifiable(D,F,w,eps):
    return minimax_overlap(D,F,w)/w>2*eps+1e-12

def observed_fraction(s,D,F,w,k):
    return overlap(s,D,k*F,w)/w

if __name__=="__main__":
    F=1/30; w=.010; eps=.05
    print("sharp hypothesis boundary ms:",1000*sharp_boundary(F,w,eps))
    print("q=.5 detector boundary ms:",1000*detector_boundary(F,w,.5,eps))
