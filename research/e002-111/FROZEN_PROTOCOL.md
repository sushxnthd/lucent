# E002-111: Original GP3 comparison MAT integrity and array-structure preflight
Date: 2026-10-11 UTC. Classification: CAPABILITY-BUILDING / DISCRIMINATION.
Source: public Zenodo 18429496, data.zip, member data/comparison/DATA_pupilSSVEP.mat.
Modality: MEYELens IR illuminated by GP3, NOT ordinary RGB. One human participant; no state labels.

## Hypothesis and prediction
If the E002-101 HDF5 root-name preflight reflects actual complete paired reference data, a fresh GitHub Actions runner can retrieve the original ZIP member, verify uncompressed size and CRC32, open the MATLAB v7.3 HDF5 payload, and identify nonempty, typed data reachable under GOGGLES, TIME, and GAZEPOINT_PUPIL.

## Frozen structural gates
1. HTTP 206 byte-range retrieval of exactly the previously reported 1,759,383,333 compressed bytes starting at ZIP offset 1,666,508, with local ZIP member header verified.
2. DEFLATE decompression yields exactly 1,841,799,077 bytes and matches central-directory CRC32.
3. HDF5 file opens with h5py; all five top-level keys GOGGLES, TIME, GAZEPOINT_PUPIL, GAZEPOINT_EYE_X, GAZEPOINT_EYE_Y are present.
4. At least one nonempty dataset reachable from GAZEPOINT_PUPIL and TIME (object references count only if their targets resolve). Report actual shape/dtype, not fabricated sample rates or values.
All four required for PASS; failures and unexpected schema are preserved. No model tuning or waveform scoring in this experiment.

## Confounds, competing explanations, uncertainty
Names alone may be empty placeholders, MATLAB object references, or summary-only data. Even if all gates pass, the reference is single-participant, IR-illuminated, not a smartphone RGB recording. No participant-held-out or fatigue inference is possible. Downloaded file integrity is member CRC32 only, not full ZIP MD5. Avoid dumping identifiable raw image pixels.

## Cheapest next discriminator
Once shape, timestamp units and reference signals are known, freeze a separate five-second GP3-versus-goggles waveform comparison (lag tolerance, correlation, amplitude fidelity, baseline and onset controls) before computing outcomes. Independently locate a public visible-light RGB + tracker pair for RGB-REFERENCE-OBSERVABILITY-002.
