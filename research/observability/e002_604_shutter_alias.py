#!/usr/bin/env python3
"""E002-604 frozen synthetic global-shutter counterexample; no human validation."""
import json
from math import isclose

W = .010
THETA = .2
N = 10000


def deficit_primitive(t, w=W):
    """Integral of max(0,1-2*abs(t)/w) from -infinity to t."""
    if t <= -w/2:
        return 0.
    if t < 0:
        x = t + w/2
        return x*x/w
    if t < w/2:
        return w/4 + t - t*t/w
    return w/2


def aperture_at(t, w=W):
    return 1 - max(0., 1-2*abs(t)/w)


def shutter_average(center, exposure, w=W):
    assert exposure > 0
    return 1 - (deficit_primitive(center+exposure/2,w)-deficit_primitive(center-exposure/2,w))/exposure


def min_integrated(w, exposure):
    return exposure/(2*w) if exposure <= w else 1-w/(2*exposure)


def miss_fraction(fps, exposure, instantaneous=False, w=W, theta=THETA, n=N):
    period = 1/fps
    misses = 0
    for j in range(n):
        phase = period*j/n
        observed = [aperture_at(k*period+phase, w) if instantaneous else
                    shutter_average(k*period+phase, exposure, w)
                    for k in range(-4, 5)]
        if min(observed) > theta:
            misses += 1
    return misses/n


def run():
    checks = []
    for e in (.002,.005,.010,.020):
        observed = shutter_average(0., e)
        predicted = min_integrated(W,e)
        assert isclose(observed,predicted,abs_tol=1e-12), (e,observed,predicted)
        checks.append({'exposure_ms':round(e*1000,6), 'predicted_min_aperture':round(predicted,9), 'integrated_min_aperture':round(observed,9)})
    cases = []
    for fps,e in ((30,.020),(95,.005),(95,.002)):
        avg_miss = miss_fraction(fps,e)
        point_miss = miss_fraction(fps,e,True)
        if (fps,e) in ((30,.020),(95,.005)):
            assert avg_miss == 1., (fps,e,avg_miss)
        cases.append({'fps':fps,'exposure_ms':round(e*1000,6), 'average_missed_fraction':avg_miss,'point_missed_fraction':point_miss})
    return {'experiment':'E002-604','tier':'SYNTHETIC_PHYSICAL_MEASUREMENT_MODEL_ONLY','phase_count':N,'triangular_closure_duration_ms':W*1000,'assumed_velocity_aperture_per_s':2/W,'threshold':THETA,'minima':checks,'cases':cases,'human_sequences':0,'physical_shutter_calibrations':0,'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True))
