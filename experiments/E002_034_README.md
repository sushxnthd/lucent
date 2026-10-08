# E002-034 research note

The code in `e002_034_identifiability.py` constructs two observationally identical five-second pupil/iris measurement traces under distinct camera-scale versus iris-segmentation-bias assumptions. The correct normalization decision differs between the two cases. This is an algebraic counterexample, not a human-data result.

A separate frozen synthetic experiment (8 regimes, 500 trials each) found that duplicate segmentation uncertainty selects normalization well when nuisance assumptions hold, but fails in shared photometric-bias regimes. No real RGB or fatigue-state validation is claimed. The full experiment package is distributed separately.

Next: obtain authorized synchronized ordinary RGB and independent pupil-reference recordings, preregister participant/device splits, and test waveform fidelity with lighting and motion negative controls. The previous PupilSense scale negative result is unchanged.