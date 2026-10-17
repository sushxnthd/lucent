# Failed scientific gate and infrastructure provenance
Run 39040920585 (commit bb5af56f10a38dbb54ca5ecd6da324f68811989c) failed at E002-262 mutation test, while original E002-220 download, CRC/SHA, counts, PTS and manifest steps passed.
The failure exposed a scientific design problem: two consecutive Tobii rows marked invalid are NOT a defensible blink proxy because original records include many invalid rows between ~25ms valid samples. The original 2-invalid-row gate is retired. This is not an ordinary CI-only failure.
Corrected prospective observable: gaps >=100ms between consecutive timestamps of the UNION of valid left and right reference samples; 150ms sensitivity. Even this only admits further RGB corroboration.
No original human waveform correlation or fatigue claim.
