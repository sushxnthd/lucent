# E002-118 frozen evaluation

Goal: independent Python replication of existing EyeDentify RGB/Tobii pilot on six previously evaluated participants, plus descriptive time-detrended and luminance-adjusted waveform checks. Same human cohort; not a new validation sample.

Data: participants 1,4,50,7,17,34, sessions 1 and 11, first 30 every-third CSV rows, left-eye 32x16 RGB. Reuse E002-112 estimator unchanged and compare all 12 sessions to published E002-112/114 numbers. Primary gate: >=11/12 sessions match frame count, both raw and normalized correlations within 0.002, tracker SD within 0.0005 mm. No retuning. Secondary: Pearson r, first-difference r, linearly detrended r, and detrended+luminance partial r; circular-shift null using shifts 5..n-5, no lag search. Participant is unit. Any new exploratory association is not proof of fatigue inference.

Preserve previous frozen failures. Do not distribute original participant images. Zero personal spend. E002-118 code and data not yet executed at protocol freeze.
