# E002-577 | Frozen authentic-LPW acquisition and native-video decode probe

Date: 2026-11-01. Primary kernel: E002-371. This is the **first actual archive-access experiment** following E002-573–576 preparation. It is not a blink-validation experiment.

## Question and prospective decision

Can an ephemeral no-cost hosted runner access the original investigators' LPW archive, extract **one predetermined native video** without transferring the entire 2.4 GB ZIP, and decode real human eye-region frames? The primary source is https://datasets.d2.mpi-inf.mpg.de/tonsen/LPW.zip, linked from the Max Planck investigators' LPW page. The paper reports approximately 95 fps, but individual shutter timing is not certified.

Freeze before running:
1. Read remote HEAD Content-Length; request the ZIP tail and central directory with HTTP byte ranges. Require status 206 and exact Content-Range. **Never** fall back to downloading the full ZIP if byte ranges are ignored.
2. Reject ZIP64, encrypted entries, malformed offsets, unsupported compression, mismatched CRC, size amplification, and archive entries above 100 MiB compressed or 400 MiB uncompressed. Select the lexicographically first eligible video entry (.avi/.mp4/.mkv/.mov) in the central directory, without viewing content or using labels. If no eligible entry exists, record a bounded failure.
3. Fetch only that member's compressed byte interval, decompress in memory, verify CRC, write it to a temporary directory, and run ffprobe and ffmpeg on frames 0, 10 and 20. Print only source archive URL, selected member name, sizes, cryptographic video digest, native stream metadata, and whether three frames decode. Never print, upload, commit, cache, or publish human imagery, labels, or derived frame pixels. No GitHub Actions artifacts.
4. The run must complete within 12 minutes. A network/permission/range failure is an explicit acquisition negative result, **not** evidence about eyelid velocity, hidden closures, or dataset quality.

## Evidence gates

SUCCESS: authentic source-linked member bytes + CRC verified + native video decodes. This advances human-source acquisition only; human anatomical rater pairs remain zero, authenticated exposure/clock remains zero, and hidden-closure physical validation remains zero.

FAILURE: preserve failure class and any public nonidentifying transport facts; do not manufacture a success, infer physiology, or expand to an unfrozen dataset search. The next step is investigator-approved acquisition or independent consented physical capture.

The LPW dataset is for noncommercial scientific research. Keep raw recordings ephemeral and private. Its pupil-center labels are **not** closure labels. All Lucent physiological product outputs remain `ABSTAIN_UNCALIBRATED` and release remains `BLOCKED`.
