# E002-726 | Actual capture timeline ingestion bridge

**Evidence tier:** executable acquisition bridge; no captured instrument or human observations.

The frozen E002-714/724 physical-occluder protocol needs independently timed camera and reference traces. This script ingests real ffprobe video-frame presentation timestamps and independently recorded binary reference samples, rejects malformed/nonmonotonic records, and reports exact decimal inter-frame gaps and reference sample transitions. It deliberately **does not** infer exposure start/end, synchronize two clocks, or treat a sampled transition as an exact event time. No certificate or calibration verdict is issued.

## Reproduction
```sh
ffprobe -v error -select_streams v:0 -show_frames -show_entries frame=best_effort_timestamp_time,pkt_duration_time -of json capture.mp4 > frames.json
python research/observability/e002_726_capture_alignment.py frames.json independent_reference.csv
```
Reference CSV columns: `time_s,closed` with independently clocked sampled 0/1 states. For a real experiment retain raw video, reference trace, acquisition device configuration, clock synchronization measurement, shutter/exposure characterization, source hashes, and blinded reference labels. Camera presentation timestamps are *not* shutter timestamps. Transitions are interval-censored by adjacent reference samples. This tool is a conservative ingestion checkpoint, not empirical validation.

**Next falsification:** acquire a synchronized LED/photodiode or physical occluder trace, independently bound clock offset and exposure intervals, then compare preregistered E002-371 predictions with held-out verified closure/no-closure trials. Until then product ABSTAIN_UNCALIBRATED / BLOCKED.
