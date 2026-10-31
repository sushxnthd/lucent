#!/usr/bin/env python3
"""E002-454: conditional participant-cluster falsification of E002-453's 0/649.

Uses only the checksum-verified, deidentified E002-453 aggregate. Does not
estimate a hard physiological cap, new human observations, or camera shutter.
"""
import argparse
import json
import math
from pathlib import Path


def zero_failure_upper(n, alpha=0.05):
    """Exact one-sided Clopper-Pearson upper limit for 0 successes in n trials."""
    if type(n) is not int or n <= 0 or not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError('positive integer n and 0 < alpha < 1 required')
    return -math.expm1(math.log(alpha) / n)


def analyze(aggregate):
    if not isinstance(aggregate, dict):
        raise ValueError('expected object')
    r = aggregate['rows']
    n_train, n_hold = r['train_subjects'], r['holdout_subjects']
    n_blinks = r['holdout']
    for n in (n_train, n_hold, n_blinks):
        if type(n) is not int or n <= 0:
            raise ValueError('positive integer sample counts required')
    if r['participants'] != n_train + n_hold or r['valid'] != r['train'] + n_blinks:
        raise ValueError('inconsistent participant or blink counts')
    if not aggregate.get('source', {}).get('sha256_verified'):
        raise ValueError('source integrity unverified')
    t = aggregate['tests']['pooled_train_max']
    if t['denominator'] != n_blinks or t['count'] != 0 or t['holdout_subjects_with_exceedance'] != 0 or t['abstained'] != 0:
        raise ValueError('this frozen analysis requires 0/holdout complete coverage')
    v_train, v_hold = aggregate['train']['max'], aggregate['holdout']['max']
    if any(not isinstance(v, (float, int)) or not math.isfinite(v) or v < 0 for v in (v_train, v_hold)):
        raise ValueError('nonfinite/invalid velocity')
    if v_hold > v_train:
        raise ValueError('holdout maximum exceeds training maximum')
    if aggregate.get('physical_release_authorized') is not False or aggregate.get('product_claim') != 'ABSTAIN_UNCALIBRATED':
        raise ValueError('incompatible product release tier')
    alpha = 0.05
    null_no_exceed = n_train / (n_train + n_hold)
    person_upper = zero_failure_upper(n_hold, alpha)
    naive_blink_upper = zero_failure_upper(n_blinks, alpha)
    kill = null_no_exceed >= 0.5 or person_upper >= 0.10
    return {
        'id': 'E002-454',
        'input': 'E002_453_HUMAN_AGGREGATE.json',
        'source_verified': True,
        'participants_calibration': n_train,
        'participants_held_out': n_hold,
        'heldout_blinks': n_blinks,
        'observed_holdout_exceedances': 0,
        'null_no_exceedance_probability_if_exchangeable_unique_max': null_no_exceed,
        'one_sided_95pct_upper_participant_session_failure_if_iid_people': person_upper,
        'invalid_blink_iid_95pct_upper_for_comparison_only': naive_blink_upper,
        'overconfidence_ratio_participant_vs_blink_iid': person_upper / naive_blink_upper,
        'preregistered_kill_triggered': kill,
        'interpretation': 'DESCRIPTIVE_SAME_STUDY_TRANSFER_NOT_HARD_CAP_VALIDATION',
        'limitations': [
            'exchangeable continuous participant-session maxima and prespecified split assumed for null benchmark',
            'independent comparable people assumed only for participant-level confidence bound',
            'five participants do not establish universal maximum or unseen camera hidden-closure performance',
            'blink-level iid comparison is invalid due to within-participant clustering',
        ],
        'physical_release_authorized': False,
        'product_claim': 'ABSTAIN_UNCALIBRATED',
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--aggregate', type=Path, default=Path(__file__).with_name('E002_453_HUMAN_AGGREGATE.json'))
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    result = analyze(json.loads(args.aggregate.read_text(encoding='utf-8')))
    rendered = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n'
    if args.out:
        args.out.write_text(rendered, encoding='utf-8')
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
