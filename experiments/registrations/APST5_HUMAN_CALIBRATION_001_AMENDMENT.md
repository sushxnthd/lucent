# APST5-HUMAN-CALIBRATION-001 Data-Structure Amendment

**Status:** frozen after archive/schema inspection and before any probe-ranking outcome is computed.

## Why this amendment exists

The initial preregistration was written from the associated paper description, which refers to repeated illuminance-task sessions.

The public Zenodo archive itself contains **one luminance recording per subject**:

- one `AOB_UW_pupil_XX_sn2.mat`;
- one `AOB_UW_cogent_XX_sn2.mat`;
- approximately 288 s per available luminance recording;
- 24 five-second disc trials separated by five-second returns to the gray background;
- six presentations of each of four disc luminance levels;
- 23 subject IDs in the archive;
- subject 06 luminance pupil data are explicitly missing due technical failure.

The archive README describes the dataset as 23 healthy controls; the lesion participant is not represented as an additional public subject ID.

Therefore the original session-1–3 fit / session-4–5 validation plan cannot be executed from the released archive.

This amendment changes only the within-person fit-validation split. The participant-level design/test split, probe space, H1/H2 criteria, and claim boundary remain unchanged.

## Frozen within-person fit/validation split

For each subject with valid luminance pupil data:

1. identify the 24 non-background disc trials chronologically;
2. group trials by the four disc stimulus levels;
3. within each stimulus level, sort by chronological trial index;
4. use the **first three** presentations of that level for dynamic-parameter fitting;
5. use the **last three** presentations of that level for held-out waveform validation.

Thus each subject contributes:

- 12 balanced fit trials;
- 12 balanced held-out validation trials.

Both disc onset and return-to-background portions remain inside each 10-second trial waveform.

After held-out waveform metrics are frozen, refit the same five-parameter model on all 24 trials for the participant-level probe-design population.

## Event mapping

The released pupil file supplies an event-marker channel, and the matching Cogent file supplies stimulus type.

The analysis must derive marker/stimulus mapping from the released files and document it before optimization.

No event code may be relabeled based on observed pupil responses.

## Missing subject

Subject 06 is excluded because the archive explicitly lacks the luminance pupil file.

No other subject may be excluded because their fitted dynamics are inconvenient or reduce the probe advantage.

## Updated interpretation of waveform validation

Because validation is now trial-held-out rather than session-held-out, held-out (R^2) tests interpolation across repeated controlled luminance trials within one recording session.

It does **not** establish across-day or across-session stability.

That limitation must be stated with any positive probe-design result.
