# RGB-REFERENCE-OBSERVABILITY-003: Native-Synchrony Dataset Triage

**Status:** research branch; no primary E002 outcome changed.

## Decision

The released EyeDentify derivative remains unsuitable as the reference waveform for RGB-REFERENCE-OBSERVABILITY-002 because its preprocessing converts Tobii timestamps to whole-second labels and averages three timestamp groups row-wise before pairing them with 30-fps webcam frames.

However, the **official EyeDentify repository confirms that the original collection retained the synchronization inputs**: each 3-second webcam recording has a timestamp file, the Tobii recording is retained at 90 Hz, and the upstream alignment code performs timestamp-window matching before frame extraction. Therefore the scientific blocker is not the original acquisition design; it is the released/preprocessed derivative.

Official collection details:
- webcam: 1280x720, 30 fps
- Tobii: 90 Hz
- 3-second recordings
- timestamp file per recording/session
- screen colors varied to evoke pupil responses
- official alignment code in `data_creation/eyedentify/tobii_and_webcam_data_alignment.py`

The correct next step is to determine whether the **raw public EyeDentify archive** still contains the timestamp CSVs, source Tobii CSVs, and 3-second videos. If so, rebuild synchronization directly from native timestamps and use only participant-held-out raw sessions for the frozen waveform test.

## Fresh public dataset search

### Strong but not exact matches

- **ON007537 / OpenNeuro ds007537, CC0:** 23 healthy adults; synchronized EEG, head-mounted eye tracking, PPG and GSR during smartphone interaction/video viewing. Useful for physiological/state context, but it does not provide ordinary RGB webcam video.
- **MCFW-Gaze:** 15 participants; continuous 120-Hz Tobii Pro Fusion pupil diameter, eye openness and gaze across controlled and natural web interaction. Useful as a high-quality reference target, but no ordinary RGB webcam stream.
- **LPW:** 66 high-speed eye-region videos from 22 participants across unconstrained illumination, glasses, contacts and makeup. Useful for pupil-segmentation robustness, but not the required ordinary-RGB + independent-reference pairing.
- **OpenEDS:** synchronized eye-facing camera imagery with pupil/iris/sclera annotations. Useful for anatomical-reference segmentation, but not the required phone/webcam + independent physiological reference.
- **HybridGaze (2026):** explicitly combines a standard RGB webcam with a Tobii tracker and synchronized gaze annotations. This is a promising new dataset lead, but the currently accessible publication description does not establish that native pupil-diameter labels are exposed, so it is not yet accepted as the E002 reference source.

## Required acceptance condition for a replacement dataset

A replacement source must expose:
1. ordinary visible-spectrum RGB video;
2. native frame timestamps;
3. independent pupil/physiological reference;
4. sufficient repeated stimulus variation;
5. legal public access;
6. participant-level held-out evaluation without calibration leakage.

No result is scored until all six are verified.

## Claim boundary

This triage does not establish RGB-phone observability or fatigue prediction. It exists to prevent the frozen E002 experiment from being evaluated against a temporally degraded reference.

The prior failed symmetric human-calibrated primary test, directional secondary result, and EyeLink-to-Pupil-Labs transfer remain frozen and unchanged.
