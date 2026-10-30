#!/usr/bin/env python3
"""E002-544: noncertifying session-wise optical-edge multiplicity gate.

No physical sources are authenticated here. Frozen protocol: E002_544_FROZEN.md.
"""
from __future__ import annotations
import argparse
import json
import math
import random
import re
from pathlib import Path

SCHEMA = 'E002-544-v1'
TOP_KEYS = {'schema', 'prelabel_commitment', 'alpha', 'nuisance_stratum',
            'calibration_sessions', 'test_session'}
SESSION_KEYS = {'session_id', 'partition', 'nuisance_stratum', 'paired_differences',
                'eligible_outside_verified', 'quality_verified'}
HEX64 = re.compile(r'^[0-9a-f]{64}$')
ALPHA = 0.05


def finite_number(v):
    return type(v) in (int, float) and math.isfinite(v)


def abstain(reason):
    return {'schema': SCHEMA, 'decision': 'ABSTAIN_INVALID_EVIDENCE',
            'reason': reason, 'evidence_tier': 'OWNER_ASSERTED_NOT_AUTHENTICATED',
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def evaluate(p):
    if type(p) is not dict or set(p) != TOP_KEYS or p.get('schema') != SCHEMA:
        return abstain('schema')
    if (type(p['prelabel_commitment']) is not str
            or HEX64.fullmatch(p['prelabel_commitment']) is None):
        return abstain('unverified_prelabel_digest')
    if not finite_number(p['alpha']) or p['alpha'] != ALPHA:
        return abstain('alpha_not_frozen')
    stratum = p['nuisance_stratum']
    if type(stratum) is not str or not stratum.strip():
        return abstain('stratum')
    nulls = p['calibration_sessions']
    if type(nulls) is not list or len(nulls) < 19:
        return abstain('insufficient_independent_null_sessions')
    sessions = nulls + [p['test_session']]
    ids = set()
    maxima = []
    n = None
    for i, session in enumerate(sessions):
        if type(session) is not dict or set(session) != SESSION_KEYS:
            return abstain('session_schema')
        ident = session['session_id']
        if type(ident) is not str or not ident.strip() or ident in ids:
            return abstain('nonunique_session_identity')
        ids.add(ident)
        expected = 'calibration_null' if i < len(nulls) else 'heldout_outside'
        if session['partition'] != expected:
            return abstain('partition')
        if session['nuisance_stratum'] != stratum:
            return abstain('nuisance_shift_or_mismatch')
        if (session['eligible_outside_verified'] is not True
                or session['quality_verified'] is not True):
            return abstain('timing_or_quality_not_verified')
        residuals = session['paired_differences']
        if type(residuals) is not list or not residuals:
            return abstain('missing_windows')
        if n is None:
            n = len(residuals)
        if len(residuals) != n:
            return abstain('window_count_mismatch')
        if any(not finite_number(v) or abs(v) > 1 for v in residuals):
            return abstain('invalid_roi_difference')
        maxima.append(max(abs(v) for v in residuals))
    m = len(nulls)
    test_max = maxima[-1]
    pvalue = (1 + sum(x >= test_max for x in maxima[:-1])) / (m + 1)
    return {'schema': SCHEMA,
            'decision': ('FALSIFICATION_CANDIDATE_FWER' if pvalue <= ALPHA
                         else 'NO_FALSIFICATION_CENSORED'),
            'calibration_sessions': m, 'windows_per_session': n,
            'rank_pvalue': pvalue, 'evidence_tier': 'OWNER_ASSERTED_NOT_AUTHENTICATED',
            'physical_source_authenticated': False,
            'shutter_support_certified': False,
            'human_anatomical_validation': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def simulate(seed=5442026, replications=2000, m=39, windows=200):
    rng = random.Random(seed)
    naive = 0
    ranked = 0
    shifted = 0
    per_trial_threshold = 1.959963984540054
    for _ in range(replications):
        null_maxima = [max(abs(rng.gauss(0, 1)) for _ in range(windows))
                       for _ in range(m)]
        test = [abs(rng.gauss(0, 1)) for _ in range(windows)]
        shifted_test = [1.25 * abs(rng.gauss(0, 1)) for _ in range(windows)]
        test_max = max(test)
        naive += test_max > per_trial_threshold
        ranked += ((1 + sum(x >= test_max for x in null_maxima)) / (m + 1)) <= ALPHA
        shifted += ((1 + sum(x >= max(shifted_test) for x in null_maxima)) / (m + 1)) <= ALPHA
    return {'schema': 'E002-544-SYNTHETIC-v1', 'seed': seed,
            'replications': replications, 'null_sessions_per_replication': m,
            'windows_per_session': windows,
            'naive_independent_null_exact_any_hit': 1 - (1 - ALPHA)**windows,
            'naive_null_any_hit_count': naive,
            'naive_null_any_hit_rate': naive / replications,
            'rank_null_candidate_count': ranked,
            'rank_null_candidate_rate': ranked / replications,
            'rank_shift_1_25_candidate_count': shifted,
            'rank_shift_1_25_candidate_rate': shifted / replications,
            'physical_captures': 0, 'human_ratings': 0,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def no_duplicate_keys(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            raise ValueError('duplicate JSON key')
        d[key] = value
    return d


def load_private(path):
    with Path(path).open(encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=no_duplicate_keys,
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON number')))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--simulate', action='store_true', help='frozen synthetic stress test')
    group.add_argument('--input', help='owner-private matched-session manifest')
    ap.add_argument('--output', default='-', help='aggregate-only JSON output')
    args = ap.parse_args()
    if args.simulate:
        result = simulate()
    else:
        try:
            result = evaluate(load_private(args.input))
        except (ValueError, TypeError, OSError, UnicodeError):
            result = abstain('unreadable_or_invalid_json')
    out = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output == '-':
        print(out, end='')
    else:
        Path(args.output).write_text(out, encoding='utf-8')


if __name__ == '__main__':
    main()
