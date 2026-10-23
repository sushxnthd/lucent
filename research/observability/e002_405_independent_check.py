#!/usr/bin/env python3
"""E002-405 independent rank oracle, physical witness and bridge enforcement.

Separate combinatorial enumeration and analytical envelope; no human claims.
"""
from __future__ import annotations
import itertools
import json
import math
from pathlib import Path

from e002_399_annotation_bridge import analyze, hard_velocity_evidence


def rank_oracle():
    cases=[]
    for n,m in ((4,2),(5,3),(7,1)):
        positions=range(n+m)
        subsets=list(itertools.combinations(positions,n))
        future_exceeds=sum((n+m-1) not in s for s in subsets)
        empirical=future_exceeds/len(subsets)
        expected=m/(n+m)
        assert abs(empirical-expected)<1e-14
        cases.append({'n':n,'m':m,'enumerated_subsets':len(subsets),
                      'exceedance_probability':empirical})
    return cases


def witness_oracle(w):
    e=w['exposure_s']
    assert abs(w['true_minimum']-.18)<1e-12
    assert abs(w['means'][0]-.30)<1e-12
    assert abs(w['means'][1]-.30)<1e-12
    gap=w['times_s'][1]-w['times_s'][0]
    for speed,key in ((4.,'incorrect_empirical_certificate'),
                      (6.,'correct_hard_speed_certificate')):
        # Independent two-cone intersection, including uniform shutter moment.
        analytical_min=.30-speed*(gap/2+e/4)
        reported=w[key]['lower_min']
        assert abs(analytical_min-reported)<1e-10, (speed,analytical_min,reported)
        expected='CONFIRMED_NO_CROSSING' if speed==4 else 'UNRESOLVED'
        assert w[key]['decision']==expected
    assert w['true_minimum']<w['threshold']
    return True


def bridge_oracle():
    clip='e'*20
    manifest={'experiment':'E002-398','clips':[{'clip_id':clip,
        'frames':[{'frame_in_clip':i} for i in range(7)]}]}
    def rows(who):
        return {(clip,str(i)):{
            'rater_id':who,'center_upper_x':'50','center_upper_y':'30',
            'center_lower_x':'50','center_lower_y':'80'}
            for i in range(7)}
    timing={(clip,str(i)):{'nominal_time_s':str(i/240),
        'exposure_s':'0.001','clock_error_s':'0'} for i in range(7)}
    cfg={'speed_upper':6.,'threshold':.2,
        'iris_scale_lower_px':100.,'iris_scale_upper_px':100.,
        'landmark_error_px':0.,
        'optical_mean_error_bound':0.,
        'optical_mean_error_provenance':'synthetic_exact_mean_oracle',
        'row_timing_calibration':{
            'upper_offset_abs_s_upper':0.,
            'lower_offset_abs_s_upper':0.,
            'upper_landmark_speed_upper_per_s':0.,
            'lower_landmark_speed_upper_per_s':0.,
            'equal_row_exposure_verified':True,
            'provenance':'synthetic_exact_global_shutter'},
        'landmark_geometry_calibration':{
            'reference_column_px':50.,'upper_lid_slope_bound':0.,
            'lower_lid_slope_bound':0.,'vertical_axis_verified':True,
            'provenance':'synthetic_exact_vertical_geometry'},
        'temporal_kernel_calibration':{
            'first_absolute_moment_fraction_upper':.25,
            'provenance':'synthetic_uniform_kernel'},
        'gates':{k:True for k in (
            'independent_velocity','aperture_geometry','optical_response',
            'exposure_timing','clock_synchronization','nuisance_resolved',
            'uniform_shutter_verified')}}
    a,b=rows('A'),rows('B')
    def decision():
        return analyze(manifest,a,b,timing,cfg)['decisions']
    assert decision()['ABSTAIN_UNCALIBRATED']==1
    for kind in ('sample_maximum','empirical_quantile',
                 'conformal_marginal','unknown_type'):
        cfg['velocity_bound_calibration']={
            'bound_kind':kind,'upper_per_s':6.,
            'validity_domain':'synthetic_test_domain',
            'provenance':'synthetic_oracle_not_a_hard_bound'}
        assert not hard_velocity_evidence(cfg)
        assert decision()['ABSTAIN_UNCALIBRATED']==1,kind
    cfg['velocity_bound_calibration']['bound_kind']='deterministic_physical_upper'
    cfg['velocity_bound_calibration']['provenance']='synthetic_exact_hard_speed'
    assert hard_velocity_evidence(cfg)
    assert decision()['CONFIRMED_NO_CROSSING']==1
    cfg['velocity_bound_calibration']['upper_per_s']=4.
    assert not hard_velocity_evidence(cfg)
    assert decision()['ABSTAIN_UNCALIBRATED']==1
    cfg['velocity_bound_calibration']['upper_per_s']=6.
    cfg['velocity_bound_calibration']['validity_domain']=''
    assert not hard_velocity_evidence(cfg)
    assert decision()['ABSTAIN_UNCALIBRATED']==1
    cfg['velocity_bound_calibration']['validity_domain']='synthetic_test_domain'
    cfg['gates']['independent_velocity']=False
    assert decision()['ABSTAIN_UNCALIBRATED']==1
    return {'missing_abstains':True,'empirical_kinds_abstain':4,
            'explicit_synthetic_hard_bound_certifies':True,
            'mismatched_bound_abstains':True,
            'invalid_domain_abstains':True,
            'legacy_boolean_alone_rejected':True}


def main():
    path=Path(__file__).with_name('e002_405_results.json')
    data=json.loads(path.read_text())
    assert data['experiment']=='E002-405'
    assert len(data['rank_experiments'])==6
    assert all(r['absolute_error']<.03 for r in data['rank_experiments'])
    assert witness_oracle(data['physical_witness'])
    print(json.dumps({'experiment':'E002-405','independent_rank_enumeration':rank_oracle(),
                      'independent_witness_oracle':True,'bridge':bridge_oracle(),
                      'human_validation':False},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
