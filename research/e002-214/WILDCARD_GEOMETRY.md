# E002-214 wildcard | Human-frame scale perturbation, third-party outputs
This is a 10%-effort **controlled serendipity** check of the same fixed PupilSense checkpoint on digitally rescaled real-human video frames. The input frame is held fixed; only a digital rescale from 0.6x to 1.6x varies. We independently recomputed per-frame extrema from 8 published third-party scale CSVs pinned to `aa9bddf498a3b6e4104c2c000d2cc0c06a816aae` and verified their Git blob hashes. We did **not** independently run the checkpoint or collect new human measurements.

Across **96 distinct original frames** and **864 rescaled model outputs** (nine scales each), **94/96** frames had a >0.25 mm change in at least one eye's prediction solely from rescaling; left 90/96 and right 73/96. The largest within-frame swings were **0.667861223 mm left** and **0.802765846 mm right**. This is a fixed-model geometry-nuisance failure, not a universal RGB impossibility. The 0.25 mm line is exploratory and is not the frozen waveform amplitude gate.

**SCIENCE:** The source model is not invariant to digital image scaling under a fixed anatomical pupil. Third-party analysis previously reported scale sensitivity; the contribution here is an independently checked paired-frame audit and pinned provenance, not novelty over CondadosAI.

**PRODUCT:** No uncalibrated mm reading from this checkpoint should be certified under uncontrolled distance. Lucent's relative pupil/iris observable and rejection on insufficient iris/pupil pixels are better-aligned candidates, but still require native-time paired human validation.

**Scope:** Human images originate in source clips, but only derived prediction CSVs were accessed. No RGB/tracker paired physiological waveform, device holdout or fatigue claim.
