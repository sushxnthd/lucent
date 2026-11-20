# E002-641 | Spatial uncertainty creates an optimal calibration cadence

**Evidence tier:** exact analytic result plus locally executed deterministic synthetic assertions; no physical or human validation. Extends E002-640 without changing the scientific kernel.

Suppose a continuously differentiable aperture x(t) has a separately certified |x''| <= A on a true interval h. Both endpoint aperture measurements have independent *worst-case* absolute error <= epsilon (independence is not a probabilistic assumption). If measured displacement is D, then

    sup |x'(t)| <= (|D| + 2 epsilon)/h + A h/2.

This follows from the E002-640 sharp secant-to-velocity bound and the triangle inequality. Each term is independently tight in the absence of additional coupling assumptions. Endpoint errors can have opposite signs, so a nominally zero displacement is not a zero-speed observation.

For a **fixed measured displacement D=0**, the nuisance-only penalty B(h)=2 epsilon/h + A h/2 is minimized at h*=sqrt(4 epsilon/A), giving B*=2 sqrt(A epsilon) when A>0 and epsilon>0. This is a cadence-design tradeoff, **not** a universal optimum over arbitrary observed trajectories (D itself depends on h), nor a statistical human velocity guarantee. Dimensionless ratio q=A h²/(4 epsilon) yields B(h)/B*= (sqrt(q)+1/sqrt(q))/2. Faster sampling can worsen a worst-case velocity certificate because endpoint localization error is divided by a shorter time interval.

**Synthetic reproducibility:** `python research/observability/e002_641_cadence.py` (Python standard library only). For epsilon=0.05 mm, A=10,000 mm/s², D=0: continuous optimum ~4.472 ms, B*~44.721 mm/s; on an integer 1–20 ms grid, 4 ms yields 45 mm/s; 2 ms and 10 ms each yield 60 mm/s. Local execution passed all assertions. These numbers are illustrative, **not** measured eyelid parameters.

**Predeclared acquisition consequence:** For a future motorized-aperture reference, independently calibrate endpoint spatial error and continuous acceleration bounds before choosing reference cadence. Precompute the admissible velocity ceiling at each candidate cadence and freeze it before revealing closure labels. Treat exposure integration, clock uncertainty, rolling shutter, geometric distortion, missingness, blur, gaze and glasses as separate error terms or abstention triggers. Do not substitute frame-localization repeatability for a hard bound. If independent epsilon or A certification is unavailable, retain `ABSTAIN_UNCALIBRATED`.

**Falsification:** A continuous encoder/reference trajectory exceeding the certified bound under verified premises invalidates the calibration or mathematics. If candidate cadences fail the nuisance assumptions, do not optimize over them post hoc. Compare precommitted cadence selection against held-out motorized trials and human sequences only after independent calibration. Human closure sensitivity and fatigue claims remain unsupported.

**Current gate:** no physical acquisitions, no human rater pairs, no independently certified physiological acceleration. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
