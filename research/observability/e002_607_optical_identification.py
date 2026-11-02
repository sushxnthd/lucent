#!/usr/bin/env python3
"""E002-607: conservative finite-grid LED shutter calibration, not a human result.

Input is a PRIVATE, externally authenticated linear-light instrument JSON.
No software flag alone authenticates optical timing or sensor radiometry.
"""
import argparse
from fractions import Fraction
import json
import random

OFFSETS = range(9)
EXPOSURES = range(2, 9)
ROW_DELAYS = range(5)
FRAMES = [0, 20, 40, 60, 80]
ROWS = [0, 1, 2]
TRUE = (3, 4, 2)


def avg(code, start, exposure):
    if (isinstance(start, bool) or not isinstance(start, int) or
        isinstance(exposure, bool) or not isinstance(exposure, int) or
        start < 0 or exposure <= 0 or start + exposure > len(code)):
        raise ValueError('uncovered exposure interval')
    return Fraction(sum(code[start:start+exposure]), exposure)


def prediction(code, frame, row, candidate):
    offset, exposure, row_delay = candidate
    return avg(code, frame + offset + row * row_delay, exposure)


def identify(code, samples, tolerance, offsets=OFFSETS, exposures=EXPOSURES, delays=ROW_DELAYS):
    if not samples or tolerance < 0:
        raise ValueError('empty samples or invalid tolerance')
    if any(v not in (0, 1) or type(v) is not int for v in code):
        raise ValueError('nonbinary LED trace')
    found = []
    for candidate in ((o, e, d) for o in offsets for e in exposures for d in delays):
        if all(abs(prediction(code, f, r, candidate)-v) <= tolerance for f, r, v in samples):
            found.append(candidate)
    return found


def fixture(code, candidate=TRUE, frames=FRAMES):
    return [(f, r, prediction(code, f, r, candidate)) for f in frames for r in ROWS]


def code607():
    rng = random.Random(607)
    return [rng.randrange(2) for _ in range(120)]


