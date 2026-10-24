"""E002-420: exact two-exposure observational-equivalence witness (research only)."""
import argparse
import json
import math
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Witness:
    aperture: float
    velocity_per_s: float
    frame_gap_s: float
    exposure_s: float
    closure_threshold: float


def validate(w: Witness) -> None:
    values = tuple(asdict(w).values())
    if not all(isinstance(x, (float, int)) and math.isfinite(x) for x in values):
        raise ValueError('all parameters must be finite')
    a, v, d, e, theta = values
    if not (0 < v and 0 < e <= d and 0 <= theta <= 1 and 0 <= a <= 1):
        raise ValueError('invalid shutter, speed, threshold or aperture')
    if a - v*d/2 < 0:
        raise ValueError('closure-world aperture becomes negative')


def aperture(w: Witness, t: float, world: str) -> float:
    validate(w)
    if world == 'open':
        return w.aperture - w.velocity_per_s*w.exposure_s/8
    if world == 'closure':
        return w.aperture - w.velocity_per_s*min(t, w.frame_gap_s-t) if 0 <= t <= w.frame_gap_s else w.aperture
    raise ValueError('unknown world')


def exposure_average(w: Witness, center: float, world: str, bins: int = 20000) -> float:
    if bins < 2 or bins % 2:
        raise ValueError('midpoint bins must be even and >=2')
    step = w.exposure_s/bins
    start = center - w.exposure_s/2
    return math.fsum(aperture(w, start+(i+0.5)*step, world) for i in range(bins))/bins


def evaluate(w: Witness) -> dict:
    validate(w)
    observed = w.aperture - w.velocity_per_s*w.exposure_s/8
    closure_min = w.aperture - w.velocity_per_s*w.frame_gap_s/2
    ambiguous = closure_min <= w.closure_threshold < observed
    return {
        'research_only': True,
        'conditional_observational_ambiguity': ambiguous,
        'predicted_both_exposure_averages': observed,
        'open_world_minimum': observed,
        'closure_world_minimum': closure_min,
        'dimensionless_exposure_fraction': w.exposure_s/w.frame_gap_s,
        'dimensionless_hidden_depth': w.velocity_per_s*w.frame_gap_s/(2*max(observed-w.closure_threshold, 1e-15)),
        'product': 'ABSTAIN_UNCALIBRATED',
        'product_claim_authorized': False,
        'physical_provenance_authenticated_by_tool': False,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--bins', type=int, default=20000)
    args = p.parse_args()
    w = Witness(.30, 60., 1/240, .002, .20)
    out = evaluate(w)
    out['numerical_camera_observations'] = {
        world: [exposure_average(w, t, world, args.bins) for t in (0, w.frame_gap_s)]
        for world in ('open', 'closure')
    }
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
