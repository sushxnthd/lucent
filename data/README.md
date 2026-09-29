# Data Contract

No participant data is stored in this repository.

This directory documents how a Lucent dataset should be structured so experiments can be reproduced without leaking identity or session information.

## Proposed observation schema

| Field | Type | Purpose |
| --- | --- | --- |
| `participant_id` | string | grouping for subject-held-out splits |
| `session_id` | string | prevent same-session leakage |
| `clip_id` | string | unique observation identifier |
| `captured_at` | timestamp | temporal analysis |
| `device_family` | categorical | robustness / device holdout |
| `video_path` | path | local or controlled-storage reference |
| `pvt_median_rt_ms` | float | behavioral target |
| `pvt_lapse_count` | integer | optional vigilance target |
| `sleepiness_score` | float | subjective state target |
| `sleep_duration_h` | float | non-visual baseline |
| `time_awake_h` | float | context baseline |
| `quality_flags` | object | blur, face visibility, occlusion, etc. |

Exact fields may change with the protocol.

## Split safety

A valid final split must satisfy:

```
participants(train) ∩ participants(test) = ∅
source_recordings(train) ∩ source_recordings(test) = ∅
```

For session-specific experiments, session separation is additionally enforced.

## Privacy principles

- collect the minimum metadata required to answer the research question;
- separate participant identity from research identifiers;
- do not commit raw face video to Git;
- document retention and deletion rules for each collection;
- make dataset access explicit rather than accidental;
- publish derived / anonymized artifacts only when their privacy properties are understood.

## Data quality

Each clip should carry machine-readable quality information rather than being silently discarded. This makes exclusion analysis possible and helps detect whether a model works only under unusually clean conditions.
