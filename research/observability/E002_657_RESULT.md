# E002-657 | Shutter-kernel first-moment falsification

**Tier:** exact deterministic synthetic counterexample, not physical or human validation.

## New boundary
For nonnegative normalized shutter response k(u), observed exposure average y at nominal center s, and a V-Lipschitz scalar aperture a, the one-observation certificate is
a(t) >= y - V ∫ k(u)|t-s-u|du.
It is sharp without additional aperture constraints: a(x)=c+V|x-t| attains equality (choose a bounded admissible domain and c to avoid saturation). The familiar V e/4 uncertainty at the exposure center assumes a *uniform rectangular* shutter kernel of width e; knowing e alone does not justify that factor.

## Falsifier
Set e=0.20 seconds, V=4 aperture units/second, closure threshold 0.30, and a(t)=0.20+4|t|. Let exposure weight be uniform only on offsets [0.09,0.10] seconds (within the nominal [-0.10,0.10] window). Its absolute first moment is 0.095 seconds rather than 0.05. The exposure mean is 0.58. A rectangular-kernel assumption incorrectly certifies a(0)>=0.38 (>0.30), despite the actual a(0)=0.20. The calibrated kernel-moment bound gives exactly 0.20 and therefore abstains.

## Reproduction
Run `python3 research/observability/e002_657_shutter_kernel.py`. Uses only Python standard library and rational arithmetic; no random seed or external data. The code asserts the counterexample and the rectangular control. GitHub hosted CI and independent execution are not established by this commit.

## Product consequence
Do not treat nominal exposure duration as sufficient shutter calibration. Require an independently bounded temporal shutter response (or conservatively use maximum possible temporal offset e/2, plus clock and row uncertainty). Unknown exposure weighting forces `ABSTAIN_UNCALIBRATED`; production remains `BLOCKED`.

## Scope and next experiment
This result isolates temporal weighting. It does not model spatial optics, image-derived aperture error, rolling shutter variation, saturation, or human eyelid velocities. Independently measure LED/photodiode shutter temporal impulse response across relevant image rows, freeze a worst-case moment bound before evaluating held-out eyelid sequences, and run the E002-653 protocol. No physiological or clinical claim is unlocked.
