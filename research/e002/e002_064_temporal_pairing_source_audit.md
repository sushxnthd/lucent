# E002-064: EOTT timestamp pairing source audit (2026-10-10)

**Classification:** source-code measurement-pipeline defect, deterministic reproduction; not a human RGB/reference waveform score.

**Upstream:** Brown HCI WebGazer `www/data/src/webgazerExtractServer.py`, Git blob `20f88872f77e8d82361f8ab3598ec4bc7e9d7963`.

The upstream `writeDataToCSV` loop advances `tobiiListPos` while `frameTimeEpoch > tobiiList[pos].timestamp` and then compares `pos` with `pos+1`. For a frame strictly between two tracker samples, `pos` is the first **future** record. The code cannot choose the previous (possibly closer) sample. The comments also mention resetting `tobiiListPos` for out-of-order videos, but no per-video reset was found in the inspected source.

**Frozen before numerical execution:** SHA256 `be2daf0d820b6d48523afebe1d36f434b4cb2fdcfc2a40b165f8ba383f89aa29`.

Deterministic 5-second, 30-fps synthetic frame grids with a prespecified 2.1-ms phase offset:
| Reference | Published-style mean absolute timestamp error | True nearest |
| --- | ---: | ---: |
| 40 Hz | 14.567 ms | 6.256 ms |
| 120 Hz | 6.233 ms | 2.100 ms |

The published-style pairing disagreed with true nearest on 100/150 frames at 40 Hz and 150/150 at 120 Hz. These are **constructed** clock grids, not measured EOTT synchronization errors.

A constructed tracker gap [0,25,50,307875,307900] ms with a frame at 60 ms produced 307815 ms matching error under the published-style algorithm versus 10 ms under bracketing nearest. An out-of-order video construction produced 8015 ms versus 10 ms. These show *possible* failure modes, not that any released EOTT video experienced them.

Ten local unit tests and two independent exact-rational arithmetic checks passed. Official upstream documentation separately warns that WebM frame timestamps can repeat; actual participant-level prevalence remains unmeasured.

**Discovery V2:** KNOWN source-level forward matching defect; BELIEVED nearest bracketing + max-gap abstention should protect pairing; CONFLICTING nominal epoch overlap versus unverified frame timestamps; FALSIFIED source always chooses nearest; ANOMALOUS code comment about cursor reset without corresponding reset; UNTESTED real human waveform impact.

**Next:** bounded official-archive extraction of P_54 eligible RGB video and original tracker, independently verify PTS/session epochs, perform reference-blind pupil/iris segmentation, apply frozen E002-063 held-out gates. Preserve all PupilSense and earlier RGB negative results.

No five-second fatigue, sleepiness or alertness inference has been validated. No user laptop or personal spend used.
