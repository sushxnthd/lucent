# E002-441 — first successfully acquired human high-speed video (2026-10-25)

**Evidence tier:** real human-video acquisition and codec inspection only. **E002-371 physical validation: FAIL / not yet tested.** Published S19 archive was obtained and inspected by GitHub Actions on [run 40199794338](https://github.com/sushxnthd/lucent/actions/runs/40199794338) after fixing the prior runner's missing FFmpeg dependency.

## Reproducible observed result
- Archive: 373,146,176 bytes; published MD5 `8a16cf12526f7558b4e49926c4bc5e8e` matched exactly; 8 archive members.
- One Phantom AVI was found and **two real human-video frames were successfully decoded**, with distinct frame hashes. This is not synthetic-fixture output.
- AVI: MPEG-4, 320×288 pixels, 56,911 declared frames.
- **Unexpected timebase:** both `r_frame_rate` and `avg_frame_rate` are **1/1 fps**, `time_base=1/1`, with `duration=56,911 seconds`, whereas the dataset description advertises approximately **500-fps acquisition**. The 1-fps stream clock therefore cannot be assumed to represent physical shutter time; the original 500-fps claim cannot yet be verified from the AVI itself.
- One synchronization CSV has 8 columns including `Time`, `PhanTime`, `RelTime`, `RecordingTimestamp`, `LocalTimeStamp`, and `Blinks`. One Phantom XML file was present with root `chd`. **No synchronization data rows or anatomical eyelid apertures were examined in E002-441.**
- Hosted acquisition and fixture tests completed successfully. Nonidentifying metadata aggregate: [workflow artifact](https://github.com/sushxnthd/lucent/actions/runs/40199794338/artifacts/12601077933).

## Falsification and product consequence
This directly refutes the shortcut *'native AVI frame-rate metadata is a trustworthy physical clock'* for this particular published high-speed dataset. It does **not** refute the dataset's nominal acquisition-rate claim, since a postprocessing/export operation may have changed its stream timebase. It does not show a human hidden closure, estimate a speed bound, or validate E002-371.

**Next experiment E002-442:** preregistered reconciliation of S19's independent synchronization table against the 56,911-frame video, without releasing private timestamps. The protocol was frozen before examining any sync data rows. Holdouts S21/S22 remain sealed. A passing candidate-clock check still cannot authenticate shutter exposure.

Product remains `ABSTAIN_UNCALIBRATED` for no-hidden-closure, blink duration, PERCLOS, and fatigue. No physical deployment claim is justified.
