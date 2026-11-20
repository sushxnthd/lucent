"""E002-674: adversarial audit-input forgery regression. Run: python e002_674_auditor_forgery.py"""
import importlib.util
from pathlib import Path

path = Path(__file__).with_name("e002_673_reference_audit.py")
spec = importlib.util.spec_from_file_location("reference_audit", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

base = dict(participant="heldout-1", split="test", interval_id="gap-1",
 modality="gap", certificate=True, reference="no_confirmed_closure",
 clock_calibrated=True, shutter_calibrated=True, quality_ok=True,
 velocity_basis="independent_hard_bound")
def run(row):
 return mod.audit({"protocol":"E002-671","records":[row]})

# Metadata declarations alone cannot establish an independently bounded V.
# This input is accepted even though it contains no velocity value, units,
# timestamp bounds, provenance, calibration artifact or signed attestation.
for mutation in (
 {},
 {"velocity_bound":-1},
 {"velocity_bound":0, "velocity_units":"unknown"},
 {"clock_error_seconds":-999},
 {"shutter_exposure_seconds":-1},
 {"measurement_error":float("nan")},
):
 result=run(dict(base,**mutation))
 assert result["counts"]["eligible"]==1, result
 assert result["decision"]=="INSUFFICIENT_HUMAN_EVIDENCE"

# Positive human witness is correctly rejected even with forged metadata.
positive=run(dict(base,reference="confirmed_closure",rater1="closure",rater2="closure"))
assert positive["counts"]["false_exclusions"]==1
assert positive["decision"]=="FAIL"
print("E002-674: six forged-calibration inputs ACCEPTED as eligible; one positive witness correctly fails")
