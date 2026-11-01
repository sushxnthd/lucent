# E002-593 | Prospective virtual-shutter uncertainty stress protocol

Date: 2026-11-01 UTC. Kernel: E002-371. Evidence: **synthetic oracle experiment only**. The synthetic generator was explored locally before GitHub freezing; this is NOT a prospectively preregistered human study. This document freezes its deterministic reproduction and a separate future physical study.

## Question
Does the E002-371 shutter-gap exclusion survive independently bounded endpoint-aperture and clock error, and how often does the naive nominal test falsely exclude an actual hidden closure near the mathematical boundary?

## Synthetic oracle and held-out comparison
Run 12,000 deterministic independent *synthetic scenarios* from xorshift32 seed 593, integer arithmetic. For each: c in [300,800] milli-aperture units, threshold tau=100; physical gap g in [12000,30000] microseconds; ratio r in [850,1150] milliunits, where V*g/[2(c-tau)]=r/1000. Generate two independently perturbed observed endpoint apertures c+eL and c+eR, each e in [-20,20] milliunits, and observed gap g+eT with eT in [-1500,1500] microseconds. All draws are inclusive uniform integer modular draws; this is a deterministic test distribution, not a population model. The synthetic true eyelid trajectory is the V-Lipschitz symmetric tent with endpoints c and center c-(c-tau)*r/1000. It reaches tau iff r>=1000. Exact equality counts as closure.

Compute strict (not <=) exclusion:
- naive: V*gObserved < aLeftObserved+aRightObserved-2*tau
- robust: V*(gObserved+1500) < (aLeftObserved-20)+(aRightObserved-20)-2*tau
- oracle: r<1000.

Evaluate false exclusions (predicted impossible despite true synthetic closure) and coverage. Strict equality must abstain. Use integer cross-products, no floating-point boundary decisions. Independent Python and Node BigInt implementations must match every aggregate.

## Required falsification
A calibrated bound is essential: at c=500, tau=100, g=20000, r=1000, measured gap=18500 and both measured endpoints=520, the robust exclusion must abstain at equality. If endpoint measurement error is actually +30 while declared <=20, endpoints=530 make the nominally robust method **falsely exclude** a closure. Report this as model misspecification, not a production attack on a deployed camera.

## Prospective physical handoff (NOT performed)
1. Freeze shutter and rolling-row exposure supports using independent optical phase scan and photodiode, including response nonlinearity and clock uncertainty.
2. Measure anatomical eyelid aperture in synchronized high-speed video (preferably >=400-600 fps) using two independent blinded raters; obtain participant-disjoint calibration and holdout groups. Do not infer a hard continuous-time V ceiling from discrete maximum observed speed.
3. Calibrate geometric aperture uncertainty and physical V ceiling by separately justified instrument/physiological assumptions; otherwise abstain. Freeze gaze, glasses, blur, brightness, missingness and row-exposure strata before holdout.
4. For each ordinary-camera shutter gap, calculate exclusion without seeing held-out anatomical labels; count any reference-confirmed closure during an exclusion as a falsification, with reference sensitivity and temporal-dwell limitations disclosed.
5. Report participant/session-clustered false exclusions and abstention. Keep product ABSTAIN_UNCALIBRATED / BLOCKED until independently reviewed physical evidence exists.

No physical capture, anatomical rater pair, or certified physiological speed ceiling is supplied by this experiment.
