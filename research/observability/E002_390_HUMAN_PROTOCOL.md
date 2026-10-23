# E002-390 prospective human validation — protocol, not performed

**Status:** acquisition plan only. No human participants, synchronized cameras, reference labels or physical calibration have been obtained.

## Target estimand
For each 30/60-Hz RGB recording interval, does a *physically calibrated* E002-371 no-hidden-threshold-crossing certificate exclude every real central-palpebral-aperture crossing below 0.2? Report (i) error among issued certificates, (ii) abstention rate, (iii) unresolved high-speed reference labels, (iv) stratified failures by device and nuisance, and (v) statistical vs deterministic meaning of the velocity envelope. Do not call a brief threshold crossing a full blink.

## Acquisition and independent calibration
- Feasibility: 12 adult volunteers, then preregistered 60-adult confirmatory cohort (20 calibration, 40 untouched test), recruited under appropriate consent/ethics procedures. No medical claims or induced hazardous fatigue.
- Acquire ordinary 30-Hz and 60-Hz RGB plus an independently timestamped high-speed reference, preferably >=1000 Hz with short exposure. A 600-Hz reference is an alternative only when its exposure/time uncertainty makes the relevant threshold events resolvable. Borrow shared equipment rather than assume hardware funding.
- Calibrate actual shutter opening/closing and intercamera offset with an independent pulsed-light target; record rolling-shutter row time, frame drops, VFR timing, optical blur and sensor saturation. Nominal FPS alone is insufficient.
- Obtain reference eyelid margin/aperture from two blinded annotators, including explicit uncertainty bands for landmarks and ambiguous partial closures. Do not infer ground truth from a single high-speed frame without exposure adequacy.
- Estimate velocity envelope on **calibration participants only** from high-speed aperture trajectories, with timing and landmark uncertainty. Report observed maxima and statistical extrapolation separately. A sample maximum is not a deterministic physiological upper bound. If no justified upper bound exists, hard certificates must abstain.
- Independently calibrate RGB transfer using intermediate apertures and exposure-integral forward modeling, not merely two-point open/closed RGB calibration.

## Frozen evaluation and nuisance controls
1. Freeze the threshold, allowable measurement error, timing envelope, reference adequacy, target intervals and certificate decision before opening test labels.
2. Predict which shutter gaps can conceal crossings under the independent speed envelope; test all phases on untouched participants and a camera model absent from calibration.
3. Compare circular self-calibrated velocity from ordinary RGB (negative-control baseline) against independent high-rate calibration; preserve failures.
4. Record glasses/no glasses, gaze eccentricity, illumination changes, exposure/gain drift, blur, geometry, rolling-shutter span, missing frames, and clock drift. Predeclare an abstention condition for every uncalibrated nuisance.
5. Evaluate true positives/negatives only when reference labels are adequate. Treat reference-ambiguous intervals as **unresolved**, never confirmed negatives.
6. Report exact binomial upper bounds for selective false-certificate risk among issued decisions. With zero failures, at least 299 independent issued decisions are needed for a one-sided 95% upper bound below 1%; participant clustering requires cluster-aware inference and may increase this number.
7. Secondary endpoints: bound tightness, issuance rate, prediction calibration on an unseen device, and robustness of complete-closure vs row-occlusion definitions. Report participant-level uncertainty and failure cases.

## Primary falsification
Any high-confidence reference-confirmed crossing in an interval for which Lucent issued a purported deterministic no-crossing certificate **and** all physical assumptions were independently verified falsifies the implementation or assumed envelope. A crossing under unverified assumptions demonstrates the necessity of abstention, not a theorem counterexample.

## Priority/availability audit (2026-10-23)
- Kwon et al., J R Soc Interface (2013), DOI 10.1098/rsif.2013.0227: 600-fps recordings from 25 adults and quantified eyelid speed; paper/figures available, but paired ordinary-RGB recordings not obtained.
- Espinosa et al., PLOS ONE (2018), DOI 10.1371/journal.pone.0196125: high-speed blink characterization; raw paired ordinary-RGB/reference material not obtained.
- OpenEDS (2019), arXiv:1905.03702: 200-Hz eye-facing VR sequences, access by request; not paired with an ordinary camera.
- LPW (2015), arXiv:1511.05768: about 95-fps eye videos with gaze/glasses variation; insufficient alone for sub-millisecond ground-truth labels.
- mEBAL2 (2024), BiDAlab/mEBAL2: 30-Hz multimodal RGB/NIR/EEG, useful for nuisance transfer but not a high-speed reference.

Do not treat any of these as completed Lucent human validation. The exact-shutter/velocity inequality is rooted in established Lipschitz/sampling mathematics; priority claims require comparison against primary literature and an independently demonstrated new empirical measurement result.
