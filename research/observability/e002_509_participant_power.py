#!/usr/bin/env python3
"""E002-509: participant-level zero-event risk gate, never physical validation."""
import argparse
import json
import math
from pathlib import Path


def _probability(x, name):
    if type(x) not in (float, int) or not math.isfinite(x) or not 0 < x < 1:
        raise ValueError('INVALID_' + name)
    return float(x)


def zero_failure_upper(n, alpha=0.05, failures=0):
    """Exact one-sided binomial CP upper limit ONLY when failures==0."""
    if type(n) is not int or n <= 0:
        raise ValueError('INVALID_PARTICIPANT_COUNT')
    if type(failures) is not int or failures != 0:
        raise ValueError('NONZERO_FAILURES_REQUIRE_SEPARATE_INTERVAL')
    alpha = _probability(alpha, 'ALPHA')
    return -math.expm1(math.log(alpha) / n)


def minimum_zero_failure_n(target=0.01, alpha=0.05):
    target = _probability(target, 'TARGET')
    alpha = _probability(alpha, 'ALPHA')
    n = max(1, math.ceil(math.log(alpha) / math.log1p(-target)))
    while zero_failure_upper(n, alpha) > target:
        n += 1
    while n > 1 and zero_failure_upper(n - 1, alpha) <= target:
        n -= 1
    return n


def evaluate(records, alpha=0.05, target=0.01):
    """Records must be from real, distinct, independently adjudicated people."""
    _probability(alpha, 'ALPHA')
    _probability(target, 'TARGET')
    if not isinstance(records, list) or not records:
        raise ValueError('NO_PARTICIPANTS')
    seen = set()
    failures = 0
    covered = 0
    total_eligible = 0
    total_certificates = 0
    for r in records:
        if not isinstance(r, dict) or set(r) != {
            'participant_id', 'eligible_windows', 'certificates',
            'false_exclusions', 'unresolved_certificates', 'reference_resolved'
        }:
            raise ValueError('INVALID_PARTICIPANT_RECORD')
        pid = r['participant_id']
        if not isinstance(pid, str) or not pid or pid in seen:
            raise ValueError('MISSING_OR_DUPLICATE_PARTICIPANT')
        seen.add(pid)
        eligible, cert, failed, unknown = (r[k] for k in (
            'eligible_windows', 'certificates', 'false_exclusions', 'unresolved_certificates'))
        if any(type(x) is not int or x < 0 for x in (eligible, cert, failed, unknown)):
            raise ValueError('INVALID_COUNTS')
        if eligible == 0 or cert > eligible or failed + unknown > cert:
            raise ValueError('INCONSISTENT_COUNTS')
        if r['reference_resolved'] is not True or unknown:
            raise ValueError('UNRESOLVED_REFERENCE_CANNOT_COUNT_AS_SUCCESS')
        failures += int(failed > 0)
        covered += int(cert > 0)
        total_eligible += eligible
        total_certificates += cert
    n = len(records)
    result = {
        'experiment': 'E002-509', 'participants': n,
        'participant_failures': failures, 'participants_with_certificate': covered,
        'participants_without_certificate': n - covered,
        'eligible_windows': total_eligible, 'certified_windows': total_certificates,
        'confidence': 1 - alpha, 'target_participant_session_risk': target,
        'minimum_zero_failure_participants': minimum_zero_failure_n(target, alpha),
        'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED',
        'hard_physical_guarantee': False,
    }
    # E002-511: distinguish unconditional session risk (all enrolled)
    # from conditional risk GIVEN >=1 certificate (covered participants).
    # A large abstaining cohort must never imply conditional certificate safety.
    result['unconditional_risk_denominator'] = n
    result['conditional_risk_denominator'] = covered
    result['certificate_participant_coverage'] = covered / n
    result['coverage_utility_target_preregistered'] = False
    result['conditional_estimand'] = 'P(any_false_exclusion | at_least_one_certificate)'
    result['unconditional_estimand'] = 'P(any_false_exclusion_per_enrolled_session)'
    if failures:
        result['risk_gate'] = 'NONZERO_FAILURES_REQUIRE_EXACT_INTERVAL'
        result['zero_failure_upper'] = None
        result['unconditional_zero_failure_upper'] = None
        result['conditional_zero_failure_upper'] = None
    else:
        # Retain the legacy field for compatibility, but explicitly label it
        # UNCONDITIONAL; never use it for a conditional safety gate.
        result['zero_failure_upper'] = zero_failure_upper(n, alpha)
        result['unconditional_zero_failure_upper'] = result['zero_failure_upper']
        result['conditional_zero_failure_upper'] = (
            zero_failure_upper(covered, alpha) if covered else None)
        if covered == 0:
            result['risk_gate'] = 'NO_USEFUL_COVERAGE'
        elif result['conditional_zero_failure_upper'] <= target:
            result['risk_gate'] = 'PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY'
        elif covered < n:
            result['risk_gate'] = 'INSUFFICIENT_COVERED_PARTICIPANTS'
        else:
            result['risk_gate'] = 'INSUFFICIENT_PARTICIPANTS'
    result['human_data_authenticated_by_code'] = False
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-cohort-json', type=Path)
    args = p.parse_args()
    if args.private_cohort_json:
        cohort = json.loads(args.private_cohort_json.read_text(encoding='utf-8'))
        print(json.dumps(evaluate(cohort), sort_keys=True, indent=2))
    else:
        print(json.dumps({
            'experiment': 'E002-509', 'evidence': 'MATHEMATICAL_DESIGN_ONLY',
            'zero_failure_upper': {str(n): zero_failure_upper(n) for n in (8, 24, 80, 298, 299, 300)},
            'minimum_n_at_95_percent_for_1_percent_risk': minimum_zero_failure_n(),
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'
        }, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
