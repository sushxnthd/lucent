#!/usr/bin/env python3
"""E002-537 frozen participant-level split-conformal stress (synthetic only)."""
import json
import math
import numpy as np

SEED = 53720261030
ALPHA = 0.05
TRIALS = 20000


def threshold(scores, alpha=ALPHA):
    """Participant nonconformity threshold, +inf when sample too small."""
    values = np.asarray(scores, dtype=float)
    if values.ndim != 1 or len(values) == 0 or np.isnan(values).any():
        raise ValueError('invalid participant scores')
    if not (0 < alpha < 1):
        raise ValueError('invalid alpha')
    k = math.ceil((len(values) + 1) * (1 - alpha))
    return float(np.partition(values, k-1)[k-1]) if k <= len(values) else math.inf


def participant_score(aggressiveness, reference, evidence_ok=True):
    """Truth must be 1=closure, 0=no closure, None=unknown; unknown is fatal."""
    if not evidence_ok:
        return math.inf
    if len(aggressiveness) != len(reference) or not aggressiveness:
        return math.inf
    if any(x is None or x not in (0, 1) for x in reference):
        return math.inf
    if any(not math.isfinite(float(a)) for a in aggressiveness):
        return math.inf
    positives = [float(a) for a, h in zip(aggressiveness, reference) if h == 1]
    return max(positives, default=-math.inf)


def decide(aggressiveness, q, evidence_ok):
    if not evidence_ok or not math.isfinite(aggressiveness):
        return 'ABSTAIN'
    return 'EXCLUDE_CONDITIONALLY' if aggressiveness > q else 'ABSTAIN'


def run(seed=SEED, trials=TRIALS):
    if trials < 10000:
        raise ValueError('>=10000 trials frozen')
    rng = np.random.default_rng(seed)
    outputs = []
    for n in (12, 19, 39):
        k = math.ceil((n + 1) * (1 - ALPHA))
        train = rng.normal(size=(trials, n))
        q = np.sort(train, axis=1)[:, k-1] if k <= n else np.full(trials, math.inf)
        test = rng.normal(size=trials)
        shifted = rng.normal(loc=1.5, size=trials)
        iid_fail = int(np.count_nonzero(test > q))
        shifted_fail = int(np.count_nonzero(shifted > q))
        expected = (n+1-k)/(n+1) if k <= n else 0.0
        p = iid_fail/trials
        se = math.sqrt(expected*(1-expected)/trials)
        outputs.append(dict(n=n,k=k,finite_threshold=(k<=n),iid_failures=iid_fail,
                            iid_risk=p,iid_expected=expected,iid_mc_se=se,
                            iid_within_5se=(abs(p-expected)<=5*se if se else p==expected),
                            shifted_failures=shifted_fail,shifted_risk=shifted_fail/trials))
    # False iid assumption: 600 strongly correlated windows from only 12 people.
    # Chunking prevents excessive peak memory.
    naive_fail = 0
    for _ in range(trials//200):
        latents = rng.normal(size=(200,12,1))
        train = latents + rng.normal(scale=0.1,size=(200,12,50))
        windows = train.reshape(200,600)
        k = math.ceil((601)*(1-ALPHA))
        q = np.partition(windows,k-1,axis=1)[:,k-1]
        new_latent = rng.normal(size=(200,1))
        test = new_latent + rng.normal(scale=0.1,size=(200,50))
        naive_fail += int(np.count_nonzero(np.max(test,axis=1)>q))
    naive_risk = naive_fail/trials
    result = dict(experiment='E002-537',evidence_tier='SYNTHETIC_ONLY',seed=seed,
                  trials=trials,alpha=ALPHA,participant_conditions=outputs,
                  pseudoreplication=dict(calibration_participants=12,
                      windows_per_participant=50,naive_window_count=600,
                      test_participant_any_window_failures=naive_fail,
                      familywise_risk=naive_risk),
                  product='ABSTAIN_UNCALIBRATED',release='BLOCKED')
    assert all(x['iid_within_5se'] for x in outputs)
    assert outputs[0]['iid_risk'] == 0 and not outputs[0]['finite_threshold']
    assert all(x['shifted_risk'] > 0.1 for x in outputs[1:])
    assert naive_risk > 0.05
    return result


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
