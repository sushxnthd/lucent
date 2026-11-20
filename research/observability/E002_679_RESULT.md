# E002-679 | Physical acquisition intake gate (2026-11-06 UTC)

**Evidence tier:** locally executed instrument-intake software, not physical or human validation.

This executable is a deliberately narrow bridge from the frozen E002-671 study design to physical data acquisition. It screens numerical consistency of paired-camera acquisition manifests, including reference sampling interval, exposure, clock drift, row timing, independently named calibration, and artifact hashes. It rejects a reference camera whose temporal uncertainty cannot resolve the target gap. Six local self-tests passed, including five malformed/inconsistent manifest cases.

**Critical limitation:** hashes and named calibrators are self-declared here. A passing manifest returns `AWAIT_INDEPENDENT_AUTHENTICATION`, never `CERTIFIED`. The script neither authenticates provenance nor establishes a physiological velocity ceiling, anatomical labels, actual reference sensitivity, or usable closure coverage. This is an instrument intake tool, not a measurement-science breakthrough. It must not be counted as independent empirical validation.

**Next decisive action:** capture synchronized photodiode/LED traces and paired ordinary/high-speed videos, independently authenticate calibration, freeze predictions before reference annotation, and run E002-673 on blinded held-out human closures. If reference temporal sensitivity cannot be independently established, abstain. Do not extend synthetic theorem cases in lieu of acquisition.

Reproduce: `python research/observability/e002_679_capture_gate.py --selftest`.

Product remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
