"""Generate deterministic nonidentifying synthetic E002-477 intake aggregate."""
import json
import tempfile
from e002_477_optical_intake import evaluate
from test_e002_477_optical_intake import make_bundle


def main():
    with tempfile.TemporaryDirectory() as tmp:
        paths = make_bundle(tmp)
        result = evaluate(*paths)
        assert result['qa_status'] == 'PASS_INTAKE_ONLY'
        print(json.dumps({'evidence_tier':'SYNTHETIC_INTAKE_QA_ONLY','frozen_protocol':'E002_477_FROZEN.md','fixture':{'nominal_fps':240,'phase_step_ms':0.05,'scan_periods':2,'repeats_per_phase':20,'row_strata':['top','bottom'],'true_simulated_row_shutter_starts_ms':{'top':0.2,'bottom':0.35}},'result':result},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
