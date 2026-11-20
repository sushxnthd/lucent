"""E002-428: exact participant-level velocity exceedance tail, study-only.

No hard physiological speed bound or physical camera certificate is produced.
Requires an independently archived, pre-holdout frozen V; a string is not proof.
"""
import argparse
import json
import math


def binomial_cdf(k, n, p):
    """P[Binomial(n,p) <= k], using log-sum-exp to avoid underflow."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n must be a positive integer')
    if not isinstance(k, int) or isinstance(k, bool) or not 0 <= k <= n:
        raise ValueError('k must be between zero and n')
    if not isinstance(p, (int, float)) or isinstance(p, bool) or not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('p must be in [0,1]')
    if k == n or p == 0:
        return 1.0
    if p == 1:
        return 0.0
    logs = [math.lgamma(n+1)-math.lgamma(j+1)-math.lgamma(n-j+1)
            + j*math.log(p)+(n-j)*math.log1p(-p) for j in range(k+1)]
    top = max(logs)
    return min(1.0, math.exp(top)*math.fsum(math.exp(v-top) for v in logs))


def upper_exact(n, k, alpha=0.05):
    """One-sided exact Clopper-Pearson upper confidence bound, IID assumption."""
    if not isinstance(alpha, (int, float)) or isinstance(alpha, bool) or not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError('alpha must be in (0,1)')
    binomial_cdf(k, n, 0.5)  # validate n,k
    if k == n:
        return 1.0
    if k == 0:
        return -math.expm1(math.log(alpha)/n)
    lo, hi = 0.0, 1.0
    for _ in range(85):
        mid = (lo+hi)/2
        if binomial_cdf(k, n, mid) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def evaluate(n, witnessed, unresolved, velocity_mm_s, frozen_reference,
             alpha=0.05, iid_participant_assumption=False):
    """Participant-level sensitivity; unresolved must not become nonviolations."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n must be a positive integer')
    for name, v in [('witnessed', witnessed), ('unresolved', unresolved)]:
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            raise ValueError(name+' must be a nonnegative integer')
    if witnessed+unresolved > n:
        raise ValueError('counts exceed participant count')
    if not isinstance(velocity_mm_s, (int, float)) or isinstance(velocity_mm_s, bool) or not math.isfinite(velocity_mm_s) or velocity_mm_s <= 0:
        raise ValueError('frozen velocity must be positive finite mm/s')
    if not isinstance(frozen_reference, str) or len(frozen_reference.strip()) < 8:
        raise ValueError('independent pre-holdout freeze reference required')
    if not isinstance(iid_participant_assumption, bool):
        raise ValueError('IID assumption flag must be boolean')
    lo = upper_exact(n, witnessed, alpha)
    hi = upper_exact(n, witnessed+unresolved, alpha)
    return {
        'evidence_tier':'STUDY_ONLY_PARTICIPANT_BINOMIAL_SENSITIVITY',
        'participant_count':n, 'witnessed_velocity_exceedances':witnessed,
        'unresolved_participants':unresolved, 'frozen_velocity_mm_s':velocity_mm_s,
        'frozen_reference_unverified':frozen_reference,
        'one_sided_confidence_level':1-alpha,
        'iid_participant_assumption_declared':iid_participant_assumption,
        'best_case_tail_upper':lo, 'worst_case_tail_upper':hi,
        'risk_bound_interpretation':'Only under frozen V and IID independent held-out participants; worst case counts unresolved as exceedances.',
        'population_tail_inference_eligible':iid_participant_assumption,
        'physical_certificate_authorized':False,
        'hard_velocity_bound_authorized':False,
        'product':'ABSTAIN_UNCALIBRATED'
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--participants',type=int,required=True)
    parser.add_argument('--witnessed',type=int,required=True)
    parser.add_argument('--unresolved',type=int,required=True)
    parser.add_argument('--frozen-velocity-mm-s',type=float,required=True)
    parser.add_argument('--frozen-reference',required=True)
    parser.add_argument('--alpha',type=float,default=0.05)
    parser.add_argument('--iid-participants-reviewed',action='store_true')
    args=parser.parse_args()
    print(json.dumps(evaluate(args.participants,args.witnessed,args.unresolved,
        args.frozen_velocity_mm_s,args.frozen_reference,args.alpha,
        args.iid_participants_reviewed),indent=2,sort_keys=True))


if __name__=='__main__':
    main()
