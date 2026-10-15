# E002-206 — Source-verified pupil-reference ceiling (15 October 2026)

**One active question:** Can the prospectively selected 15 original-human, five-second same-eye tracker windows satisfy Lucent's 75% accepted-coverage product requirement, with >=570 valid samples per 600-sample window and <=26-ms complete temporal gaps? This is a reference-only necessary condition of the unchanged RGB pupil/iris waveform versus synchronized tracker pupil diameter kernel.

## SCIENCE ledger
The original-human E002-204 Actions run 38695030636 (15 October 2026) downloaded the published MD5-verified MCFW-Gaze archive and established **30/30** exact matches between source trial-validity counts and original pupil_valid counts, **30/30** matches for pupil_valid AND finite positive pupil diameter, and **27/30** mismatches for the separately named pupil_available field. This resolves the earlier semantic ambiguity for these 30 eye/trial records only.

Using the frozen `research/e002-203/selected_trial_marginals.csv` (Git blob `ffad6b33fce22aa31633055c2af7042d4855a0a6`), any 600-sample subwindow has at most the whole-trial number of valid pupil samples. Requiring >=570 valid samples gives sharp marginal upper bounds: left 11/15, right 10/15, oracle choice of one fixed eye per trial 11/15, simultaneous binocular 10/15. The 75% participant-window threshold requires ceil(0.75*15)=**12/15**. Thus **no fixed-eye-per-window selection rule can pass the 75% gate on this selected 15-trial cohort**, regardless of temporal gap positions. These are sharp upper bounds from counts, not measured actual acceptance.

Proof: For any trial and eye, valid(window) <= valid(full trial). Thus a trial whose full-trial count is <570 can never contribute a passing 600-sample window. Enumerate the 15 count pairs; at most 11 have max(left,right)>=570. Even an oracle selecting the better fixed eye cannot reach 12.

## PRODUCT ledger
**Kill the 15 selected image_01_1 trials as a product-coverage certification cohort** under this gate; retain them for reference-integrity and failure-boundary characterization. Do not relax the 75% requirement or select only favorable participants. A new cohort with sufficient pupil reference coverage is needed for product coverage. Do not interpret reference failure as RGB failure.

## Frozen primary kernel / limits
Primary signal/reference: geometry- and photometry-normalized ordinary RGB anatomical pupil/iris waveform versus native-time independently synchronized same-eye tracker diameter. Primary scalar: held-out participant-bootstrap 95% lower Pearson correlation, with frozen lag/amplitude/NRMSE/nuisance and coverage gates. Confounds: illumination, blur, gaze, synchronization. Publishable success: >=8 untouched paired participants, participant/device/lighting/glasses holdouts, independent checker and mechanism prediction. Kill/reformulate after prospective waveform failure or 3 nondiscriminating primary runs. No end-to-end fatigue inference.

This is elementary finite-count arithmetic, not a novel physiological theorem. Actual original-human temporal gate results are separately executing in E002-206 Actions. A ~10% wildcard from E002-204 is the `pupil_available` flag disagreement; it is not used as a replacement validity signal. Source: https://zenodo.org/records/20300972. Exact executable marginal test: `research/e002-206/marginal_bound.py`.
