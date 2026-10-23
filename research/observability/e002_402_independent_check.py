#!/usr/bin/env python3
"""Independent geometric oracle and end-to-end fail-closed bridge regression.

Uses exact contour equations and independent perturbations; does not call the
E002-402 interval routine for its oracle calculations.
"""
import json
import random
from e002_399_annotation_bridge import analyze
from e002_402_geometry import experiment


def independent_contour_oracle(n=300,seed=4026):
    rng=random.Random(seed)
    for i in range(n):
        xref=rng.uniform(55,85)
        yu_ref=rng.uniform(25,45)
        gap_ref=rng.uniform(1,20)
        yl_ref=yu_ref+gap_ref
        su=rng.uniform(-.3,.3)
        sl=rng.uniform(-.3,.3)
        xu=rng.uniform(45,95)
        xl=rng.uniform(45,95)
        E=rng.uniform(0,1)
        # Sample true contours at unknown perturbed coordinates.
        dxu=rng.uniform(-E,E)
        dxl=rng.uniform(-E,E)
        dyu=rng.uniform(-E,E)
        dyl=rng.uniform(-E,E)
        reported_upper=yu_ref+su*((xu+dxu)-xref)+dyu
        reported_lower=yl_ref+sl*((xl+dxl)-xref)+dyl
        observed=reported_lower-reported_upper
        bound=(.3*abs(xref-xu)+.3*abs(xref-xl)+E*2.6)
        assert observed-bound-1e-12<=gap_ref<=observed+bound+1e-12, i
    return n


def bridge_regression():
    clip='d'*20
    manifest={'experiment':'E002-398','clips':[{'clip_id':clip,'frames':[
        {'frame_in_clip':i} for i in range(7)]}]}
    def row(i,who,xu,yu,xl,yl):
        return {'clip_id':clip,'frame_in_clip':str(i),'rater_id':who,
                'center_upper_x':str(xu),'center_upper_y':str(yu),
                'center_lower_x':str(xl),'center_lower_y':str(yl)}
    timing={(clip,str(i)):{'nominal_time_s':str(i/240),
        'exposure_s':'.001','clock_error_s':'0'} for i in range(7)}
    gates={k:True for k in ('independent_velocity','aperture_geometry',
        'optical_response','exposure_timing','clock_synchronization',
        'nuisance_resolved','uniform_shutter_verified')}
    cfg={'speed_upper':0.,'threshold':.2,'iris_scale_lower_px':50.,
         'iris_scale_upper_px':50.,'landmark_error_px':0.,
         'optical_mean_error_bound':0.,
         'optical_mean_error_provenance':'synthetic_exact_optical_mean',
         'row_timing_calibration':{
            'upper_offset_abs_s_upper':0.,'lower_offset_abs_s_upper':0.,
            'upper_landmark_speed_upper_per_s':0.,
            'lower_landmark_speed_upper_per_s':0.,
            'equal_row_exposure_verified':True,
            'provenance':'synthetic_zero_row_skew'},
         'gates':gates}
    def sheets(xu,yu,xl,yl):
        return ({(clip,str(i)):row(i,'A',xu,yu,xl,yl) for i in range(7)},
                {(clip,str(i)):row(i,'B',xu,yu,xl,yl) for i in range(7)})
    s1,s2=sheets(60,40,80,40)
    missing=analyze(manifest,s1,s2,timing,cfg)
    assert missing['decisions']['ABSTAIN_UNCALIBRATED']==1, ('G4',missing)
    cfg['landmark_geometry_calibration']={
        'reference_column_px':70.,'upper_lid_slope_bound':0.,
        'lower_lid_slope_bound':0.,'vertical_axis_verified':True,
        'provenance':'synthetic_parallel_contours_at_x70'}
    zero_gap=analyze(manifest,s1,s2,timing,cfg)
    assert zero_gap['decisions']['CONFIRMED_CROSSING']==1, ('G4',zero_gap)
    s1,s2=sheets(50,30,50,50)
    cfg['landmark_geometry_calibration']['reference_column_px']=50.
    open_eye=analyze(manifest,s1,s2,timing,cfg)
    assert open_eye['decisions']['CONFIRMED_NO_CROSSING']==1, ('G4',open_eye)
    cfg['landmark_geometry_calibration']['upper_lid_slope_bound']=.8
    cfg['landmark_geometry_calibration']['lower_lid_slope_bound']=.8
    s1,s2=sheets(60,30,80,50)
    uncertain=analyze(manifest,s1,s2,timing,cfg)
    assert uncertain['decisions']['UNRESOLVED']==1, ('G5',uncertain)
    s1,s2=sheets(50,50,50,49)
    invalid=analyze(manifest,s1,s2,timing,cfg)
    assert invalid['excluded_frames']==7
    assert invalid['decisions']['CONFIRMED_NO_CROSSING']==0
    cfg['landmark_geometry_calibration'].pop('provenance')
    try: analyze(manifest,s1,s2,timing,cfg)
    except ValueError: pass
    else: raise AssertionError('G4 provenance omission was accepted')
    return {'missing_geometry_abstains':True,
            'diagonal_zero_gap_not_falsely_certified_open':True,
            'clean_vertical_gap_certified':True,
            'increased_slope_forces_unresolved':True,
            'inverted_gap_frames_excluded':True,
            'missing_provenance_rejected':True}


if __name__=='__main__':
    result=experiment()
    assert result['max_interval_violation']==0
    print(json.dumps({'experiment':'E002-402','independent_oracle_cases':
                      independent_contour_oracle(),
                      'bridge':bridge_regression(),
                      'synthetic_trials':result['trials'],
                      'human_validation':False},indent=2,sort_keys=True))
