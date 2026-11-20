# E002-712 | Phase-randomized shutter synthetic prediction and abstention

**Tier:** deterministic synthetic oracle, not physical or human evidence.

A triangular unit-amplitude closure deficit with half-width w is integrated exactly over shutter duration T. Random shutter start is uniform over [-S/2,S/2]. With independently bounded total photometric error e, a positive closure signal is certified only when mean deficit d exceeds e; otherwise ABSTAIN. Absence of signal never certifies absence of closure.

Executed locally: `python research/observability/e002_712_phase_instrument.py --seed 712 --n 10000`. Exact-integral self-tests PASS. T=1, w=.2, S=4: ideal e=0, 3459 detectable / 6541 abstentions; bounded e=.10, 2487 detectable / 7513 abstentions; uninformative e=1, 0 detectable / 10000 abstentions. All counts are synthetic and depend on the stipulated phase distribution. The initial test expected ambiguity under zero-error zero-signal and failed; it was corrected to treat zero signal as ABSTAIN.

**Frozen prospective physical test:** independently time occluder motion with encoder/photodiode, randomize external shutter trigger phase, record actual exposure timing and uncertainty, calibrate aperture-to-intensity response on disjoint trials, and stratify phase, brightness, geometry, gaze, blur, glasses, missingness, rolling shutter, clock error. Before held-out trials freeze waveform, uncertainty bounds, detection threshold and exclusion policy. Publish all phase-by-phase predicted/observed detection and abstention results; indeterminate reference timing or closure labels must themselves abstain. Follow with consented participant-disjoint human recordings and independently justified physiological velocity limits.

**Product:** reject uncalibrated pixel-brightness closure-exclusion; no detection is not no blink. Remain ABSTAIN_UNCALIBRATED, production BLOCKED.