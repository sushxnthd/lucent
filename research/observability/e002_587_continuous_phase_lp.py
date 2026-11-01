#!/usr/bin/env python3
"""E002-587: continuous affine-shutter outer supports (synthetic only)."""
import argparse
import json
import math
from scipy.optimize import linprog

REQUIRED = ('photodiode_edge_timed', 'linear_response_verified',
            'unclipped_pixels', 'row_geometry_verified',
            'rolling_mode_fixed', 'gain_and_dark_calibrated',
            'led_transition_bounded', 'same_imaging_path')
PARAM_BOUNDS = ((0., 4.), (2., 6.), (0., .2))


def brightness(s, e, p):
    return min(1., max(0., (s + e - p) / e))


def synth(s=2., e=4., d=.1, rows=(0, 20, 40), phases=None, row_offset=None):
    phases = [i / 2 for i in range(25)] if phases is None else phases
    return [{'row': r, 'phase_ms': p,
             'intensity': brightness(s + r*d + (row_offset or {}).get(r, 0.), e, p)}
            for r in rows for p in phases]


def model(obs, controls, delta=0., epsilon=0.):
    if not isinstance(controls, dict) or not all(controls.get(k) is True for k in REQUIRED):
        raise ValueError('UNCALIBRATED_OPTICAL_OR_GEOMETRY_CONTROL')
    if not all(type(v) in (int, float) and math.isfinite(v) and v >= 0
               for v in (delta, epsilon)) or epsilon > 1:
        raise ValueError('BAD_UNCERTAINTY')
    if not isinstance(obs, list) or not obs:
        raise ValueError('MISSING_PHASE_DATA')
    groups, seen = {}, set()
    A, b = [], []
    for x in obs:
        if not isinstance(x, dict):
            raise ValueError('BAD_OBSERVATION')
        r, p, y = (x.get(k) for k in ('row', 'phase_ms', 'intensity'))
        if type(r) is not int or not 0 <= r <= 10000 or any(
                type(v) not in (int, float) or not math.isfinite(v)
                for v in (p, y)) or not 0 <= y <= 1:
            raise ValueError('BAD_OBSERVATION')
        if (r, p) in seen:
            raise ValueError('DUPLICATE_PHASE')
        seen.add((r, p))
        groups.setdefault(r, []).append(y)
        lo, hi = max(0., y-epsilon), min(1., y+epsilon)
        if lo > 0:
            A.append([-1., -(1.-lo), -float(r)])
            b.append(-p+delta)
        if hi < 1:
            A.append([1., (1.-hi), float(r)])
            b.append(p+delta)
    if len(groups) < 3:
        raise ValueError('INSUFFICIENT_ROW_GEOMETRY')
    for ys in groups.values():
        if len(ys) < 6 or not any(.2 < y < .8 for y in ys) or not (
                any(y <= .05 for y in ys) and any(y >= .95 for y in ys)):
            raise ValueError('UNIDENTIFIABLE_PHASE_SWEEP')
    for j, (low, high) in enumerate(PARAM_BOUNDS):
        up = [0.]*3
        up[j] = 1.
        A.append(up)
        b.append(high)
        dn = [0.]*3
        dn[j] = -1.
        A.append(dn)
        b.append(-low)
    return A, b, sorted(groups)


def optimize(A, b, c):
    result = linprog(c, A_ub=A, b_ub=b, bounds=[(None, None)]*3,
                     method='highs', options={'primal_feasibility_tolerance': 1e-9,
                                               'dual_feasibility_tolerance': 1e-9})
    if not result.success:
        raise ValueError('MODEL_FALSIFIED_OR_NUMERICAL_FAILURE:' + str(result.message))
    x, dual = result.x.tolist(), result.ineqlin.marginals.tolist()
    max_violation = max(sum(a*t for a,t in zip(row,x))-rhs for row,rhs in zip(A,b))
    stationarity = max(abs(sum(row[j]*m for row,m in zip(A,dual))-c[j]) for j in range(3))
    gap = abs(sum(v*m for v,m in zip(b,dual))-sum(t*v for t,v in zip(x,c)))
    if max_violation > 1e-7 or stationarity > 1e-7 or gap > 1e-7 or max(dual)>1e-7:
        raise AssertionError('PRIMAL_DUAL_CERTIFICATE_FAILURE')
    return {'primal':x,'dual':dual,'objective':sum(t*v for t,v in zip(x,c)),
            'primal_max_violation':max_violation,
            'dual_stationarity_max':stationarity,'duality_gap':gap}


