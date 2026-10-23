#!/usr/bin/env python3
"""Independent E002-401 shutter quadrature and fail-closed bridge regression.

The oracle evaluates each moving eyelid row separately; it does not reuse the
analytical mean routine to calculate the reference observation.
"""
from __future__ import annotations
import json
import random
from e002_399_annotation_bridge import analyze
from e002_401_rolling_shutter import experiment, upper, lower, row_measurement


def quadrature(fn, center, offset, aperture, velocity, exposure=.001, n=2048):
    start = center + offset - exposure / 2
    return sum(fn(start + (k+.5)*exposure/n, aperture, velocity)
               for k in range(n)) / n


def independent_oracle():
    rng = random.Random(40101)
    worst = 0.
    for i in range(100):
        aperture = rng.choice((.19,.30))
        velocity = rng.uniform(-20.,20.)
        center = rng.uniform(-.0015,.0015)
        du = -.004 + rng.uniform(-.00025,.00025)
        dl = .004 + rng.uniform(-.00025,.00025)
        # Independently verify that the physical eyelid coordinates are valid
        # across the entire acquisition support.
        for t in (center+du-.0005,center+du+.0005,
                  center+dl-.0005,center+dl+.0005):
            assert 0 < upper(t,aperture,velocity) < 1
            assert 0 < lower(t,aperture,velocity) < 1
        numeric = (quadrature(lower,center,dl,aperture,velocity)
                   - quadrature(upper,center,du,aperture,velocity))
        analytic = row_measurement(center,aperture,velocity,du,dl)
        worst = max(worst,abs(numeric-analytic))
        assert abs(numeric-analytic)<1e-9, ('W6',i,numeric,analytic)
        # Separate, independent geometric triangle-inequality bound.
        assert abs(numeric-aperture) <= 20.*(abs(du)+abs(dl))+1e-9
    return worst


def bridge_checks():
    clip = 'c'*20
    manifest={'experiment':'E002-398','clips':[{'clip_id':clip,'frames':[
        {'frame_in_clip':i} for i in range(7)]}]}
    def row(i,who):
        return {'clip_id':clip,'frame_in_clip':str(i),'rater_id':who,
                'center_upper_x':'50','center_upper_y':'30',
                'center_lower_x':'50','center_lower_y':'70'}
    s1={(clip,str(i)):row(i,'rater-A') for i in range(7)}
    s2={(clip,str(i)):row(i,'rater-B') for i in range(7)}
    timing={(clip,str(i)):{'nominal_time_s':str(i/240),
                           'exposure_s':'.001','clock_error_s':'.0001'}
            for i in range(7)}
    gates={k:True for k in ('independent_velocity','aperture_geometry',
        'optical_response','exposure_timing','clock_synchronization',
        'nuisance_resolved','uniform_shutter_verified')}
    cfg={'speed_upper':60.,'threshold':.2,'iris_scale_lower_px':100.,
         'iris_scale_upper_px':100.,'landmark_error_px':1.,
         'optical_mean_error_bound':0.,
         'optical_mean_error_provenance':'synthetic_exact_mean_oracle',
         'gates':gates}
    assert analyze(manifest,s1,s2,timing,cfg)['decisions']['ABSTAIN_UNCALIBRATED']==1, 'W7 missing'
    cfg['row_timing_calibration']={
        'upper_offset_abs_s_upper':0.,'lower_offset_abs_s_upper':0.,
        'upper_landmark_speed_upper_per_s':20.,
        'lower_landmark_speed_upper_per_s':20.,
        'equal_row_exposure_verified':True,
        'provenance':'synthetic_verified_zero_row_skew'}
    clean=analyze(manifest,s1,s2,timing,cfg)
    assert clean['decisions']['CONFIRMED_NO_CROSSING']==1, ('W7 zero',clean)
    cfg['gates']['uniform_shutter_verified']=False
    cfg['gates']['calibrated_row_shutter']=True
    cfg['row_timing_calibration']['upper_offset_abs_s_upper']=.004
    cfg['row_timing_calibration']['lower_offset_abs_s_upper']=.004
    wide=analyze(manifest,s1,s2,timing,cfg)
    assert wide['decisions']['UNRESOLVED']==1, ('W7 rolling',wide)
    assert abs(wide['row_skew_error_bound_applied']-.16)<1e-12
    cfg['row_timing_calibration']['upper_offset_abs_s_upper']=.01
    wider=analyze(manifest,s1,s2,timing,cfg)
    assert wider['decisions']['UNRESOLVED']==1, ('W7 monotonic',wider)
    cfg['row_timing_calibration'].pop('provenance')
    try: analyze(manifest,s1,s2,timing,cfg)
    except ValueError: pass
    else: raise AssertionError('W7 provenance missing but accepted')
    return {'missing_row_abstained':True,'zero_skew_certified':True,
            'calibrated_rolling_abstained':True,
            'increased_skew_abstained':True,'missing_provenance_rejected':True}


if __name__ == '__main__':
    result=experiment()
    oracle=independent_oracle()
    bridge=bridge_checks()
    print(json.dumps({'experiment':'E002-401','independent_quadrature_cases':100,
                      'max_analytic_numeric_difference':oracle,
                      'naive_wrong':result['naive_wrong_certificates'],
                      'corrected_wrong':result['corrected_wrong_certificates'],
                      'bridge':bridge,
                      'human_validated':False},indent=2,sort_keys=True))
