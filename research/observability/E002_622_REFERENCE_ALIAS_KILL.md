# E002-622 | High-speed reference aliasing: an adversarial velocity-envelope kill test (2026-11-03)

**Evidence tier:** constructive mathematical counterexample and executable synthetic instrument; NOT a human or physical-camera measurement. This is a direct falsification of the tempting inference that the largest finite-difference eyelid speed in a high-frame-rate reference video is a valid continuous-time speed ceiling.

## Constructive counterexample (frozen before any human application)

Take two adjacent reference frames at times 0 and h with measured aperture A>c in both frames. For any desired M>0, define an aperture path that is A at both sampled endpoints and forms a triangular excursion to c at h/2, with piecewise slopes ±2(A-c)/h. Every sampled finite difference is zero, but the true maximum absolute velocity is 2(A-c)/h and a complete closure occurs between reference frames. By reducing the triangle's width to epsilon, its peak speed grows without bound while the same sampled observations persist. Nonnegative aperture and continuity are preserved. Hence no finite continuous-time Lipschitz ceiling follows from finitely many exact aperture samples *without an independently defended regularity constraint*. More high-speed frames shrink the possible excursion duration but do not eliminate this logical non-identifiability.

**Quantitative counterexample:** A=3 mm, c=1 mm, h=1/240 s: an unsampled full closure at the midpoint requires 960 mm/s on the symmetric triangular path while the frame-to-frame estimate remains 0 mm/s. This speed is a mathematical witness, NOT an assertion that human eyelids reach it. Any physical plausibility objection requires independently validated acceleration, bandwidth, velocity or exposure constraints, not an inference from the same frames.

## Consequence for E002-618 / E002-620

The velocity ceiling V must be obtained from independent physical instrumentation or an explicit externally validated dynamical model with a stated coverage/uncertainty claim. Even 240-fps ground-truth *frame labels* cannot establish the absence of subframe closure. A high-speed reference with nonzero exposure also integrates over time; reference-frame labels must not be presented as continuous-time anatomical ground truth. A photodiode verifies timing, not eyelid kinematics.

**Hard stop:** If V is estimated as the maximum observed finite difference on calibration frames alone, E002-371 certificates MUST remain `ABSTAIN_UNCALIBRATED`; held-out zero-error performance cannot repair an invalid deterministic premise. Likewise, any reference closure/no-closure label is bounded by reference temporal resolution and independently assessed shutter integration. Do not call a reference-negative interval a physically proven open interval.

## Next decisive physical test

Use a calibrated motorized occluder with programmable aperture, a traceable position sensor sampled faster than both cameras, and a separate photodiode exposure trace. First demonstrate a deliberately hidden triangular excursion at reference frame boundaries, then repeat at varying widths, phases, shutter duties and brightness. Record raw sensor time series, timestamp uncertainty, encoder uncertainty, motor dynamics and both camera images. Blind the analyst to the commanded trajectory; preregister rejection when the camera-derived bound incorrectly certifies no closure. For humans, require an independent biomechanical speed-envelope justification and explicitly label reference uncertainty; do not transfer the motor's speed envelope to human eyelids.

## Minimal deterministic reproduction

```python
from fractions import Fraction
A,c,h=Fraction(3),Fraction(1),Fraction(1,240)
def aperture(t):
    return A-(A-c)*(2*t/h) if t<=h/2 else c+(A-c)*(2*t/h-1)
assert aperture(0)==A and aperture(h)==A
assert aperture(h/2)==c
sampled_speed=abs(aperture(h)-aperture(0))/h
true_peak_speed=2*(A-c)/h
assert sampled_speed==0 and true_peak_speed==960
print("sampled mm/s",sampled_speed,"hidden peak mm/s",true_peak_speed)
```

The counterexample is exact rational arithmetic. Its scientific purpose is to **kill** unqualified high-speed-derived V certification, not to claim a novel theorem of sampling theory. Product status remains `ABSTAIN_UNCALIBRATED` / `BLOCKED`.
