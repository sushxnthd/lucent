#!/usr/bin/env python3
"""Independent temporal-kernel quadrature and fail-closed bridge oracle for E002-403."""
from __future__ import annotations
import json
import random
from e002_403_shutter_kernel import experiment
from e002_399_annotation_bridge import analyze


def independent_pulse_oracle(seed=4037, n=100):
    rng=random.Random(seed)
    max_error=0.
    for i in range(n):
        v=rng.uniform(10,40)
        e=rng.uniform(.005,.02)
        width=e*rng.uniform(.01,.03)
        minimum=.2-.06*v*e
        # Two independent pulse integrals via midpoint quadrature. We do not
        # reuse the analytic mean routine in the experiment.
        left_start=-e/2
        right_start=1.5*e-width
        nsteps=2001
        def physical(t):
            return minimum+v*abs(t-e/2)
        left=sum(physical(left_start+(j+.5)*width/nsteps)
                 for j in range(nsteps))/nsteps
        right=sum(physical(right_start+(j+.5)*width/nsteps)
                  for j in range(nsteps))/nsteps
        analytic=minimum+v*(e-width/2)
        max_error=max(max_error,abs(left-analytic),abs(right-analytic))
        assert abs(left-analytic)<1e-11 and abs(right-analytic)<1e-11
        # The independent geometric moment is e/2-width/2.
        moment=sum(abs(left_start+(j+.5)*width/nsteps)
                   for j in range(nsteps))/nsteps
        assert abs(moment-(e/2-width/2))<1e-11
        # A directly computed lower-envelope minimum on the center interval.
        naive_lower=analytic-v*e/4
        moment_lower=analytic-v*moment
        naive_min=min(max(naive_lower-v*abs(t),
                          naive_lower-v*abs(t-e))
                      for t in (0.,e/2,e))
        aware_min=min(max(moment_lower-v*abs(t),
                          moment_lower-v*abs(t-e))
                      for t in (0.,e/2,e))
        assert naive_min>.2 and aware_min<=.2+1e-11
    return max_error


def bridge_regression():
    clip='e'*20
    manifest={'experiment':'E002-398','clips':[{'clip_id':clip,'frames':[
        {'frame_in_clip':i} for i in range(7)]}]}
    def row(i,who):
        return {'clip_id':clip,'frame_in_clip':str(i),'rater_id':who,
                'center_upper_x':'50','center_upper_y':'30',
                'center_lower_x':'50','center_lower_y':'65.4'}
    a={(clip,str(i)):row(i,'A') for i in range(7)}
    b={(clip,str(i)):row(i,'B') for i in range(7)}
    timing={(clip,str(i)):{'nominal_time_s':str(i/240),
                           'exposure_s':'.001','clock_error_s':'0'}
            for i in range(7)}
    gates={k:True for k in ('independent_velocity','aperture_geometry',
          'optical_response','exposure_timing','clock_synchronization',
          'nuisance_resolved','uniform_shutter_verified')}
    cfg={'speed_upper':60.,'threshold':.2,'iris_scale_lower_px':100.,
         'iris_scale_upper_px':100.,'landmark_error_px':0.,
         'optical_mean_error_bound':0.,
         'optical_mean_error_provenance':'synthetic_exact_optical_mean',
         'row_timing_calibration':{
             'upper_offset_abs_s_upper':0.,'lower_offset_abs_s_upper':0.,
             'upper_landmark_speed_upper_per_s':0.,
             'lower_landmark_speed_upper_per_s':0.,
             'equal_row_exposure_verified':True,
             'provenance':'synthetic_exact_global_shutter'},
         'landmark_geometry_calibration':{
             'reference_column_px':50.,'upper_lid_slope_bound':0.,
             'lower_lid_slope_bound':0.,'vertical_axis_verified':True,
             'provenance':'synthetic_exact_vertical_geometry'},
         'gates':gates}
    assert analyze(manifest,a,b,timing,cfg)['decisions']['ABSTAIN_UNCALIBRATED']==1
    # E002-405: synthetic oracle supplies a known physical speed envelope;
    # observed human sample maxima are explicitly not accepted as hard bounds.
    cfg['velocity_bound_calibration']={
        'bound_kind':'deterministic_physical_upper',
        'upper_per_s':cfg['speed_upper'],
        'validity_domain':'synthetic_exact_aperture_trajectory_only',
        'provenance':'synthetic_oracle_hard_velocity_upper'}
    cfg['temporal_kernel_calibration']={
        'first_absolute_moment_fraction_upper':.25,
        'provenance':'synthetic_verified_uniform_kernel'}
    clean=analyze(manifest,a,b,timing,cfg)
    assert clean['decisions']['CONFIRMED_NO_CROSSING']==1, clean
    cfg['temporal_kernel_calibration']['first_absolute_moment_fraction_upper']=.5
    widened=analyze(manifest,a,b,timing,cfg)
    assert widened['decisions']['UNRESOLVED']==1, widened
    cfg['temporal_kernel_calibration']['first_absolute_moment_fraction_upper']=-.1
    try: analyze(manifest,a,b,timing,cfg)
    except ValueError: pass
    else: raise AssertionError('negative moment bound accepted')
    cfg['temporal_kernel_calibration']['first_absolute_moment_fraction_upper']=.25
    cfg['temporal_kernel_calibration'].pop('provenance')
    try: analyze(manifest,a,b,timing,cfg)
    except ValueError: pass
    else: raise AssertionError('missing provenance accepted')
    return {'missing_kernel_abstained':True,'clean_uniform_certified':True,
            'wider_moment_forces_unresolved':True,
            'invalid_or_unattributed_kernel_rejected':True}


if __name__=='__main__':
    print(json.dumps({'experiment':'E002-403',
        'independent_numeric_pulse_cases':100,
        'max_quadrature_difference':independent_pulse_oracle(),
        'bridge':bridge_regression(),
        'instrument':experiment(),
        'human_validated':False},indent=2,sort_keys=True))
