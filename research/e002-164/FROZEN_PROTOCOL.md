# E002-164 — frozen source-to-label lineage and temporal-alias audit
Date: 2026-10-13. Status: pre-outcome; zero-spend source audit and deterministic tests.

## One active kernel
Question: can an ordinary-RGB 3–5 s pupil waveform be validated against a concurrent independently timed pupil-diameter reference, or does the available EyeDentify session_data.csv destroy the required temporal identity?
Signal/reference: webcam RGB-derived temporal pupil observable (ultimately pupil/full-anatomical-iris log ratio) versus true tracker pupil diameter at matching exposure times; the immediate audit compares webcam frame ordinal to processed Tobii session_data.csv labels.
Frontier: E002-112/114 reported failed RGB/Tobii waveform gates on EyeDentify; E002-162 established non-invertibility of the documented 3-group averaging source, but did not verify released CSV lineage. E002-132 also evaluated left/right temporal agreement using processed session_data.csv.
Scalar observability: frequency-specific gain |H(f)| for the three-second group fold, plus actual released-CSV timestamp uniqueness ratio if data can be obtained. Ultimate frozen Pearson/lag/amplitude/NRMSE/coverage gates unchanged.
Strongest confound: tracker time folding, second-precision timestamp grouping, video-frame/label index substitution, and camera exposure timing; independently, lighting and eye geometry.
Decisive falsification: original per-sample tracker timestamps and frame-matched physiological labels shown for released CSV (source path not applied), or valid untouched paired human waveforms pass original gates against genuinely synchronous data.
Publishable threshold: source-provenance chain + actual CSV confirmation + independently verified exact null modes, plus untouched RGB/reference heldout validation for physiological claim. An exact source-law alone is a measurement-integrity result, not a novel physiological theorem.
Product threshold: demonstrably correct eligibility/rejection of temporal references; recover usable coarse session means only if count and missingness assumptions verified.
Kill: stop EyeDentify as temporal waveform reference after two failed data-path attempts or confirmed folding; switch source. Never retune human gates to rescue a corrupted reference.

## Predefined source audit
Pin upstream blob `f46d7ae369a62596f7044ca647d361c38fcb16ea` for `data_creation/eyedentify/tobii_and_webcam_data_alignment.py`, and runner blob `a4952e047c69f101a4ad581a1f0a8ff0c3055893` for `run_data_alignment.py`, identical across `vijulshah/eyedentify` and `vijulshah/webcam-based-pupil-diameter-estimation`.
Check that runner calls `algin_data`; implementation selects three second-rounded timestamp groups, concatenates same ordinal positions, row-averages left_pupil/right_pupil/pupil_diameter, writes identical first timestamp to all output rows, appends video frame_path by ordinal index, and writes `session_data.csv`. Distinguish **code path** from **provenance of released Kaggle bytes**.

## Frozen mathematical tests (assume 90 tracker samples/s and 30 RGB frames/s, each three seconds)
Define y[i]=(x[i]+x[i+90]+x[i+180])/3 for i=0..89. For continuous x(t)=a+bt, x[k]=a+b*k/90 and webcam frame t=i/30: y[i]=a+b*(1+i/90). Thus fitted slope per webcam second is b/3 (not b), despite Pearson=+1 for monotone noiseless ramps. For x(t)=sin(2*pi*f*t), transfer across one-second segments H(f)=(1+e^(2*pi*i*f)+e^(4*pi*i*f))/3. H(f)=0 at f=k+1/3 or k+2/3 Hz; output may be identically zero even for a real pupil oscillation. This is a model-free exact aliasing statement for the stated operator, not proof of human physiology.

## Frozen gates
G0 upstream source blob IDs and output lineage independently verified.
G1 exact linear-ramp slope compression b/3 at 30 fps within 1e-12; Pearson still +1.
G2 f=1/3 and f=2/3 Hz cancellation max abs(y)<=1e-12 on 270 samples.
G3 two distinct source sequences, including opposing trends, yield identical 90-vector.
G4 actual Kaggle CSV check: >=1 unmodified `session_data.csv`, report SHA256, row count, unique #timestamp count, whether all rows share one timestamp, and source URL; **NOT_EVALUABLE** if inaccessible. This is supporting evidence, not cryptographic lineage proof.
G5 E002-112/114/115/132 interpretation audit; never present their processed-label temporal correlations as valid physiological waveform tests without raw-tracker lineage.
G6 untouched RGB/tracker five-second evaluation NOT RUN.

## 10% wildcard
Check if session-level arithmetic mean survives the fold exactly for equal-length groups; report missing/unequal-group failure mode. Do not change active kernel.

## SCIENCE and PRODUCT
SCIENCE: determine exactly what the published conversion destroys and what remains unknowable about released file provenance.
PRODUCT: fail closed on temporal reference eligibility, preserve potentially usable session-level mean only when verified, switch to true synchronized tracker capture; no fatigue inference.
