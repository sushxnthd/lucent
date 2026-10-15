# E002-219 three-session provenance gate — 2026-10-15 UTC

SCIENCE: Direct byte-range extraction from the author-linked ZIP succeeded for three different participant/session paths. Each CRC-verified CSV has exactly one distinct #timestamp across respectively 89, 83, and 89 rows. Member SHA-256s and the GitHub-generated Actions artifact SHA-256 are pinned in MULTI_VERIFIED.json. This demonstrates loss of native per-frame timestamps in these released processed CSVs, not loss of all physiological information or universal RGB nonobservability. It corroborates, but does not prove every distributed CSV shares, the documented time-folding implementation.

PRODUCT: Do not admit these processed CSVs as native-time ground truth for five-second lag, NRMSE, or waveform correlation. They may support static-image baselines. The primary dataset path must switch to original paired recordings with independently verified timestamps. No APST-5 or fatigue claim.

CI: run 38805040718 succeeded. ZIP64 parsing failure in run 38804663012 was infrastructure and repaired. No human RGB waveform gate has been tested.
