# E002-753 | Exposure-kernel-shape falsification (2026-11-11 UTC)

## Question
Does E002-752's duration/exposure/threshold ratio R=d/(theta e) determine detectability for an exposure-integrating reference detector when the temporal weighting is unknown?

## Frozen synthetic comparison
Event: unit-amplitude full closure lasting d=1/4 of a unit exposure, threshold theta=3/4 of normalized detector response. Three nonnegative, unit-integral temporal kernels: uniform density 1 on [0,1]; front density 4 on [0,1/4] and zero elsewhere; rear density 4 on [3/4,1] and zero elsewhere. Exact rational overlap integration. Enumerate 7,501 start phases i/10000 for i=0,...,7500; a closure stays entirely within [0,1]. No parameter fitting, human data, or instrument calibration.

## Locally executed result
```
uniform 0 of 7501 admissible phases
front 626 of 7501 admissible phases
rear 626 of 7501 admissible phases
PASS: kernel counterexamples and exact phase enumeration
```
For an event at exposure start, the uniform, front, and rear responses are respectively 1/4, 1, and 0. The rear kernel detects the event at start 3/4. All have R=1/3. Hence R<1 is an impossibility condition **only under the uniform temporal weighting assumed by E002-752**, not a kernel-independent law. The 626/7501 phase counts are deterministic grid counts, not random-phase probability estimates.

## Corrected conditional rule
For a known nonnegative unit-integral kernel k(t), an event interval I is detectable iff integral_I k(t)dt >= theta in this ideal unit-contrast model. For a kernel density known only to satisfy k(t)<=M, every event of duration d with Md<theta is undetectable (necessary condition); this says nothing about sufficiency or actual detector noise. If kernel support or response linearity is uncalibrated, the detector's negative closure labels are not independently certified.

## Product / experimental consequence
Physical reference calibration must sweep pulse **phase and width** while recording temporal response, not just nominal FPS and exposure duration. Freeze measured kernel or a conservative envelope before held-out acquisition; include response nonlinearity, clock offset, detector bandwidth and threshold drift. Do not generalize the E002-752 R threshold beyond uniform kernels. E002-744 human study and E002-750 negative-label restrictions remain unchanged. Evidence tier T1 synthetic; human/physical observations zero; product ABSTAIN_UNCALIBRATED, release BLOCKED.

Reproduce: `python research/observability/e002_753_kernel_detector_falsifier.py` (Python standard library). No external data or network.
