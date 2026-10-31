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

The authentic S01 [push run 40629467422](https://github.com/sushxnthd/lucent/actions/runs/40629467422) **completed successfully on 2026-10-28 at approximately 04:30 UTC**. It executed the frozen synthetic controls, downloaded and checksum-checked the S01 source, and uploaded an aggregate-only artifact. The exact downloaded ZIP SHA-256 `a425fc5f72a2a426d350d65b629e986aba4c380bdd8ad89add5ce1237ef3866a` matches the GitHub artifact digest. The parsed [aggregate JSON](E002_501_HOSTED_AGGREGATE.json) has exactly 2,399 windows in each of four conditions. The first PR-triggered run 40629473278 was cancelled; a later PR run 40629513457 was still pending at verification. Do not conflate that pending run with the verified successful push run.

### Prespecified authentic outcome: zero positive optical aliases

| Frozen condition | Nuisance abstentions / 2,399 | Endpoint different | No alias evidence | Image alias candidates |
| --- | ---: | ---: | ---: | ---: |
| Original S01 | 2,221 (92.58%) | 64 | 114 | **0** |
| Uniform brightness +8 | 2,221 (92.58%) | 64 | 114 | **0** |
| 3x3 blur | 2,182 (90.95%) | 89 | 128 | **0** |
| Alternating +/-1px horizontal jitter | **2,399 (100%)** | 0 | 0 | **0** |

All four conditions had zero image-alias candidates and zero all-condition survivors. In baseline, only 178/2,399 windows (7.42%) survived nuisance abstention, so the zero candidate count has **very low screening coverage**. Jitter drove abstention to 100%, an especially strong **coverage failure**. No positive event can be compared across conditions, so this does not measure candidate sensitivity or robustness. It does not establish absence of blink aliases in human video, much less absence of hidden eyelid closures.

**Prespecified decision:** This source and frozen detector yield **no positive optical-alias evidence**. Retire E002-501 as a candidate source for any product observable. Preserve the high abstention rates as a negative result, do not relax thresholds or optimize another optical proxy on S01. The next decisive experiment must involve real blinded anatomical annotations and authenticated camera/shutter timing, not more image-motion screening.

## Scientific interpretation and release

The observed zero image-alias count shows only that this prespecified optical threshold found none among 2,399 windows on one calibration participant, with 92.58% baseline abstention. It cannot exclude hidden blinks, establish physiological timing, or validate a physical observability boundary. Neither outcome validates E002-371's sharp physical shutter-gap/eyelid-velocity law.

There are still **zero independent anatomical ratings**, **zero authenticated camera clocks/shutters**, **zero certified human continuous-time velocity upper bounds**, and **zero held-out participant physical predictions**. No participant S21-S31 was used. E002-371 remains physically unvalidated. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.

**Next:** obtain two independent S01 anatomical review sheets plus physical clock/shutter calibration, then freeze participant-disjoint predictions. The E002-501 optical surrogate is closed with a negative/low-coverage result. Hush PR #45 remains untouched.
