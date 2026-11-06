#!/usr/bin/env python3
"""E002-680: deterministic phase-locked synthetic blink aliasing challenge.
No physiological parameters inferred; normalized aperture and ideal box exposure."""
import json
def aperture(t,d):
    if t<0 or t>d:return 1.0
    return abs(2*t/d-1)
def measured(t,d,exposure):
    if exposure==0:return aperture(t,d)
    n=200
    return sum(aperture(t+exposure*(i+.5)/n,d) for i in range(n))/n
def run():
    rows=[]
    for duration in (0.010,0.020,0.040,0.060):
        for exposure in (0.,0.005,0.010):
            miss=0
            for phase_i in range(1000):
                phase=(phase_i+.5)/1000/30
                samples=[measured(phase+k/30,duration,exposure) for k in range(-2,5)]
                if min(samples)>0.30:miss+=1
            rows.append(dict(blink_duration_ms=round(duration*1000),exposure_ms=round(exposure*1000),missed_phases=miss,total_phases=1000,miss_fraction=miss/1000))
    return rows
if __name__=="__main__":
    print(json.dumps(run(),indent=2))
