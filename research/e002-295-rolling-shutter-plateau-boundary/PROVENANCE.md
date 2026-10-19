# Provenance and reproducibility
Source: analytically generated hard-step moving eyelid and row-integrated RGB profile. All inputs hypothetical. No human recordings, no participant data, no paid services, no user laptop compute.
Code: experiment.py, independent_checker.py, stress_controls.py. Independent checker uses Python Fraction and does not import experiment.py.
Random physical-exposure integration: seed 20261019; 80 parameter draws; 4001 shutter samples per case. Derived outputs in results.json, verification.json and stress_results.json. Full integration stress script in downloadable E002-295 package.
Frozen synthetic holdout: HOLDOUT_FREEZE.json. Human protocol frozen but not executed. Prior art and failed gates retained.