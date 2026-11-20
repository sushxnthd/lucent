"""E002-440: participant-cluster falsification and conservative human-ledger gate.

No physical measurement, velocity-cap validation or deployment authorization.
Standard-library only. Do not publish private human ledgers.
"""
import argparse
import json
import math
import random
from pathlib import Path


def binomial_cdf(k: int, n: int, p: float) -> float:
    """P[Binomial(n,p) <= k], stable around its quantile for n<=several thousand."""
    if not isinstance(n, int) or not isinstance(k, int) or n <= 0 or not 0 <= k <= n:
        raise ValueError("require integer 0 <= k <= n and n > 0")
    if not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError("p must lie in [0,1]")
    if k == n or p == 0:
        return 1.0
    if p == 1:
        return 0.0
    if k == 0:
        return math.exp(n * math.log1p(-p))
    mass = math.exp(math.lgamma(n + 1) - math.lgamma(k + 1)
                    - math.lgamma(n - k + 1) + k * math.log(p)
                    + (n - k) * math.log1p(-p))
    total = mass
    for j in range(k - 1, -1, -1):
        mass *= ((j + 1) * (1 - p)) / ((n - j) * p)
        total += mass
    return min(1.0, total)


def cp_upper(failures: int, participants: int, alpha: float = 0.05) -> float:
    """Exact one-sided binomial upper confidence bound; assumes iid participants."""
    if not isinstance(participants, int) or not isinstance(failures, int) or participants < 1 or not 0 <= failures <= participants:
        raise ValueError("invalid participant/failure count")
    if not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must be strictly between 0 and 1")
    if failures == participants:
        return 1.0
    if failures == 0:
        return -math.expm1(math.log(alpha) / participants)
    low, high = 0.0, 1.0
    for _ in range(80):
        mid = (low + high) / 2
        if binomial_cdf(failures, participants, mid) > alpha:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def min_zero_failure_participants(alpha: float, target: float) -> int:
    if not (0 < alpha < 1 and 0 < target < 1):
        raise ValueError("alpha and target must be in (0,1)")
    n = max(1, math.floor(math.log(alpha) / math.log1p(-target)))
    while cp_upper(0, n, alpha) >= target:
        n += 1
    while n > 1 and cp_upper(0, n - 1, alpha) < target:
        n -= 1
    return n


def run_cluster_countermodel(seed: int = 440, trials: int = 20000,
                             participants: int = 30, frames: int = 40,
                             latent_risk: float = 0.05) -> dict:
    if not isinstance(trials, int) or trials <= 0 or participants <= 0 or frames <= 0 or not 0 <= latent_risk <= 1:
        raise ValueError("invalid simulation parameters")
    rng = random.Random(seed)
    zero = 0
    total_failed_participants = 0
    for _ in range(trials):
        failed_participants = sum(rng.random() < latent_risk for _ in range(participants))
        total_failed_participants += failed_participants
        zero += failed_participants == 0
    analytic = (1 - latent_risk) ** participants
    return {
        "evidence_tier": "synthetic_countermodel_only",
        "seed": seed, "trials": trials, "participants_per_trial": participants,
        "candidate_frames_per_participant": frames,
        "true_participant_any_error_risk": latent_risk,
        "zero_error_studies": zero,
        "observed_zero_error_frequency": zero / trials,
        "exact_zero_error_probability": analytic,
        "mean_failed_participants": total_failed_participants / trials,
        "zero_error_cp_upper_participant": cp_upper(0, participants),
        "zero_error_naive_frame_upper_INVALID": cp_upper(0, participants * frames),
        "minimum_independent_zero_error_participants_for_upper_below_1pct": min_zero_failure_participants(.05, .01),
        "physical_release_authorized": False,
    }


def adjudicate_ledger(study: dict) -> dict:
    """Read-only risk accounting. Boolean attestations are NOT authentication."""
    if not isinstance(study, dict) or study.get("evidence_tier") not in ("synthetic", "human_prospective"):
        raise ValueError("explicit evidence tier required")
    people = study.get("participants")
    if not isinstance(people, list) or not people:
        raise ValueError("nonempty participant list required")
    seen = set()
    failures = eligible = unresolved = abstain_only = 0
    total_candidates = total_abstentions = 0
    for person in people:
        if not isinstance(person, dict):
            raise ValueError("participant must be an object")
        pid = person.get("participant_id")
        if not isinstance(pid, str) or not pid or pid in seen:
            raise ValueError("participant identifiers must be unique nonempty strings")
        seen.add(pid)
        flags = ("predictions_locked", "reference_authenticated", "physical_calibration_authenticated", "nuisance_complete")
        if any(type(person.get(flag)) is not bool for flag in flags):
            raise ValueError("all participant attestation flags must be explicit booleans")
        observations = person.get("observations")
        if not isinstance(observations, list) or not observations:
            raise ValueError("participant must have observations")
        candidate_refs = []
        for row in observations:
            if not isinstance(row, dict) or row.get("decision") not in ("ABSTAIN", "NO_CLOSURE_CANDIDATE"):
                raise ValueError("invalid prediction decision")
            if row["decision"] == "ABSTAIN":
                if row.get("reference") is not None:
                    raise ValueError("abstentions cannot supply candidate reference successes")
                continue
            if row.get("reference") not in ("NEGATIVE_CONDITIONAL", "WITNESSED_FALSE", "UNRESOLVED"):
                raise ValueError("candidate reference must be independently adjudicated")
            candidate_refs.append(row["reference"])
        total_candidates += len(candidate_refs)
        total_abstentions += len(observations) - len(candidate_refs)
        if not candidate_refs:
            abstain_only += 1
        elif "WITNESSED_FALSE" in candidate_refs:
            failures += 1
        elif ("UNRESOLVED" in candidate_refs or len(candidate_refs) != 40 or
              len(observations) != 40 or not all(person[flag] for flag in flags)):
            unresolved += 1
        else:
            eligible += 1
    n_evaluable = eligible + failures
    upper = cp_upper(failures, n_evaluable) if n_evaluable else None
    flags = ("random_sampling_verified", "external_review_verified", "velocity_cap_verified", "nuisance_transport_verified")
    if any(type(study.get(flag)) is not bool for flag in flags):
        raise ValueError("all study-level attestation flags must be explicit booleans")
    review_candidate = (study["evidence_tier"] == "human_prospective" and
                        all(study[flag] for flag in flags) and
                        unresolved == 0 and abstain_only == 0 and
                        failures == 0 and n_evaluable >= 299 and
                        upper is not None and upper < .01)
    return {"participants_total": len(people), "candidate_intervals_total": total_candidates,
            "abstention_intervals_total": total_abstentions,
            "evaluable_participants": n_evaluable,
            "participant_any_false": failures, "eligible_negative_participants": eligible,
            "unresolved_participants": unresolved, "abstain_only_participants": abstain_only,
            "one_sided_95pct_upper_conditional_on_iid_and_complete_reference": upper,
            "eligible_for_external_release_review_ONLY": review_candidate,
            "physical_release_authorized": False,
            "warning": "Attestation booleans are not cryptographic proof; fixed 40-candidate challenge and complete reference required; selected reference labels invalidate population claims."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ledger", type=Path, help="private prospective JSON ledger; never publish participant records")
    parser.add_argument("--seed", type=int, default=440)
    parser.add_argument("--trials", type=int, default=20000)
    args = parser.parse_args()
    result = adjudicate_ledger(json.loads(args.ledger.read_text())) if args.ledger else run_cluster_countermodel(seed=args.seed, trials=args.trials)
    output = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
