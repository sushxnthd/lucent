# E002-263 — Geometry-only observability kernel (isolated, non-human)
Date: 2026-10-17. Inherits frozen E002-261 human protocol unchanged.

**One active question:** Can an image-space pupil/iris observable remove planar projective camera/gaze distortion *exactly*, and does it outperform naive span ratio under boundary localization noise without making a false human-physiology claim?

**Signal/reference pair:** Four ordered RGB iris/pupil boundary crossings on a *corresponding true diameter* versus the latent physical pupil/iris radius ratio r/R in an ideal concentric, coplanar planar-iris model. The eventual human pair remains RGB normalized pupil/iris waveform versus independently synchronized same-eye Tobii pupil diameter.

**Frontier:** Pupil foreshortening and corneal refraction are established confounds (Aguirre 2019; gaze-angle-dependency work 2021); projective cross-ratio invariance is classical mathematics. EVE Basler has documented synchronization but restricted data access; no human validation here.

**Scalar observability:** geometry-only absolute radius-ratio error under perspective parameter k, and 4000-trial RMSE under independent 0.5 px endpoint noise at fixed 120 px iris span. E002-261 prospective human scalar remains within-session r with frozen lag/amplitude/NRMSE gates.

**Strongest confound:** pupil/iris boundaries are not necessarily one common physical plane or centered; entrance-pupil corneal refraction, gaze-dependent nonprojective distortion, partial occlusion, segmentation and incorrect radial correspondence break the theorem.

**Decisive falsification:** If cross-ratio estimate varies under *exact* projective warp of four collinear corresponding points, reject theorem/implementation. If it fails against nonprojective/offset/occluded human conditions or cannot beat brightness/geometry controls, reject deployable observable.

**Publishable threshold:** not met by synthetic classical invariant; requires untouched synchronized human waveforms, participant/device/lighting/glasses holdouts, independent checker, and mechanism-derived unseen prediction. No novel theorem claim.

**Product threshold:** cross-ratio candidate may enter the prospective EVE baseline only if four boundaries and diameter correspondence can be reliably estimated; eventual >=75% accurate accepted windows under frozen E002-261 human gates.

**Kill condition:** no valid four-boundary correspondence in consumer RGB or real physiology violates model enough to lose advantage; three nondiscriminating human experiments kill/reformulate. Do not advance to fatigue inference.
