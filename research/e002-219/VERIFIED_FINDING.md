# E002-219 verified finding (2026-10-15 UTC)
SCIENCE: Direct ZIP64 byte-range extraction succeeded. The source CSV SHA-256 is pinned in PROVENANCE_VERIFIED.json. Its 89 rows share one #timestamp, so this session has no per-frame native timestamp. This is not a human waveform validation. The source alignment implementation also averages three one-second tracker blocks; whether all released sessions use that exact revision is not proven.

PRODUCT: This sampled EyeDentify CSV is NOT an admissible native-time reference for five-second Lucent lag or waveform gates. Keep the release for static-image baseline comparisons, not physiological temporal certification. Switch primary paired-source search unless original Tobii/webcam time-series are recovered. No fatigue inference.

CI: successful run 38804885596. Initial run 38804663012 failed due missing ZIP64 parser; fixed in commit b1ca9129fcfdee29b93d0a75ccf84d0bbffb60fa. Dataset access was not the failure.
