#!/usr/bin/env python3
"""E002-399: interval-valued high-speed *reference* adequacy, not a blink detector.

All inputs must be independently calibrated normalized physical aperture *exposure
means*, not image proxy values. No human data are bundled or claimed.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import argparse
import json
import math
import random
from typing import Sequence


@dataclass(frozen=True)
class Frame:
    t: float
    mean_lo: float
    mean_hi: float
    exposure: float
    clock_error: float
    # Independently bounded E_w|time - nominal_center|; None only for verified
    # uniform temporal kernels in direct E002-399 synthetic callers.
    temporal_first_abs_moment_s: float | None = None


@dataclass(frozen=True)
class Calibration:
    speed_upper: float
    threshold: float
    independent_velocity: bool = False
    aperture_geometry: bool = False
    optical_response: bool = False
    exposure_timing: bool = False
    clock_synchronization: bool = False
    nuisance_resolved: bool = False
    uniform_shutter_verified: bool = False

    def qualified(self):
        return (self.independent_velocity and self.aperture_geometry and
                self.optical_response and self.exposure_timing and
                self.clock_synchronization and self.nuisance_resolved and
                self.uniform_shutter_verified)


@dataclass(frozen=True)
class Result:
    decision: str
    lower_min: float | None
    witnessed_upper: float | None
    interval_start: float | None
    interval_end: float | None
    reason: str


def _finite(*values):
    return all(math.isfinite(v) for v in values)


def exact_lower_envelope_min(times: Sequence[float], lower: Sequence[float], speed: float) -> float:
    """Exact min_t max_i [L_i - V |t-t_i|] over [first,last] for sorted centers.

    Computes prefix and suffix cone envelopes; each inter-frame envelope is
    the maximum of a decreasing and an increasing line, so its minimum is
    attained at their clipped intersection. O(n), no time discretization.
    """
    n = len(times)
    if n != len(lower) or n == 0:
        raise ValueError('Nonempty equal-length arrays required')
    if n == 1:
        return lower[0]
    if speed == 0:
        return max(lower)
    left = [0.0] * n
    right = [0.0] * n
    left[0] = lower[0]
    for i in range(1, n):
        left[i] = max(lower[i], left[i-1] - speed*(times[i]-times[i-1]))
    right[-1] = lower[-1]
    for i in range(n-2, -1, -1):
        right[i] = max(lower[i], right[i+1] - speed*(times[i+1]-times[i]))
    answer = float('inf')
    for i in range(n-1):
        gap = times[i+1]-times[i]
        x = max(0.0, min(gap, (left[i]-right[i+1]+speed*gap)/(2*speed)))
        local = max(left[i]-speed*x, right[i+1]-speed*(gap-x))
        answer = min(answer, local)
    return answer


def certify(frames: Sequence[Frame], calibration: Calibration) -> Result:
    if not calibration.qualified():
        return Result('ABSTAIN_UNCALIBRATED', None, None, None, None,
                      'Missing independent aperture, shutter, timing, velocity, optical or nuisance calibration')
    if not _finite(calibration.speed_upper, calibration.threshold) or calibration.speed_upper < 0:
        raise ValueError('Invalid speed/threshold')
    if len(frames) < 2:
        return Result('UNRESOLVED', None, None, None, None, 'Need >=2 valid frames for interval')
    ts, lower, upper = [], [], []
    for f in frames:
        if not _finite(f.t, f.mean_lo, f.mean_hi, f.exposure, f.clock_error):
            raise ValueError('Nonfinite reference data')
        if f.exposure <= 0 or f.clock_error < 0 or f.mean_lo > f.mean_hi:
            raise ValueError('Invalid exposure/uncertainty/mean interval')
        if ts and f.t <= ts[-1]:
            raise ValueError('Frame centers must be strictly increasing')
        ts.append(f.t)
        # e/4 is valid for uniform temporal integration ONLY. For calibrated
        # nonuniform shutters the independently bounded first absolute moment
        # is required (E002-403). Human annotation bridge always supplies it.
        moment = f.exposure/4 if f.temporal_first_abs_moment_s is None else f.temporal_first_abs_moment_s
        if not _finite(moment) or moment < 0 or moment > f.exposure/2 + 1e-12:
            raise ValueError('Invalid shutter temporal first absolute moment')
        correction = calibration.speed_upper*(moment + f.clock_error)
        lower.append(f.mean_lo-correction)
        upper.append(f.mean_hi+correction)
    min_lower = exact_lower_envelope_min(ts, lower, calibration.speed_upper)
    witnessed_upper = min(upper)
    if witnessed_upper < calibration.threshold:
        decision, reason = 'CONFIRMED_CROSSING', 'A calibrated exposure forces a below-threshold instantaneous center'
    elif min_lower > calibration.threshold:
        decision, reason = 'CONFIRMED_NO_CROSSING', 'Entire bounded interval lies above threshold'
    else:
        decision, reason = 'UNRESOLVED', 'Reference permits both crossing and no-crossing trajectories'
    return Result(decision, min_lower, witnessed_upper, ts[0], ts[-1], reason)


def calibrated(speed=60., threshold=.2):
    return Calibration(speed, threshold, True, True, True, True, True, True, True)


def triangular(t, center, baseline=.85, minimum=.10, speed=60.):
    width=(baseline-minimum)/speed
    return baseline-(baseline-minimum)*max(0., 1.-abs(t-center)/width)


def integrate_triangle(a, b, center, baseline=.85, minimum=.10, speed=60.):
    """Analytic integral via exact linear-segment trapezoids."""
    width=(baseline-minimum)/speed
    pts=[a]+sorted(v for v in (center-width,center,center+width) if a<v<b)+[b]
    area=sum((triangular(x,center,baseline,minimum,speed)+triangular(y,center,baseline,minimum,speed))*(y-x)/2
             for x,y in zip(pts,pts[1:]))
    return area/(b-a)


def simulate(seed=399, n=200):
    rng=random.Random(seed)
    configs={
        'open_240': (240., .001, 'open', False, .85),
        'crossing_960': (960., .0005, 'cross', False, .85),
        'crossing_30': (30., .010, 'cross', False, .85),
        'marginal_240_full': (240., .0005, 'open', False, .38),
        'marginal_240_missing': (240., .0005, 'open', True, .38),
    }
    outputs={}
    total_wrong=0
    for name,(fps,exposure,kind,drop,baseline) in configs.items():
        counts={'CONFIRMED_CROSSING':0,'CONFIRMED_NO_CROSSING':0,'UNRESOLVED':0,
                'ABSTAIN_UNCALIBRATED':0,'wrong_certificates':0}
        for rep in range(n):
            phase=rng.uniform(0,1/fps)
            delta=.0001
            frames=[]
            i=0
            while True:
                t=phase+i/fps
                if t>.2: break
                if not drop or i%2==0:
                    true_t=t+rng.uniform(-delta,delta)
                    if kind=='cross':
                        mean=integrate_triangle(true_t-exposure/2,true_t+exposure/2,.1)
                    else:
                        mean=baseline
                    observed=mean+rng.uniform(-.005,.005)
                    frames.append(Frame(t,observed-.02,observed+.02,exposure,delta))
                i+=1
            result=certify(frames,calibrated())
            counts[result.decision]+=1
            true_cross=(kind=='cross' and frames[0].t <= .1 <= frames[-1].t)
            wrong=((result.decision=='CONFIRMED_CROSSING' and not true_cross) or
                   (result.decision=='CONFIRMED_NO_CROSSING' and true_cross))
            if wrong: counts['wrong_certificates']+=1; total_wrong+=1
            if rep==0:
                counts['example']={'result':asdict(result),'frame_count':len(frames)}
            widened=[Frame(f.t,f.mean_lo-.05,f.mean_hi+.05,f.exposure,f.clock_error+.001) for f in frames]
            result_wide=certify(widened,calibrated())
            if result.decision=='UNRESOLVED' and result_wide.decision!='UNRESOLVED':
                raise AssertionError('P7 violated: uncertainty made unresolved into a certificate')
        outputs[name]=counts
    assert outputs['open_240']['CONFIRMED_NO_CROSSING']>=.95*n, 'P1 failed'
    assert outputs['crossing_960']['CONFIRMED_CROSSING']>=.95*n, 'P2 failed'
    assert outputs['crossing_30']['CONFIRMED_CROSSING']<=.30*n, 'P3 failed'
    assert outputs['marginal_240_full']['CONFIRMED_NO_CROSSING']>=.95*n, 'P4a failed'
    assert outputs['marginal_240_missing']['UNRESOLVED']>=.95*n, 'P4b failed'
    sample=[Frame(0.,.8,.9,.001,.0001),Frame(.004,.8,.9,.001,.0001)]
    invalid=Calibration(60.,.2,False,True,True,True,True,True,True)
    assert certify(sample,invalid).decision=='ABSTAIN_UNCALIBRATED', 'P5a failed'
    invalid_glare=Calibration(60.,.2,True,True,True,True,True,False,True)
    assert certify(sample,invalid_glare).decision=='ABSTAIN_UNCALIBRATED', 'P5b failed'
    assert total_wrong==0, 'P6 failed'
    return {'experiment':'E002-399','evidence_tier':'synthetic physical-aperture instrument only',
            'seed':seed,'trials_per_cohort':n,'total_wrong_certificates':total_wrong,
            'frozen_predictions_passed':7,'human_annotations':0,
            'product':'ABSTAIN_UNCALIBRATED','cohorts':outputs}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',default='')
    args=p.parse_args()
    report=simulate()
    out=json.dumps(report,indent=2,sort_keys=True)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(out+'\n')
    print(out)


if __name__=='__main__':
    main()
