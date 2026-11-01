# E002-597 | Authentic LPW development-image nuisance falsification instrument

Date: 2026-11-02. Primary E002-371 kernel. [Protocol frozen before source execution](E002_597_FROZEN.md) at commit `0227b2b`. This is a real-human-source *instrument and prospective analysis*, not a completed anatomical experiment.

## Scientific question and necessary stability gate

Two deliberately nonanatomical image proxies, a fixed dark-pixel fraction and vertical-edge energy in the central image region, are tested against frozen brightness, gamma, blur, ROI translation and opaque-occlusion perturbations. For each of 10 source-bound 19-frame development clips, a perturbation is considered dominant when its absolute proxy change at a frame exceeds that clip's entire native temporal proxy range. A proxy fails the necessary nuisance-stability gate if any perturbation dominates more than 19/190 frames. All perturbations and the decision rule were fixed before inspecting real-image results.

This attacks the unjustified step from 'an image observable varies with time' to 'that observable measures eyelid aperture'. Even a stability pass is **not** anatomical validity, and nuisance failure is not a claim that a blink occurred.

## New reproducible artifact

- [Source-bound experiment](e002_597_source_nuisance.py) reuses E002-578's authenticated 95-fps LPW development participant-1 video, SHA-256, deterministic windows and private reviewer packet. It processes 190 decoded native images, reports only aggregate nuisance counts and proxy summary statistics, and destroys video, frames and owner mapping before exiting.
- [Independent stdlib oracle](e002_597_independent_oracle.py) checks the two image metrics against the separate numpy/Pillow implementation on four frozen grayscale arrays and rejects malformed arrays.
- [Dedicated hosted workflow](../../.github/workflows/e002_597_source_nuisance.yml) runs synthetic controls, independent replay, authentic-source experiment and cleanup with dependencies installed in an isolated temporary virtual environment.
- Source acquisition, frame count, geometry, provenance and independent replay are hard CI gates. A negative scientific finding does not fail CI.

## Evidence status at commit time

The protocol, executable, independent oracle and hosted workflow have been committed to `research/observability-human-boundary`. The latest dedicated [hosted run](https://github.com/sushxnthd/lucent/actions/runs/41353572997) was **queued** at the last inspection. Therefore **no authentic-source nuisance outcome, dominance count, or hosted success is claimed in this report**. The small-array formulas and blur-direction sanity check were checked locally in an isolated scratch calculation; this is not a full script execution or real-image result.

No human anatomical labels, independent rater pairs, physical shutter/clock certificates, hard continuous-time human eyelid velocity ceilings, or participant-disjoint held-out physical predictions have been added. Source images must not be exposed through CI logs or public artifacts.

## Next decisive step

Read the exact hosted run's status and aggregate stdout. If it fails, repair reproducibility or source acquisition before pursuing new science. If it succeeds, report every nuisance/proxy outcome, retain failures, and prohibit any uncalibrated proxy from closure certification. Then advance actual independent blinded anatomical labeling and synchronized physical-camera exposure calibration; repeated proxy testing cannot substitute for those steps.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. **Draft PR #26:** open/unmerged. **Hush PR #45:** unchanged.
