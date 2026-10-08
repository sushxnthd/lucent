# E002-035: Geometry-anchor consistency experiment

On 2026-10-08, an internally frozen eight-condition simulation was evaluated over 3,200 synthetic five-second sequences. The comparison used raw log pupil, pupil-minus-iris, and pupil-minus-geometry waveforms.

The geometry-anchor method reduced mean waveform RMSE from 0.05067 to 0.00846 in the iris-specific synthetic bias condition. Under simulated yaw corruption the opposite occurred: pupil-minus-iris RMSE was 0.00849 while geometry-anchor RMSE was 0.05071.

A fixed channel-disagreement gate rejected all 400 simulated yaw-corrupted recordings, including those with accurate pupil-minus-iris waveforms. In two other adversarial conditions it accepted all 800 recordings even though the accepted pupil-minus-iris error exceeded 0.03 in every trial. These are intentionally constructed simulation outcomes, not observed rates in humans.

Mathematical conclusion: disagreement between two waveform estimates lower-bounds the error of at least one estimate, but agreement cannot certify correctness if the estimates share bias. This follows from the triangle inequality and is not claimed as novel.

No real RGB videos, eye-tracker recordings, or fatigue labels were used. EVE human-data validation remains the decisive next test. The negative PupilSense geometry result from PR 22 is unchanged. Full reproducibility files are available in the E002-035 downloadable research package.