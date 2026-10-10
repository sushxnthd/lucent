# E002-075 — Original-RGB adjudication of MEYELens mask/flag anomalies (FROZEN PROTOCOL)

Date: 2026-10-10. Class: DISCRIMINATION with CAPABILITY-BUILDING and separate SURPRISE exploration. Freeze BEFORE accessing the original JPEG pixels in this experiment.

## Context and non-negotiable claim boundaries
E002-074 found two records with eye=0, empty green eye-region masks and positive red pupil masks; and two different records with 99 and 223 red pixels outside green. These are **preselected anomalies**, NOT a prevalence sample, not independent participants, and not an RGB/Tobii waveform study. Preserve all earlier negatives. Do not infer any five-second fatigue validity.

## Frozen inputs
Anomalous eye=0 records:
- eye 15_frame_000053_pic_1192
- eye 17_frame_000054_pic_1541
Anomalous pupil-outside-green records:
- eye_frame_000070_pic_4305
- eye 12_frame_000046_pic_580
Control image from same series as first eye=0:
- eye 15_frame_000088_pic_1227
Controls are for visual comparison only, not statistical inference.

## Hypotheses
H1: The eye=0 pupil-positive records could be independent mask/flag semantics rather than absent RGB eye anatomy. If the original JPEG still contains an identifiable eye/pupil, it weakens an interpretation of eye=0 as "no pupil visible".
H2: The pupil-outside-green pixels could be near-boundary registration differences rather than a wholesale mask displacement. E002-074 already found dilation radii 4-5 pixels resolve the errors; original RGB alignment can discriminate gross mismatch from small boundary differences.

## Prespecified metrics/gates
G1 (integrity): retrieve original JPEG+PNG by exact matching ZIP stems; verify RGB 640x480; verify red/green area equals E002-074 for all available pairs. PASS only if all five are fetched and decoded; otherwise PARTIAL.
G2 (image evidence): compute mean grayscale in red pupil mask, in green-only visible eye mask (if nonempty), and in a 6px annulus around the red mask excluding red; compute pupil-minus-annulus contrast. This is an exploratory *photometric proxy*, not an anatomical truth gate. No sign threshold is allowed to prove visibility.
G3 (geometry): quantify pupil-outside-green pixel distances (nearest green pixel, distance quantiles) for the two noncontainment records; compare to 4-5px dilation prediction. PASS only if the original mask data independently reproduce 99 and 223 outside pixels and all are within 5px of green.
G4 (visual): create source JPEG/mask overlays for manual adjudication; label 'ambiguous' if eye anatomy cannot be distinguished. No claim of mask correctness from contrast alone.

## Anti-leakage, uncertainty and anomaly protocol
Do not tune thresholds to outcomes. If retrieval or decompression fails, record it. If G1/G3 fail, anomaly-mine wrong channel interpretation, ZIP member mismatch, resampling, and distance metric differences before abandoning. No person-held-out, device-held-out or independent annotation validity claims. Record alternative mechanisms (eyelid, eyelashes, shadows, color, annotation semantics). Reserve unplanned probes as explicitly exploratory. Report no novelty in pupil masks or normalization.
