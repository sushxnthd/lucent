"""Adversarial contract test: self-declared provenance is not certification.

Run next to e002_371_claim_gate.py: python e002_371_provenance_spoof.py
Synthetic-only witness; no physical/human validation.
"""
import importlib.util
from pathlib import Path

def witness(evaluate):
    base = dict(
        aperture_observation="instantaneous",
        velocity_bound_provenance="independent_certified_upper",
        timing_provenance="hardware_bounded",
        geometry_provenance="independently_calibrated",
        nuisance_clear=True,
        endpoint0_lower_mm="2", endpoint1_lower_mm="2",
        closure_threshold_mm="0", velocity_upper_mm_s="100", gap_upper_s="0.039")
    # Caller-provided strings are assertions, not authenticated attestations.
    result = evaluate(base)
    assert result["verdict"] == "CONDITIONALLY_EXCLUDED", result
    honest = {**base, "velocity_bound_provenance": "empirical_percentile"}
    assert evaluate(honest)["verdict"] == "ABSTAIN"
    print("CONFIRMED: unauthenticated provenance strings change ABSTAIN to CONDITIONALLY_EXCLUDED")
    print("RELEASE BLOCKER: do not expose as certified exclusion to untrusted inputs")

if __name__ == "__main__":
    gate = Path(__file__).with_name("e002_371_claim_gate.py")
    if not gate.is_file():
        raise SystemExit("Missing gate; fail closed")
    spec = importlib.util.spec_from_file_location("e002_371_claim_gate", gate)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    witness(module.evaluate)
