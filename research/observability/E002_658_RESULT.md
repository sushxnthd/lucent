# E002-658 | Virtual pulse-phase shutter calibration and blind-phase failure

**Evidence tier:** deterministic exact-arithmetic synthetic instrument simulation; NOT physical shutter calibration, human validation, or independent replay.

## Frozen virtual design
Twenty midpoint temporal bins across a nominal 0.20-second exposure. Three normalized response kernels: rectangular, early-only (first five bins), and late-only (last five bins). A narrow virtual LED pulse is stepped over every bin and its integrated response measured without noise; phase response reconstructs bin masses. A held-out V-Lipschitz eyelid-aperture trajectory is evaluated at t=0: a(t)=0.20+4|t|, with closure threshold 0.28. This is a synthetic aperture coordinate, not a physiological blink.

## Results
The uniform kernel has dimensionless first absolute moment 0.25, exposure average 0.40, and correctly calibrated lower bound 0.20. Early-only and late-only kernels have moment 0.375 and exposure average 0.50. Incorrect rectangular calibration gives lower bound 0.30, falsely certifying the eye open at threshold 0.28, while phase-scan calibration gives 0.20 and abstains. If the scan covers only the first 15 phases, the late-only response yields zero observations over the scanned phases despite carrying all exposure mass in the omitted five bins: full support coverage is essential.

The exact-arithmetic script was executed locally and passed. No hosted CI or independent replay is claimed.

## Product consequence
A measured exposure duration alone is insufficient; a temporal impulse-response calibration must cover the full support, with a conservative uncertainty envelope for phase, exposure row, drift, pulse width, brightness response, and saturation. Absent this, use the worst-case temporal moment or ABSTAIN_UNCALIBRATED. Production BLOCKED.

## Physical falsification protocol
Use independently timed LED pulses and a photodiode/oscilloscope reference, scan the entire exposure and rolling-shutter row range, repeat at several brightnesses and exposure settings, reserve unseen pulse phases and widths, then compare predicted integration against measured frame pixel values. Predeclare a bound on moment estimation error before testing held-out human eyelid trajectories. Synthetic calibration is not evidence of actual camera response, and physical capture count remains zero.
