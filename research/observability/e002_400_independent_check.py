#!/usr/bin/env python3
"""Independent midpoint-quadrature and piecewise-trajectory oracle for E002-400."""
import json
import math
import random
from e002_400_optical_noncommutation import experiment


def midpoint_integral(fn,a,b,n=20000):
    dt=(b-a)/n
    return sum(fn(a+(i+.5)*dt) for i in range(n))/n


def check_witness():
    k=120.; valley=.1; minimum=.199; e=.1
    def aperture(t):return minimum+abs(t-valley)
    def transfer(x):return math.exp(k*(x-.299))
    results=[]
    for t in (0.,.2):
        mean=midpoint_integral(aperture,t-e/2,t+e/2)
        intensity=midpoint_integral(lambda s:transfer(aperture(s)),t-e/2,t+e/2)
        inferred=.299+math.log(intensity)/k
        results.append({'physical_mean':mean,'inverse_optical_mean':inferred})
    assert max(abs(r['physical_mean']-.299) for r in results)<1e-6
    assert abs(results[0]['inverse_optical_mean']-results[1]['inverse_optical_mean'])<1e-6
    assert results[0]['inverse_optical_mean']-.299>.025
    return results


def check_random_quadrature():
    rng=random.Random(400)
    max_bias=0.
    for rep in range(100):
        xs=[.5]
        for j in range(10):xs.append(xs[-1]+rng.uniform(-1,1)*.01)
        def x(t):
            j=min(9,int(t*100))
            z=t*100-j
            return xs[j]*(1-z)+xs[j+1]*z
        physical=midpoint_integral(x,0.,.1,2000)
        intensity=midpoint_integral(lambda t:x(t)+.5*x(t)**2,0.,.1,2000)
        inferred=math.sqrt(1+2*intensity)-1
        bias=abs(inferred-physical)
        assert bias<=1/2400+1e-8
        max_bias=max(max_bias,bias)
    return max_bias


if __name__=='__main__':
    witness=check_witness()
    result=experiment()
    assert result['naive_decision']['decision']=='CONFIRMED_NO_CROSSING'
    assert result['physical_mean_decision']['decision']=='UNRESOLVED'
    assert result['corrected_decision']['decision']=='UNRESOLVED'
    print(json.dumps({'independent_checks_passed':True,
        'witness_midpoint_integrals':witness,'random_quadrature_trials':100,
        'max_random_quadrature_bias':check_random_quadrature(),
        'human_validation':False},indent=2))
