# E002-330 preserved failures
HUMAN_PAIRED_NATIVE_REFERENCE: NOT RUN.
UNSEEN_HUMAN_BOUNDARY: NOT RUN (synthetic frozen predictions only).
NOVELTY: FAIL (temporal-order ambiguity and elementary inequalities have prior art).
FULL_RGB_IN_VIVO_OCCUPANCY: NOT ESTABLISHED; fixed center, contrast, visibility and sensor linearity unverified.
ROLLING_SHUTTER: uniform-global-shutter proof not directly applicable.
DIFFERENTIAL_OCCLUSION: common-weight positive bound invalid if pupil/iris masks differ.
CLOCK_AND_EXPOSURE: NOT VERIFIED on human recordings.
GEOMETRY_ONLY: false pixel change under center motion, negative control PASS.
BRIGHTNESS_ONLY: true occupancy .5 -> naive .64 at gain .8, negative control PASS.
MISSINGNESS_ONLY: hidden half exposure gives identical visible measurement with different true mean, PASS.
TEMPORAL_SMOOTHNESS_ONLY: equal derivative energy/opposite phase remains exposure-identical, PASS.
REMOTE_CI: NOT VERIFIED. PRODUCT_FATIGUE: REJECTED.