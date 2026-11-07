# E002-524 | Frozen high-speed reference witness observability experiment

Date: 2026-10-29. Primary E002-371 kernel; existing `research/observability-human-boundary` and draft PR #26. This protocol is committed **before** the executable, adversarial tests, numerical results or CI. Evidence tier: exact instrument-sampling mathematics and prospective study design only, **not human data**.

## Question and predeclared failure mode

E002-519/520 use a fully contained, independently adjudicated reference-camera closure witness to falsify an ordinary-camera hidden-closure exclusion. How short a *continuous, real* closure can a high-speed camera guarantee to capture as a wholly contained exposure, regardless of acquisition phase? This is a reference **witness sensitivity** limit, not a method for certifying the absence of a blink.

Model a single fixed reference pixel/scanline as periodically exposed on intervals `[phi+kP,phi+kP+e]` for all integer k, with `0<e<P` and unknown phase `phi in [0,P)`. A continuous anatomical closure is `C=[0,d]`. Positive overlap means intersection of positive duration; a strict full witness means one reference exposure lies **strictly inside** C, not merely touching its boundary. No frame interpolation, proxy classification or assumed universal human velocity bound.

## Frozen sharp predictions

1. A positive overlap is guaranteed for **every** phase iff `d>P-e`. At `d<=P-e`, construct a phase whose blind gap contains the entire event.
2. A **strict fully contained exposure** is guaranteed for every phase iff `d>P+e`. At `d<=P+e`, construct a phase with no strict full witness. Merely detecting overlap does not prove closure in the reference image.
3. If independent calibration expands each reference exposure's possible start/end by at most `u` on each side, the robust strict-full-witness guarantee becomes `d>P+e+2u`, provided the same exposure index and periodic clock structure are independently attested. The robust no-overlap counterexample remains possible for `d<=P-e+2u` when endpoints may move adversarially within their envelopes; report uncertainty rather than treating these two conditions as a full characterization of image observability.
4. If native frames can be missing, use the **largest verified consecutive start-time gap** `G`, not nominal P. The robust full-witness sufficient condition is `d>G+e_max+2u`; absent native-index/clock provenance, abstain.
5. Dimensionless ratios: `eta=d/P`, `rho=e/P`, `xi=u/P`. Ideal overlap boundary `eta>1-rho`; ideal strict full witness `eta>1+rho`; robust full witness `eta>1+rho+2xi`.

## Frozen numeric cases (hypothetical, not camera measurements)

- 240 Hz reference, 1-ms exposure: P=25/6 ms, blind gap=19/6 ms, strict full-witness guarantee requires d>31/6 ms.
- Same with u=1/10 ms each endpoint: robust strict full witness requires d>161/30 ms.
- 1000 Hz, 0.5-ms exposure: ideal strict full witness requires d>1.5 ms.
- One missing frame at 240 Hz: G=25/3 ms, ideal strict full witness requires d>28/3 ms.

## Frozen adversarial controls

Implement exact rational arithmetic. For each case, construct explicit adversarial phase at and just below each ideal boundary; verify positive-overlap versus strict-full-witness are distinct. Independently replay with another language or implementation. Reject zero/negative/overlong exposure, invalid uncertainty, missing native-index provenance, unknown exposure width, and an unjustified hard closure-duration premise. Run tests for missing frames and boundary equality. No stochastic sweep, no AI-generated anatomical labels, no nominal-FPS-as-clock substitution.

## Direct physical study and product consequences

- In an eight-person pilot, independently measure **native frame start times**, shutter duration, clock uncertainty, exposure integration and rolling-shutter row; preregister the smallest reference closure duration for which the instrument has a guaranteed full-witness opportunity. This does **not** guarantee that human anatomy can be classified; geometry, blur, brightness, gaze, glasses and independent raters remain separate gates.
- Predeclare ordinary-camera EXCLUDE/ABSTAIN predictions before reference anatomy. A valid contained, cross-camera-calibrated closure witness falsifies a particular exclusion. An open or censored reference sequence **never** verifies absence of a hidden blink.
- If no physical calibration or two independent blinded human raters exist, no operational reference sensitivity or human E002-371 validation is claimed. Keep `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
- This is elementary sampling geometry, not a new general theorem or clinical claim. No further S01 metadata archaeology or synthetic shutter-response sweeps.
