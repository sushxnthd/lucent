"""E002-711: exact synthetic exposure-phase stress test; no human evidence."""
import math

def deficit(A,V,T,phase):
    """Integral of max(0,A-V*abs(t)) over [phase,phase+T]."""
    w=A/V
    def primitive(t):
        if t<=-w: return 0.
        if t<0: return V*(t+w)**2/2
        if t<w: return A*w/2+A*t-V*t*t/2
        return A*w
    return primitive(phase+T)-primitive(phase)

def test():
    A,V,T=1.,2.,1.5
    w=A/V
    assert abs(deficit(A,V,T,-T/2)-A*A/V)<1e-12
    assert deficit(A,V,T,w+0.01)==0
    phases=[-2+i*.001 for i in range(4001)]
    vals=[deficit(A,V,T,p) for p in phases]
    assert min(vals)>=-1e-12 and max(vals)<=A*A/V+1e-12
    for p in [-.9,-.5,-.2,0,.2,.6]:
        n=100000
        dt=T/n
        approx=sum(max(0,A-V*abs(p+(i+.5)*dt)) for i in range(n))*dt
        assert abs(approx-deficit(A,V,T,p))<2e-9,(p,approx,deficit(A,V,T,p))
    p=-T/2
    d=deficit(A,V,T,p)
    background_shift=d/T
    observed_mean=A-d/T+background_shift
    assert abs(observed_mean-A)<1e-12
    print('PASS exact integral, quadrature, phase sweep, photometric counterexample')
    print(f'A={A}, V={V}, T={T}, full deficit={d:.6f}, canceling mean offset={background_shift:.6f}')
    print('Phase outside support: deficit=0; photometric nuisance can mask full deficit')

if __name__=='__main__': test()
