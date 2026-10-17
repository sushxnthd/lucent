# E002-267 — Active measurement kernel (frozen)

**Question:** Can synchronized ordinary visible RGB yield a geometry/photometry-normalized pupil/iris temporal waveform that survives participant, device, lighting, and glasses holdouts?

**Exact signal/reference:** RGB pupil/iris ratio (candidate full-conic) versus independent same-eye native-time eye-tracker pupil diameter in mm, with exposure timestamps independently certified.

**Frontier:** EyeDentify temporal folding unsuitable for native waveform certification (E002-259/260); EOTT blink-validity clock rejected for two human windows (E002-262); EVE Basler visible-color 60Hz + Tobii is a synchronized positive-control candidate, access pending. E002-265/266 optical ambiguities were synthetic only.

**Scalar observability:** participant-bootstrap 95% lower bound on held-out within-session zero-lag r, plus five-second per-window r >= .75, lag <= 67ms, amplitude ratio .75..1.25, NRMSE <= .70; >=80% valid pairs, ref SD >= .10mm. Only training-fitted affine gain. Prospectively added: RGB r exceeds best brightness/geometry/iris/half-window-shift control by >= .10.

**Strongest confounds:** brightness/auto-exposure contour bias, gaze-dependent corneal magnification, pose, clock offset and reference interpolation.

**Decisive falsification:** untouched human windows fail frozen waveform/nuisance gates or cannot reach meaningful admitted coverage.

**Publishable success:** >=8 untouched participants, independent raw provenance, checker, nuisance controls, unseen mechanism prediction, relevant device/lighting/glasses holdouts, explicit limitations/prior-art audit.

**Product threshold:** >=75% accurate admitted human windows, >=50% admission coverage (new prospective threshold), and participant/device/lighting/glasses holdouts; EVE Basler-only result is not consumer-device certification.

**Kill:** after two blocked dataset attempts switch paths; after three nondiscriminating runs reformulate; reject pupil waveform direction if no calibrated optical bounds or useful admitted coverage. No fatigue claim.
