"""E002-421: sharp conditional two-boxcar gap law; NOT a physical product certificate."""
from dataclasses import asdict, dataclass
import argparse
import json
import math


@dataclass(frozen=True)
class GapCase:
    mean: float
    threshold: float
    velocity_per_s: float
    center_separation_s: float
    exposure_s: float


def validate(c: GapCase) -> None:
    a = tuple(asdict(c).values())
    if not all(isinstance(z, (int, float)) and not isinstance(z, bool) and math.isfinite(z) for z in a):
        raise ValueError('all parameters must be finite real numbers')
    m, theta, v, d, e = a
    if not (0 < theta < m < 1 and v > 0 and d > 0 and 0 < e <= d):
        raise ValueError('outside two-equal-mean separated-boxcar model')
    if m - v*d/2 < 0 or m + v*e/2 > 1:
        raise ValueError('outside frozen interior physical feasibility regime')


def trajectory(c: GapCase, t: float, world: str) -> float:
    validate(c)
    if not math.isfinite(t):
        raise ValueError('time must be finite')
    if world == 'open':
        return c.mean
    if world == 'valley':
        return c.mean - c.velocity_per_s*c.center_separation_s/2 + c.velocity_per_s*abs(t - c.center_separation_s/2)
    raise ValueError('unknown trajectory')


def exposure_average(c: GapCase, center: float, world: str, bins: int = 10000) -> float:
    validate(c)
    if not isinstance(bins, int) or isinstance(bins, bool) or bins < 2:
        raise ValueError('invalid quadrature bins')
    e = c.exposure_s
    start = center-e/2
    return math.fsum(trajectory(c, start+(i+.5)*e/bins, world) for i in range(bins))/bins


def evaluate(c: GapCase) -> dict:
    validate(c)
    m, theta, v, d, e = tuple(asdict(c).values())
    gap_lower = m-v*d/2
    ratio = v*(4*d-e)/(8*(m-theta))
    return {
        'evidence_tier': 'conditional analytical and synthetic',
        'sharp_gap_lower': gap_lower,
        'gap_interval_s': [e/2, d-e/2],
        'conditional_research_gap_decision': 'CERTIFY_NO_CROSSING' if gap_lower > theta else 'AMBIGUOUS',
        'construction_specific_E002_420_ratio': ratio,
        'ratio_less_than_one_does_not_certify': ratio < 1 and gap_lower <= theta,
        'dimensionless_velocity_gap_over_margin': v*d/(2*(m-theta)),
        'product': 'ABSTAIN_UNCALIBRATED',
        'product_claim_authorized': False,
        'physical_provenance_authenticated_by_tool': False,
    }


def robust_gap_lower(lower_mean: float, velocity_upper: float, separation_upper: float) -> float:
    vals = (lower_mean, velocity_upper, separation_upper)
    if not all(isinstance(z, (int, float)) and not isinstance(z, bool) and math.isfinite(z) for z in vals):
        raise ValueError('nonfinite or invalid robust inputs')
    if not (0 <= lower_mean <= 1 and velocity_upper > 0 and separation_upper > 0):
        raise ValueError('invalid robust inputs')
    return max(0.0, lower_mean-velocity_upper*separation_upper/2)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--bins', type=int, default=10000)
    args = p.parse_args()
    c = GapCase(.315, .20, 60., 1/240, .002)
    result = evaluate(c)
    result['frozen_example'] = asdict(c)
    result['independent_quadrature_check'] = {
        w: [exposure_average(c, center, w, args.bins) for center in (0., c.center_separation_s)]
        for w in ('open', 'valley')
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
