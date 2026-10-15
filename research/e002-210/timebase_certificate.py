#!/usr/bin/env python3
"""E002-210 exact clock-offset admission. Synthetic/exact; zero human outcomes."""
import json
import math

def lag_interval_ms(apparent_lag_ms, offset_bound_ms):
    if offset_bound_ms is None:
        return None
    if not (math.isfinite(apparent_lag_ms) and math.isfinite(offset_bound_ms) and offset_bound_ms >= 0):
        raise ValueError("invalid clock bound or lag")
    return [apparent_lag_ms-offset_bound_ms, apparent_lag_ms+offset_bound_ms]

def certify_lag(apparent_lag_ms, offset_bound_ms, gate_ms=100.0):
    if not math.isfinite(gate_ms) or gate_ms < 0:
        raise ValueError("invalid gate")
    interval = lag_interval_ms(apparent_lag_ms, offset_bound_ms)
    if interval is None:
        return {"admit":False,"reason":"UNBOUNDED_CLOCK_ERROR","interval_ms":None}
    worst = max(abs(interval[0]),abs(interval[1]))
    return {"admit":worst <= gate_ms+1e-12,"reason":"PASS" if worst <= gate_ms+1e-12 else "LAG_NOT_CERTIFIABLE","interval_ms":interval,"worst_ms":worst}

def sinusoid_max_error_amplitudes(f_hz, e_ms):
    if not (math.isfinite(f_hz) and f_hz >= 0 and math.isfinite(e_ms) and e_ms >= 0):
        raise ValueError("invalid frequency/error")
    return 2*math.sin(min(math.pi*f_hz*e_ms/1000,math.pi/2))

def run():
    cases = [(40,50),(40,70),(-80,15),(0,None),(0,100),(100,1)]
    return {"run":"E002-210","kind":"EXACT_THEOREM_AND_SYNTHETIC_CONTROLS","human_RGB_tracker_pairs":0,
            "cases":[{"apparent_ms":lag,"offset_bound_ms":e,"certificate":certify_lag(lag,e)} for lag,e in cases],
            "frequency_table":[{"frequency_hz":f,"clock_bound_ms":e,"max_error_in_signal_amplitudes":sinusoid_max_error_amplitudes(f,e)}
                for f in (0.5,1.0,2.0,4.0) for e in (25,50,100)],
            "EVE_admission":{"basler_reference_clock":"DOCUMENTED_RELIABLE","webcam_reference_clock":"UNBOUNDED_BY_PUBLIC_DOCUMENTATION",
                             "webcam_lag_certificate":"REJECT_UNTIL_BOUND_ESTABLISHED","pupil_labels":"left_p/right_p IN HDF; NATIVE_TRACKER_TIMEBASE_UNVERIFIED",
                             "access":"ON_REQUEST_NOT_OBTAINED"}}

if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True,indent=2))