def analyze(obs, controls, delta=0., epsilon=0.):
    A,b,rows=model(obs,controls,delta,epsilon)
    opt={}
    bounds={}
    for r in rows:
        left=optimize(A,b,[1.,0.,float(r)])
        right=optimize(A,b,[-1.,-1.,-float(r)])
        bounds[str(r)]=[left['objective'],-right['objective']]
        opt[str(r)]={'min_start':left,'max_end_negated':right}
    return {'experiment':'E002-587','evidence_tier':'CONTINUOUS_LP_SYNTHETIC_MODEL',
            'delta_ms':delta,'epsilon':epsilon,'observations':len(obs),
            'rows':rows,'outer_exposure_support_ms_by_row':bounds,
            'constraint_count':len(A),'A':A,'b':b,'certificates':opt,
            'physical_certificate':False,'human_data':False,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


def finite_grid_count(obs,delta=0.,epsilon=0.):
    count=0
    for si in range(9):
        for ei in range(4,13):
            for di in range(5):
                s,e,d=si/2,ei/2,di/20
                if all(brightness(s+x['row']*d,e,x['phase_ms']+delta)<=x['intensity']+epsilon+1e-10
                       and brightness(s+x['row']*d,e,x['phase_ms']-delta)>=x['intensity']-epsilon-1e-10
                       for x in obs):
                    count+=1
    return count


def check_reject(fn, prefix):
    try:
        fn()
    except ValueError as ex:
        assert str(ex).startswith(prefix), (prefix, str(ex))
    else:
        raise AssertionError('EXPECTED_REJECTION:'+prefix)


def self_test():
    controls={k:True for k in REQUIRED}
    obs=synth()
    exact=analyze(obs,controls)
    relaxed=analyze(obs,controls,.5,.1)
    for r,(s,e) in {'0':(2,6),'20':(4,8),'40':(6,10)}.items():
        assert max(abs(exact['outer_exposure_support_ms_by_row'][r][i]-v)
                   for i,v in enumerate((s,e))) < 1e-6
        assert relaxed['outer_exposure_support_ms_by_row'][r][0] <= s+1e-7
        assert relaxed['outer_exposure_support_ms_by_row'][r][1] >= e-1e-7
    wider=analyze(obs,controls,.75,.15)
    for r in exact['outer_exposure_support_ms_by_row']:
        assert wider['outer_exposure_support_ms_by_row'][r][0] <= relaxed['outer_exposure_support_ms_by_row'][r][0]+1e-7
        assert wider['outer_exposure_support_ms_by_row'][r][1] >= relaxed['outer_exposure_support_ms_by_row'][r][1]-1e-7
    assert finite_grid_count(obs)==1
    assert finite_grid_count(obs,.5,.1)==14
    off=synth(s=2.17)
    off_exact=analyze(off,controls)
    assert finite_grid_count(off)==0
    for r in off_exact['outer_exposure_support_ms_by_row']:
        expected=(2.17+int(r)*.1,6.17+int(r)*.1)
        assert max(abs(off_exact['outer_exposure_support_ms_by_row'][r][i]-v) for i,v in enumerate(expected)) < 1e-6
    check_reject(lambda:analyze(synth(phases=[0,.5,1,11,11.5,12]),controls),'UNIDENTIFIABLE_PHASE_SWEEP')
    check_reject(lambda:analyze(synth(rows=(0,20)),controls),'INSUFFICIENT_ROW_GEOMETRY')
    check_reject(lambda:analyze(synth(row_offset={40:1.}),controls),'MODEL_FALSIFIED_OR_NUMERICAL_FAILURE')
    bad=[dict(x) for x in obs]
    bad[0]['intensity']=.4
    check_reject(lambda:analyze(bad,controls),'MODEL_FALSIFIED_OR_NUMERICAL_FAILURE')
    for k in REQUIRED:
        cc=dict(controls);cc[k]=False
        check_reject(lambda cc=cc:analyze(obs,cc),'UNCALIBRATED_OPTICAL_OR_GEOMETRY_CONTROL')
    assert not exact['physical_certificate']
    return {'synthetic_tests_passed':17,'exact_support':exact['outer_exposure_support_ms_by_row'],
            'relaxed_support':relaxed['outer_exposure_support_ms_by_row'],
            'wider_support':wider['outer_exposure_support_ms_by_row'],
            'off_grid_support':off_exact['outer_exposure_support_ms_by_row'],
            'finite_grid_count_exact':1,'finite_grid_count_relaxed':14,
            'finite_grid_count_off_grid':0,'continuous_feasible_off_grid':True,
            'evidence_tier':'CONTINUOUS_LP_SYNTHETIC_MODEL',
            'physical_certificate':False,'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--self-test',action='store_true')
    p.add_argument('--certificates',action='store_true')
    args=p.parse_args()
    if args.self_test:
        print(json.dumps(self_test(),sort_keys=True))
    elif args.certificates:
        controls={k:True for k in REQUIRED}
        print(json.dumps({'exact':analyze(synth(),controls),
                          'relaxed':analyze(synth(),controls,.5,.1),
                          'off_grid':analyze(synth(s=2.17),controls)},sort_keys=True))
    else:
        p.error('provide --self-test or --certificates')


if __name__=='__main__':
    main()
