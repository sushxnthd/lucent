# E002-628 | Human reference-data acquisition decision (2026-11-03 UTC)

## Decision
Two targeted source checks located **Silesian5** (100 fps, 5 subjects, ~300 blinks) and **OpenEDS** (200 Hz, 152 participants, eye-facing VR cameras). Neither currently qualifies as an independently calibrated reference for the E002-371 continuous-time no-hidden-closure certificate. Do not relabel frame-rate metadata as shutter/exposure calibration or sampled finite differences as continuous-time velocity bounds.

## Sources and limitations
- Silesian5: https://www.blinkingmatters.com/research — states Basler 100 fps, 640x480, five participants and 300 blinks, with converted videos obtainable only through a signed-license permission process. It explicitly notes annotation imprecision and lost trailing frames from codec conversion. Original camera exposure windows, shutter mode, clock uncertainty and independently certified velocity/acceleration ceilings are not supplied there. **Status: candidate for coarse held-out event analysis only; access not established.**
- OpenEDS: https://arxiv.org/abs/1905.03702 — reports 200 Hz synchronized eye-facing cameras and 152 participants; 91,200 frames in video sequences. Download is upon request. The abstract does not establish actual exposure intervals, continuous-time closure ground truth, or independent acceleration envelopes. **Status: candidate for anatomical/segmentation nuisance tests, not a physical theorem validation by itself.**
- mEBAL: https://github.com/BiDAlab/mEBAL — explicitly describes 30 Hz RealSense acquisition, unsuitable as a higher-rate independent reference. Access requires a signed license.
- Ordinary 25–30 fps blink datasets do not resolve subframe closure.

## Frozen validation decision before any access
1. Separate participant identities into calibration and sealed held-out groups before estimating any bound.
2. Require original timestamp/exposure metadata, not container fps alone; measure actual light-sensitive exposure intervals and synchronization error on a timing target.
3. Independently estimate aperture geometry error and a continuous-time dynamical envelope, with explicit epistemic status. A sample maximum is never a certified envelope.
4. On held-out sequences, preregister gap-by-gap **EXCLUDE** versus **ABSTAIN** using only calibrated low-rate observations. A ground-truth closure in any EXCLUDE gap is a hard falsification of the *combined* certificate assumptions. Count abstentions and exclusions separately; never interpret abstention as correct blink detection.
5. Stratify by gaze, glasses, lighting, motion blur, missing frames, rolling shutter and synchronization uncertainty. Refuse claims outside measured nuisance envelopes.
6. If neither dataset supplies calibrated exposure/velocity evidence, execute the existing motorized-aperture timing experiment and preregister a prospective synchronized human study. Do not manufacture physiological numbers.

## Evidence tier and product consequence
**External source triage only; no human sequences downloaded or evaluated.** This targeted source check adds concrete candidate frame rates, access restrictions and annotation caveats, but does not validate E002-371. Keep `ABSTAIN_UNCALIBRATED` and production `BLOCKED`. The next scientific run must acquire genuinely new physical/human measurements or run a calibrated instrument experiment, rather than another literature-only or theorem-polishing pass.
