#!/usr/bin/env python3
"""E002-610: exact-rational photometric nuisance instrument; synthetic only.

Not a calibrated human aperture measurement. Every status is research-only.
"""
from fractions import Fraction
import argparse
import json
import random
import re
import math
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING

ATTEST = ('raw_linear_light', 'independent_flux_bounds', 'background_gain_calibrated',
          'anatomical_transfer_independently_validated', 'shutter_clock_calibrated')
NUISANCE = ('geometry', 'brightness', 'missingness', 'blur', 'gaze', 'glasses',
            'sampling', 'clock_error', 'occlusion', 'saturation', 'rolling_shutter')
DIGEST = ('sensor_transfer', 'illumination_trace', 'anatomical_transfer', 'shutter_clock')
DEC = re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?\Z')


def q(x):
    if isinstance(x, bool) or not isinstance(x, (str, int, float)) or not DEC.fullmatch(str(x)):
        raise ValueError('finite decimal required')
    return Fraction(str(x))


def result(status, **kwargs):
    return dict(experiment='E002-610', status=status,
                evidence_tier='SYNTHETIC_CONDITIONAL_RADIOMETRIC_MODEL',
                product='ABSTAIN_UNCALIBRATED', release='BLOCKED',
                physical_authentication='NOT_VERIFIED', **kwargs)


def evaluate(d):
    if not isinstance(d, dict) or d.get('experiment') != 'E002-610':
        return result('ABSTAIN_SCHEMA')
    if not isinstance(d.get('attestations'), dict) or any(d['attestations'].get(k) is not True for k in ATTEST):
        return result('ABSTAIN_ATTESTATION')
    if not isinstance(d.get('nuisances'), dict) or any(d['nuisances'].get(k) is not False for k in NUISANCE):
        return result('ABSTAIN_NUISANCE')
    dig = d.get('evidence_sha256')
    if not isinstance(dig, dict) or any(not isinstance(dig.get(k), str) or not re.fullmatch('[0-9a-f]{64}', dig[k]) for k in DIGEST):
        return result('ABSTAIN_DIGEST')
    try:
        y0,y1 = q(d['signal_lower']),q(d['signal_upper'])
        b0,b1 = q(d['background_lower']),q(d['background_upper'])
        g0,g1 = q(d['gain_lower']),q(d['gain_upper'])
        l0,l1 = q(d['flux_lower']),q(d['flux_upper'])
        tau = q(d['threshold'])
    except (KeyError, ValueError, TypeError):
        return result('ABSTAIN_NUMERIC')
    if not (0 <= y0 <= y1 and 0 <= b0 <= b1 and 0 < g0 <= g1 and 0 < l0 <= l1 and 0 <= tau <= 1):
        return result('ABSTAIN_INVALID_BOUNDS')
    if y1 < b0 or y0 > b1 + g1*l1:
        return result('ABSTAIN_INFEASIBLE_MEASUREMENT')
    lower = max(Fraction(0), (y0-b1)/(g1*l1))
    upper = min(Fraction(1), max(Fraction(0), (y1-b0)/(g0*l0)))
    if lower > upper:
        return result('ABSTAIN_INFEASIBLE_MEASUREMENT')
    return result('MEAN_WITNESS_CONDITIONAL' if upper <= tau else 'NO_MEAN_WITNESS',
                  aperture_mean_lower=str(lower), aperture_mean_upper=str(upper),
                  threshold=str(tau), note='No witness never proves absence; physical model not authenticated')


def fixture():
    return dict(experiment='E002-610', signal_lower='0.15', signal_upper='0.15',
                background_lower='0', background_upper='0.01',
                gain_lower='0.98', gain_upper='1.02',
                flux_lower='0.9', flux_upper='1.1', threshold='0.20',
                attestations={k: True for k in ATTEST},
                nuisances={k: False for k in NUISANCE},
                evidence_sha256={k: 'a'*64 for k in DIGEST})


def synthetic_sweep(n=10000, seed=610):
    rng = random.Random(seed)
    stats = {'trials':n,'actual_mean_le_threshold':0,'tight_witness':0,'loose_witness':0,
             'tight_false_witness':0,'loose_false_witness':0,'bound_violations':0}
    for _ in range(n):
        base = rng.uniform(0,0.4)
        phase = rng.uniform(0,2*math.pi)
        apertures = [max(0,min(1,base + .08*math.sin(2*math.pi*(i+.5)/16+phase))) for i in range(16)]
        light = [rng.uniform(.95,1.05) for i in range(16)]
        true_mean = sum(apertures)/16
        y = .02 + sum(a*l for a,l in zip(apertures,light))/16
        d=fixture()
        d.update(signal_lower=format(Decimal.from_float(max(0,y-.002)).quantize(Decimal('0.000000000000001'), rounding=ROUND_FLOOR), 'f'),
                 signal_upper=format(Decimal.from_float(y+.002).quantize(Decimal('0.000000000000001'), rounding=ROUND_CEILING), 'f'),
                 background_lower='0.015',background_upper='0.025',
                 flux_lower='0.95',flux_upper='1.05')
        tight=evaluate(d)
        d['flux_lower']='0.4';d['flux_upper']='1.6'
        loose=evaluate(d)
        if true_mean <= .2: stats['actual_mean_le_threshold']+=1
        for name,out in (('tight',tight),('loose',loose)):
            if out['status'] not in ('MEAN_WITNESS_CONDITIONAL','NO_MEAN_WITNESS'):
                raise AssertionError(out)
            upper=float(Fraction(out['aperture_mean_upper']))
            if true_mean > upper + 1e-12: stats['bound_violations']+=1
            if out['status']=='MEAN_WITNESS_CONDITIONAL':
                stats[name+'_witness']+=1
                if true_mean > .2 + 1e-12: stats[name+'_false_witness']+=1
    return stats


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--sweep',action='store_true')
    p.add_argument('--input')
    args=p.parse_args()
    if args.sweep:
        print(json.dumps(synthetic_sweep(),sort_keys=True));return
    if args.input:
        try:
            with open(args.input,encoding='utf-8') as f: d=json.load(f)
        except (OSError,json.JSONDecodeError):
            print(json.dumps(result('ABSTAIN_INVALID_INPUT'),sort_keys=True));return
    else: d=fixture()
    print(json.dumps(evaluate(d),sort_keys=True))

if __name__=='__main__': main()
