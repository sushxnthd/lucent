"""E002-389 experimental decision gate. Not a human-validated camera product."""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Qualification:
    physical_aperture_transfer_independently_validated: bool = False
    optical_error_worst_case_bounded: bool = False
    exposure_intervals_measured: bool = False
    speed_bound_independent_and_applicable: bool = False
    shutter_function_validated: bool = False
    clock_error_bounded: bool = False
    geometry_brightness_blur_gaze_glasses_missingness_qualified: bool = False
    device_and_human_holdout_passed: bool = False


@dataclass(frozen=True)
class Decision:
    status: str
    reason: str
    lower_bound: Optional[float] = None


def decide(*, continuum_safe_lower: Optional[float], threshold: float,
           evidence: Qualification, solver_feasible: bool,
           solver_primal_dual_verified: bool, aperture_units: str) -> Decision:
    if aperture_units != "normalized_physical_aperture":
        return Decision("ABSTAIN", "RGB intensity is not calibrated physical aperture")
    missing = [k for k, v in vars(evidence).items() if not v]
    if missing:
        return Decision("ABSTAIN", "missing independent qualifications: " + ", ".join(missing))
    if not solver_feasible or not solver_primal_dual_verified:
        return Decision("ABSTAIN", "LP infeasible or unverified")
    if continuum_safe_lower is None or not (0 <= threshold <= 1):
        return Decision("ABSTAIN", "missing or invalid threshold/lower bound")
    if not (float("-inf") < continuum_safe_lower < float("inf")):
        return Decision("ABSTAIN", "nonfinite bound")
    if continuum_safe_lower <= threshold:
        return Decision("ABSTAIN", "hidden crossing not excluded")
    return Decision("CONDITIONAL_NO_THRESHOLD_CROSSING",
                    "only within qualified deterministic aperture/timing/speed model",
                    continuum_safe_lower)


def test_fail_closed():
    assert decide(continuum_safe_lower=.246,threshold=.2,evidence=Qualification(),
                  solver_feasible=True,solver_primal_dual_verified=True,
                  aperture_units="normalized_physical_aperture").status=="ABSTAIN"
    assert decide(continuum_safe_lower=.246,threshold=.2,evidence=Qualification(),
                  solver_feasible=True,solver_primal_dual_verified=True,
                  aperture_units="RGB_mean").status=="ABSTAIN"
    full=Qualification(**{k:True for k in vars(Qualification())})
    assert decide(continuum_safe_lower=.2,threshold=.2,evidence=full,
                  solver_feasible=True,solver_primal_dual_verified=True,
                  aperture_units="normalized_physical_aperture").status=="ABSTAIN"
    assert decide(continuum_safe_lower=.246,threshold=.2,evidence=full,
                  solver_feasible=True,solver_primal_dual_verified=True,
                  aperture_units="normalized_physical_aperture").status=="CONDITIONAL_NO_THRESHOLD_CROSSING"


if __name__=="__main__":
    test_fail_closed()
    print("E002-389 fail-closed product gate: PASS (synthetic test only)")
