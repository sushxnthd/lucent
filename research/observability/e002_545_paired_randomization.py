#!/usr/bin/env python3
"""E002-545 exact whole-vector sign randomization for paired optical-edge interventions.

Research-only. No camera/shutter/human certification. Python standard library only.
"""
import argparse
import itertools
import json
import math
import sys
import unittest

MIN_PAIRS = 5
MAX_PAIRS = 16
MAX_POSITIONS = 200
ALPHA = 0.05


def _finite_vector(v, k):
    return (isinstance(v, list) and len(v) == k and
            all(type(x) in (int, float) and math.isfinite(x) and abs(x) <= 1e6 for x in v))


def exact_p(differences):
    """Return (p, tail_count, total, observed_T); flips entire position vectors."""
    n = len(differences)
    k = len(differences[0])
    obs = max(sum(row[j] for row in differences) for j in range(k))
    tail = 0
    for bits in range(1 << n):
        totals = [0.0] * k
        for i, row in enumerate(differences):
            sign = -1 if bits & (1 << i) else 1
            for j, val in enumerate(row):
                totals[j] += sign * val
        if max(totals) >= obs - 1e-10 * max(1.0, abs(obs)):
            tail += 1
    return tail / (1 << n), tail, 1 << n, obs


def analyze(doc):
    def abstain(reason):
        return {'decision': 'ABSTAIN', 'reason': reason, 'product': 'ABSTAIN_UNCALIBRATED'}
    if not isinstance(doc, dict):
        return abstain('INVALID_DOCUMENT')
    if doc.get('randomization_attested') is not True or doc.get('predeclared_analysis') is not True:
        return abstain('UNAUTHENTICATED_DESIGN')
    positions = doc.get('frozen_positions')
    if (not isinstance(positions, list) or not 1 <= len(positions) <= MAX_POSITIONS or
            len(set(map(str, positions))) != len(positions) or
            any(type(p) is not int or p < 0 for p in positions)):
        return abstain('INVALID_POSITIONS')
    pairs = doc.get('pairs')
    if not isinstance(pairs, list) or not MIN_PAIRS <= len(pairs) <= MAX_PAIRS:
        return abstain('INVALID_PAIR_COUNT')
    ids = set()
    differences = []
    for pair in pairs:
        if not isinstance(pair, dict):
            return abstain('INVALID_PAIR')
        ident = pair.get('pair_id')
        if not isinstance(ident, str) or not ident or ident in ids:
            return abstain('INVALID_PAIR_ID')
        ids.add(ident)
        if (pair.get('timing_owner_attested') is not True or
                pair.get('quality_owner_attested') is not True or
                pair.get('no_carryover_owner_attested') is not True):
            return abstain('UNRESOLVED_NUISANCE')
        assignment = pair.get('assignment')
        if assignment not in ('A_FLASH', 'B_FLASH'):
            return abstain('INVALID_ASSIGNMENT')
        a, b = pair.get('arm_a'), pair.get('arm_b')
        if not _finite_vector(a, len(positions)) or not _finite_vector(b, len(positions)):
            return abstain('INVALID_MEASUREMENT')
        if assignment == 'A_FLASH':
            differences.append([x-y for x, y in zip(a, b)])
        else:
            differences.append([y-x for x, y in zip(a, b)])
    p, tail, total, obs = exact_p(differences)
    return {'decision': 'FALSIFICATION_CANDIDATE_RANDOMIZED' if p <= ALPHA else 'NO_RANDOMIZED_EVIDENCE',
            'p_value': p, 'tail_assignments': tail, 'total_assignments': total,
            'positions': len(positions), 'pairs': len(pairs), 'max_sum_difference': obs,
            'evidence': 'OWNER_ATTESTED_RANDOMIZATION_NOT_PHYSICALLY_VERIFIED',
            'product': 'ABSTAIN_UNCALIBRATED'}


