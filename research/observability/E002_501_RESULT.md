# E002-501 | Authentic human-video temporal image-alias falsifier

Date: 2026-10-28. Frozen protocol: [E002_501_FROZEN.md](E002_501_FROZEN.md). **This experiment does not infer anatomical eyelid closure.**

## Why this is different from earlier experiments

E002-482/484 established *synthetic* shutter and exposure aliases. E002-493 falsified the E002-491 motion-event selector under registration jitter and temporal subsampling on 20 S01 clips. E002-501 tests a distinct, falsifiable prediction on **all first 12,000 S01 native image frames**: whether a five-native-frame sampling gap can hide a reversible **image-content** excursion between nearly identical surrogate endpoint images, and whether any such cases survive adversarial brightness, blur and one-pixel registration jitter. It does not reintroduce the rejected E002-491 event detector as a blink detector.

## Frozen procedure and negative-control repair

- Checksum-pinned source: S01.zip from [Guttmann-Flury et al.](https://zenodo.org/records/18970793), expected MD5 `fb56109542a13aa7879778833fe4cbaa`. Native 320x288 video is downscaled with the previously used FFmpeg area filter to 64x64 grayscale. Use 2,399 overlapping six-frame windows, step five frames, corresponding to **nominal** 150-to-30-fps instantaneous-sample surrogates, not calibrated 30-fps exposure images.
- Four unchanged condition thresholds: original, +8 brightness, 3x3 blur and alternating +/-1px jitter. Publish counts only, never images, per-window indices or traces. Classify every window as nuisance abstention, endpoint-different, image-alias candidate or no image-alias evidence.
- **Documented pre-authentic-data correction:** the first local synthetic central-pulse test failed because global-mean photometric correction subtracted some of the actual central signal, making a false border nuisance. Before any authentic S01 run or GitHub commit, photometric correction was changed to use border means; the global mean remains a nuisance veto. No outcome-dependent threshold retuning occurred.
- **13/13 synthetic adversarial tests passed locally** after that correction, covering reversible pulse, monotone change, exact duplicates, global brightness, border nuisance, actual blur/jitter transforms, input validation, and hard product abstention. These are local synthetic results, not human evidence.

## Execution and evidence tier

[Executable](e002_501_temporal_alias.py) · [Synthetic tests](test_e002_501_temporal_alias.py) · [Hosted workflow](../../.github/workflows/e002_501_temporal_alias.yml).

The authentic S01 hosted experiment was launched by commit `21234eb40cdc8fba86c73e41f4bb68f27a090ee7`. [Push run 40629467422](https://github.com/sushxnthd/lucent/actions/runs/40629467422) and [PR run 40629473278](https://github.com/sushxnthd/lucent/actions/runs/40629473278) were **queued/pending at the time of this report**. Authentic alias counts, hosted test success and any nuisance-survivor finding are **not yet verified**. The workflow publishes only an aggregate JSON, which must be inspected and persisted after success; failure must be reported honestly.

## Scientific interpretation and release

A positive image-alias count would demonstrate only reversible optical image variation between sparse *frame-sample surrogates* in this single calibration participant. A zero count would show only that the prespecified optical threshold found none, not that hidden blinks are absent. Neither outcome validates E002-371's sharp physical shutter-gap/eyelid-velocity law.

There are still **zero independent anatomical ratings**, **zero authenticated camera clocks/shutters**, **zero certified human continuous-time velocity upper bounds**, and **zero held-out participant physical predictions**. No participant S21-S31 was used. E002-371 remains physically unvalidated. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.

**Next:** verify the hosted authentic aggregate, then stop optical proxy iteration and obtain two independent S01 anatomical review sheets plus physical clock/shutter calibration. Hush PR #45 remains untouched.
