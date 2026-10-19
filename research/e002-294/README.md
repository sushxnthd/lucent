# E002-294 — Sharp periodic hidden-dose observability boundary

This isolated Lucent research result bounds how much **anatomical eyelid closure** can remain invisible between finite RGB exposures when every observed frame is compatible with an open eye. It is theoretical/synthetic, not human-validated.

**Model:** periodic c(t) in [0,1], |c'|<=V, exposure T, gap G, calibrated f(c)=c^p (p>=1), y_n=T^-1 integral_exposure f(c)dt+e_n, |e_n|<=eta. The null is c=0.

**Sharp theorem:** r=min(1,2eta), M_p(x)=2[x^(p+1)-(x-VT/2)_+^(p+1)]/[(p+1)VT], x*=sup{x in [0,1]:M_p(x)<=r}. Maximum hidden gap dose U=int_0^G min(1,x*+V min(t,G-t))dt; hidden peak <=min(1,x*+VG/2). Both ceilings are attained by explicit periodic waveforms that produce exactly the same measured features as an open eye.

**Illustrative V=20/s, eta=.025, T=1/60s:** 30fps half shutter linear U/P=10.62%; 10Hz retaining 60fps exposures 45.48%; quadratic 30fps 19.25%; quadratic 10Hz 58.95%. Synthetic worst-case ceilings, NOT empirical error rates.

**Verification:** 11 quadrature comparisons, 100 independent LP comparisons, two exact rational observational collisions, three mutation checks; all passed locally. No ordinary-RGB human validation. Prior optimal recovery and low-fps blink literature constrain novelty.

**PRODUCT:** Reject uncalibrated no-blink, pupil-waveform and fatigue certification. Conditional upper-bound reporting may be investigated after independent radiometric, exposure and eyelid-velocity calibration. No deployment authorized.

See THEOREM.md, PROTOCOL.md, experiment.py, independent_checker.py, results.json, verification.json, PRODUCT.md, FAILED_GATES.md.