def dose_interval(y, p, eta=0.0, duty=1.0, window=5.0):
    """Exact conditional bounds for mean(c**p), 0<=c<=1, p>=1."""
    assert p>=1 and 0<=y<=1 and 0<duty<=1
    lo=max(0.0,y-eta)
    hi=min(1.0,y+eta)
    return (window*duty*lo, window*(duty*hi**(1.0/p)+1.0-duty))

if __name__=='__main__':
    print(dose_interval(.25,2,0,1))
    print(dose_interval(.25,2,.01,.5))
    assert dose_interval(.216,3,0,1)==(1.08,3.0)