def fixture(n=8, k=5, effect=1.0):
    return {'randomization_attested': True, 'predeclared_analysis': True,
            'frozen_positions': list(range(k)),
            'pairs': [{'pair_id': f'pair-{i}', 'assignment': 'A_FLASH',
                       'arm_a': [effect] * k, 'arm_b': [0.0] * k,
                       'timing_owner_attested': True, 'quality_owner_attested': True,
                       'no_carryover_owner_attested': True} for i in range(n)]}


class Tests(unittest.TestCase):
    def test_strong_signal(self):
        r = analyze(fixture())
        self.assertEqual(r['tail_assignments'], 1)
        self.assertEqual(r['total_assignments'], 256)
        self.assertEqual(r['decision'], 'FALSIFICATION_CANDIDATE_RANDOMIZED')

    def test_ties(self):
        self.assertEqual(analyze(fixture(effect=0))['p_value'], 1)

    def test_minimum_resolution(self):
        self.assertEqual(analyze(fixture(n=5))['p_value'], 1/32)
        self.assertEqual(analyze(fixture(n=5))['decision'], 'FALSIFICATION_CANDIDATE_RANDOMIZED')

    def test_four_pairs_never_significant(self):
        diffs = [[i+0.2*j for j in range(5)] for i in range(1,5)]
        for signs in itertools.product((-1,1), repeat=4):
            p, _, _, _ = exact_p([[s*x for x in row] for s,row in zip(signs,diffs)])
            self.assertGreater(p, ALPHA)

    def test_exact_null_superuniform(self):
        # Fixed, highly correlated and heteroskedastic potential outcomes.
        diffs = [[(i+1)*(1 if j%2 else -0.3)+j*0.01 for j in range(5)] for i in range(8)]
        false = 0
        for signs in itertools.product((-1,1), repeat=8):
            p, _, _, _ = exact_p([[s*x for x in row] for s,row in zip(signs,diffs)])
            false += p <= ALPHA
        self.assertLessEqual(false, 0.05 * 256)

    def test_many_positions(self):
        r = analyze(fixture(k=200))
        self.assertEqual(r['positions'], 200)
        self.assertEqual(r['tail_assignments'], 1)

    def test_reversed_arm(self):
        doc = fixture()
        for pair in doc['pairs']:
            pair['assignment'] = 'B_FLASH'
            pair['arm_a'], pair['arm_b'] = pair['arm_b'], pair['arm_a']
        self.assertEqual(analyze(doc)['tail_assignments'], 1)

    def test_invalid_evidence(self):
        edits = [lambda d: d.update(randomization_attested=False),
                 lambda d: d.update(predeclared_analysis=False),
                 lambda d: d['pairs'][0].update(no_carryover_owner_attested=False),
                 lambda d: d['pairs'][0].update(timing_owner_attested=False),
                 lambda d: d['pairs'][0].update(quality_owner_attested=False),
                 lambda d: d['pairs'][0].update(assignment='BOTH_FLASH'),
                 lambda d: d['pairs'][0].update(arm_a=[float('nan')]*5),
                 lambda d: d['pairs'][0].update(arm_b=[float('inf')]*5),
                 lambda d: d['pairs'][0].update(arm_a=[1]*4),
                 lambda d: d['pairs'][1].update(pair_id='pair-0'),
                 lambda d: d.update(frozen_positions=[0,0,1,2,3]),
                 lambda d: d.update(pairs=d['pairs'][:4]),
                 lambda d: d.update(pairs=d['pairs']*3)]
        for edit in edits:
            d = fixture()
            edit(d)
            self.assertEqual(analyze(d)['decision'], 'ABSTAIN')

    def test_carryover_fails_closed(self):
        d = fixture()
        d['pairs'][2]['no_carryover_owner_attested'] = False
        self.assertEqual(analyze(d)['decision'], 'ABSTAIN')

    def test_product_never_certifies(self):
        self.assertEqual(analyze(fixture())['product'], 'ABSTAIN_UNCALIBRATED')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Owner-private JSON of paired blocks')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=[sys.argv[0]])
    elif args.input:
        with open(args.input, encoding='utf-8') as f:
            result = analyze(json.load(f))
        print(json.dumps(result, sort_keys=True))
    else:
        parser.error('Use --input or --self-test')
