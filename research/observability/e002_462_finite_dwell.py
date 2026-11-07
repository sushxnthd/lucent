"""E002-462 frozen supplemental finite-duration subthreshold synthetic witness.
This is NOT a human reference recording or a physical-camera experiment.
"""
from __future__ import annotations
import json
from e002_462_reference_aliasing import C, O, THRESHOLD

def witness(fps, baseline, minimum, dwell_ms, plateau_start_ms, shutter_ms=0.3):
    if not (0 <= minimum < THRESHOLD < baseline and dwell_ms>0 and shutter_ms>0):
        raise ValueError('invalid witness')
    dt=1000/fps
    if shutter_ms>=dt:
        raise ValueError('overlapping shutter supports')
    start=plateau_start_ms-(baseline-minimum)/C
    end=plateau_start_ms+dwell_ms+(baseline-minimum)/O
    low_start=plateau_start_ms-(THRESHOLD-minimum)/C
    low_end=plateau_start_ms+dwell_ms+(THRESHOLD-minimum)/O
    def area(center):
        a,z=center-shutter_ms/2,center+shutter_ms/2
        u,v=max(a,start),min(z,plateau_start_ms)
        left=C/2*((v-start)**2-(u-start)**2) if v>u else 0
        u,v=max(a,plateau_start_ms),min(z,plateau_start_ms+dwell_ms)
        middle=(baseline-minimum)*(v-u) if v>u else 0
        u,v=max(a,plateau_start_ms+dwell_ms),min(z,end)
        right=O/2*((end-u)**2-(end-v)**2) if v>u else 0
        return left+middle+right
    means=[baseline-area(i*dt)/shutter_ms for i in range(-4,8)]
    max_deviation=max(abs(baseline-m) for m in means)
    return {'fps':fps,'baseline_mm':baseline,'minimum_mm':minimum,
            'dwell_ms':dwell_ms,'plateau_start_ms':plateau_start_ms,
            'excursion_support_ms':[start,end],
            'subthreshold_support_ms':[low_start,low_end],
            'subthreshold_duration_ms':low_end-low_start,
            'shutter_dark_gap_ms':[shutter_ms/2,dt-shutter_ms/2],
            'max_shutter_mean_difference_mm':max_deviation,
            'identical_to_constant_open':max_deviation<1e-12,
            'physical_certification':False,'evidence_tier':'SYNTHETIC_ONLY'}

def run():
    return [witness(400,2.3,1.95,.1,.9),witness(1000,2.1,1.98,.03,.38)]

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
