# E002-479 protocol amendment A — pre-implementation geometric falsification

Date: 2026-10-27. This amendment is **after** the original freeze and **before** implementation. Preserve the original freeze; do not retroactively describe this as preregistered.

Independent exact interval arithmetic exposed a failure of the frozen assertion that the island at [2.020, 2.030] ms is invisible under ±0.004-ms phase uncertainty in *both* periods. At period T=1000/240 ms, the second-period island ends at 6.196666... ms, while a grid pulse starting at 6.200 ms could begin at 6.196 ms under the allowed phase error. The original robust-aliasing claim was therefore **falsified at design stage** (although nominal grid samples still miss the island).

Correct only the island phase and held-out probe, leaving all other parameters and predictions unchanged:
- Island: **[2.015, 2.025] ms modulo T**, width 0.010 ms.
- Held-out pulse start: **T*k + 2.017 ms** for k=0,1.
- At every original grid phase, the island is disjoint from the full possible pulse support [t-u,t+w+u], including both periods.
- Held-out ±0.002-ms jitter yields start in [2.015,2.019] ms and pulse end in [2.021,2.025] ms, fully inside the island.

The 0.036-ms per-cell uncovered-width calculation remains correct as a generic single-grid bound; it does not by itself guarantee that the *same* phase island avoids a second period with a noncommensurate phase grid. The experiment must explicitly test the joint two-period geometry. No physical observations or human evidence are involved.