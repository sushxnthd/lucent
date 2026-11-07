# E002-696 — Two-attempt public human-video suitability decision (2026-11-07 UTC)

**Tier:** source-screening result; no downloaded sequences, empirical measurements, or validation. **Decision:** no presently verified public source satisfies the frozen E002-690 deterministic-certificate acquisition contract. Do not repeat broad dataset discovery next run; proceed to physical acquisition or targeted access to OpenEDS.

## Attempt 1: high-rate candidates
- **OpenEDS** (Garbin et al., 2019; https://arxiv.org/abs/1905.03702): reported synchronized eye-facing cameras at **200 Hz**, 152 participants, and video-sequence subset. Strongest lead for a *conditional* human high-rate stress test, but access is on request and the paper abstract does not establish calibrated anatomical eyelid aperture in millimeters, exposure start/end timestamps, independently measured hard velocity ceiling, or camera-to-reference timing. **Candidate for exploratory human trajectories only; not certificate validation.**
- **SPEED** (University of Eastern Finland; https://sites.uef.fi/spectral/databases-software/speed-spectral-eye-video-database/): 180 spectral eye videos from 30 subjects; distribution under consideration, rate and timing/scale not independently established in reviewed description. **Not eligible.**

## Attempt 2: blink-specific alternatives
- **MPEblink** (Zeng et al., CVPR 2023; https://zenodo.org/records/7754768): downloadable 21.6 GB untrimmed in-the-wild blink detection corpus; original per-frame acquisition/exposure timestamps, reference aperture calibration and high-rate provenance not established. **Not eligible for deterministic exclusion validation.**
- **mEBAL2** (Daza et al.; https://github.com/BiDAlab/mEBAL2): large RGB/NIR and EEG-assisted annotated blink corpus, but access requires signed license and recorded cameras are ordinary-rate; labels are blink events, not independently calibrated high-rate aperture minima. **Not eligible.**
- **Eyeblink8 / ZJU**: literature describes 30 fps capture (https://www.mdpi.com/2078-2489/9/4/93); insufficient as independent high-rate reference. **Not eligible.**

## Frozen decision and next experimental action
The two bounded source attempts have been completed at **description/metadata screening**, not acquisition or raw-video audit. This does **not** establish that no suitable data exist anywhere. A high-rate video with a stated nominal fps alone cannot independently verify the E002-371 shutter-gap exclusion theorem. OpenEDS 200 Hz may be pursued for explicitly *exploratory* participant-disjoint falsification after lawful access, but must not be relabeled as anatomical reference truth without shutter, aperture and clock calibration.

**Next:** execute E002-690 synchronized mechanical occluder acquisition (30/60 fps phone, independent timed encoder/photodiode reference, synchronization pulse, measured exposure intervals), run the already frozen E002-695 prediction before inspecting reference labels, and preserve failures. If physical access is unavailable, record the acquisition blocker rather than create another synthetic theorem. No velocity ceiling from finite human video differences; no unconditional certificates. Product remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