def run_synthetic():
    code = code607()
    samples = fixture(code)
    fit = [s for s in samples if s[0] in FRAMES[:3]]
    holdout = [s for s in samples if s[0] in FRAMES[3:]]
    strict = identify(code, fit, Fraction(1,100))
    loose = identify(code, fit, Fraction(1,10))
    assert set(strict).issubset(set(loose))
    constant = identify([1]*120, fixture([1]*120)[:9], Fraction(1,100))
    assert len(constant) == 315
    assert TRUE in strict
    assert all(all(abs(prediction(code,f,r,c)-v) <= Fraction(1,100)
                   for f,r,v in holdout) for c in strict)
    shifted_candidates = identify(code, fit, Fraction(1,100))
    assert shifted_candidates == strict
    dropped = identify(code, fit[:-1], Fraction(1,100))
    assert set(strict).issubset(set(dropped))
    return {'experiment':'E002-607','tier':'SYNTHETIC_LED_INSTRUMENT_ONLY',
            'fit_samples':len(fit),'holdout_samples':len(holdout),
            'candidate_space':315,'strict_candidates':len(strict),
            'strict_candidate_values':strict[:20],
            'loose_candidates':len(loose),
            'constant_led_candidates':len(constant),
            'dropped_sample_candidates':len(dropped),
            'true_candidate_retained':TRUE in strict,
            'holdout_all_consistent':True,
            'human_measurements':0,'physical_camera_measurements':0,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


def parse_fraction(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError('invalid numeric value')
    q = Fraction(str(value))
    if not 0 <= q <= 1:
        raise ValueError('intensity outside linear range')
    return q


def evaluate_private(data):
    if not isinstance(data, dict) or data.get('experiment') != 'E002-607':
        raise ValueError('wrong instrument schema')
    if any(data.get(k) is not True for k in ('external_led_clock_verified',
              'linear_light_response_verified','exposure_geometry_verified',
              'photodiode_sync_verified','no_clipped_pixels')):
        return {'status':'ABSTAIN_UNVERIFIED_INSTRUMENT',
                'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}
    code = data.get('led_bits')
    rows = data.get('samples')
    if not isinstance(code,list) or len(code)<110 or not isinstance(rows,list) or not rows:
        raise ValueError('incomplete waveform or samples')
    parsed = []
    for row in rows:
        if not isinstance(row,dict) or set(row) != {'frame_ms','row','intensity'}:
            raise ValueError('invalid row')
        f,r = row['frame_ms'],row['row']
        if type(f) is not int or type(r) is not int or f not in FRAMES or r not in ROWS:
            raise ValueError('unexpected frame/row')
        parsed.append((f,r,parse_fraction(row['intensity'])))
    if len(set((f,r) for f,r,_ in parsed)) != len(parsed):
        raise ValueError('duplicate measurement')
    if len(parsed)!=15:
        return {'status':'ABSTAIN_MISSING_MEASUREMENTS',
                'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}
    tol = parse_fraction(data.get('intensity_error_bound'))
    fit=[s for s in parsed if s[0] in FRAMES[:3]]
    hold=[s for s in parsed if s[0] in FRAMES[3:]]
    candidates=identify(code,fit,tol)
    surviving=[c for c in candidates if all(abs(prediction(code,f,r,c)-v)<=tol for f,r,v in hold)]
    status=('ABSTAIN_INCONSISTENT' if not surviving else
            'ABSTAIN_NONIDENTIFIABLE' if len(surviving)!=1 else
            'GRID_IDENTIFIED_CONDITIONAL_ONLY')
    return {'status':status,'fitted_candidates':len(candidates),
            'heldout_candidates':len(surviving),
            'grid_solution':list(surviving[0]) if len(surviving)==1 else None,
            'warning':'software cannot authenticate supplied optical attestations or clock uncertainties',
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


def self_test():
    result=run_synthetic()
    assert result['true_candidate_retained']
    assert result['constant_led_candidates']==315
    assert evaluate_private({'experiment':'E002-607'})['status']=='ABSTAIN_UNVERIFIED_INSTRUMENT'
    code=code607()
    samples=fixture(code)
    payload={'experiment':'E002-607','external_led_clock_verified':True,
       'linear_light_response_verified':True,'exposure_geometry_verified':True,
       'photodiode_sync_verified':True,'no_clipped_pixels':True,
       'led_bits':code,'intensity_error_bound':'0.01',
       'samples':[{'frame_ms':f,'row':r,'intensity':str(v)} for f,r,v in samples]}
    good=evaluate_private(payload)
    assert good['heldout_candidates']>=1
    bad=dict(payload,linear_light_response_verified=False)
    assert evaluate_private(bad)['status']=='ABSTAIN_UNVERIFIED_INSTRUMENT'
    bad=dict(payload,samples=payload['samples'][:-1])
    assert evaluate_private(bad)['status']=='ABSTAIN_MISSING_MEASUREMENTS'
    bad=dict(payload,samples=payload['samples']+[payload['samples'][0]])
    try: evaluate_private(bad)
    except ValueError: pass
    else: raise AssertionError('duplicate accepted')
    bad=dict(payload,led_bits=[1]*120)
    assert evaluate_private(bad)['status']=='ABSTAIN_INCONSISTENT'
    return result,good


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--private-input',help='JSON local optical instrument input; never upload raw human data')
    args=ap.parse_args()
    if args.private_input:
        try:
            with open(args.private_input,encoding='utf-8') as fh:
                result=evaluate_private(json.load(fh))
        except (ValueError,KeyError,TypeError,OSError) as e:
            result={'status':'ABSTAIN_INVALID_INPUT','error':str(e)[:100],
                    'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}
    elif args.self_test:
        result,private=self_test()
        result['private_fixture_status']=private['status']
    else:
        result=run_synthetic()
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
