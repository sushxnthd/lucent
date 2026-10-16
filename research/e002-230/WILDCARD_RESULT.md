# E002-230: original human RGB paired-eye confound
The E002-229 frozen source CSV SHA-256 is
`087ca1cf7ce8cc1e24d9652ae5faa6e6a783abcaff716683d353a5544884e6fb`.

Original source: E002-228 Actions run 38866995557, artifact 12031733076.
Two development participants, 30 original frames per participant, two eyes per frame.

Exploratory result (independently checked locally):
- P_33: 5/30 same-frame opposite-sign center/ring contrast pairs; global frame brightness range 0.5627 grayscale levels.
- P_54: 12/30 same-frame opposite-sign pairs; global frame brightness range 0.6576 levels; 12 and 11 within-eye contrast-sign transitions.
- The ring-minus-center difference is exactly invariant to a uniform additive brightness offset absent clipping. Therefore a shared additive offset alone cannot explain or correct the contrast-polarity disagreement.
- This is **not** evidence that pupil boundaries are unobservable. Iris texture, illumination gradients, occlusion and center placement remain plausible causes.
- P_54 camera PTS remains unsuitable for lag certification. No physiological pairing, pupil ground truth or fatigue inference.

SCIENCE: stronger same-frame photometric nuisance evidence, no waveform certification.
PRODUCT: do not introduce a hard positive-contrast admission gate or global-brightness-only rescue.
Scientific gates: human waveform, device holdout, independent exposure time mapping all NOT TESTED.
CI: upstream E002-228 passed; E002-230 new checker local pass and mutation rejection; remote checker not yet executed.
