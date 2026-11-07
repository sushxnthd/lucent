# E002-483 FROZEN — complementary temporal gates as a falsification test for exposure aliasing

Date: 2026-10-27. Kernel: E002-371. Status: predictions frozen before implementation. Evidence tier: SYNTHETIC INSTRUMENT DESIGN ONLY. No human sequences or physical acquisitions.

## Question
E002-482 found two aperture trajectories with identical *full 20-ms scalar exposure means*, one closing completely and one never closing. Can two **independently timed complementary 10-ms temporal gates** distinguish these particular worlds even under adversarial channel gain, offset/noise, and clock error? This is a proposed laboratory instrument control, NOT a feature of a standard single-exposure phone camera.

## Frozen experiment
Reuse the unchanged E002-482 stationary and piecewise-linear moving worlds (baseline 1 mm; knots at 0,5,15,20 ms; +/-1 mm excursion; assumed peak speed 200 mm/s). A paired instrument measures the mean aperture in gates [s,s+10] and [s+10,s+20] ms, where s is the *common* gate timing error. All averages use exact piecewise-linear integration, not a camera image. Each channel j has independent unknown multiplicative gain g_j in [1-d,1+d] and additive offset plus measurement error e_j in [-q,q]. Observed scalar is y_j=g_j*m_j+e_j. Only consider positive observed channels. Contrast C=(y_1-y_2)/(y_1+y_2). Baseline d=0.10, q=0.03 mm-equivalent, with s in [-2,2] ms.

The **adversarial contrast interval** follows from monotonicity of C in positive y_1 and y_2: its lower endpoint uses y_1=(1-d)m_1-q and y_2=(1+d)m_2+q; its upper endpoint uses the opposite extremes. A pair of worlds is certified distinguishable by this observable only if their entire contrast intervals are disjoint for all allowed s. Otherwise record NOT_CERTIFIED; do not claim that the worlds are identical.

## Predeclared predictions and controls
1. At s=0, the stationary pair is (1,1) mm; moving pair (1.5,0.5) mm. Both full-exposure means remain 1 mm.
2. With d=.10 and q=.03, stationary contrast lies in [-.13,.13], while the moving-world lower contrast at s=0 is greater than .38.
3. The moving-world contrast remains separated from the stationary interval for all s in [-2,2] ms, but a +/-5-ms clock budget must not be declared safe without independent verification.
4. At s=0 with independent gains d=.30 and q=.03, contrast separation is lost (the moving lower endpoint is below the stationary upper endpoint).
5. A one-gate/full-exposure measurement cannot break the original E002-482 alias; a two-gate result is not interchangeable with a phone-camera output.
6. Missing gate, saturation, unbounded gain drift, unverified exposure timing, rolling-shutter row assignment, nonlinear image formation, blink geometry, blur, gaze or glasses => ABSTAIN_UNCALIBRATED for physical closure claims.

## Execution and falsification
Implement standard-library Node simulator, tests and deterministic JSON aggregate. Evaluate phase holdouts at -2,-1.5,-.5,.5,1.5,2 ms and a fine phase sweep, plus adversarial gain/noise endpoints. Use a separate independent arithmetic replay where possible. If any allowed baseline phase makes contrast intervals overlap, falsify prediction 3. If the gain-drift control unexpectedly remains certified, falsify prediction 4. Never infer a universal human eyelid speed limit or a physical shutter guarantee.

## Physical human study handoff
A future pilot needs independently calibrated dual temporal gates (or simultaneous independent reference sensors), externally timed shutter/row measurements and high-frame-rate >=400-fps anatomical eyelid reference. Obtain appropriate research ethics approval and consent, use adult volunteers, preregister participant-disjoint held-out nuisance conditions (brightness, gaze, glasses, geometry, blur, dropped frames, clock offsets), blind reference annotations and keep raw timing provenance. At least one credible reference closure under an EXCLUDED prediction is a falsification requiring model/assumption investigation. Finite human samples cannot certify a population-wide hard velocity cap. Physical claims remain ABSTAIN_UNCALIBRATED.