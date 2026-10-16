# E002-242: retrospective resolution-stratified inference repair
Primary signal/reference (still untested): normalized RGB pupil/iris temporal waveform vs independently synchronized native-time same-eye Tobii pupil diameter.
This audit: synthetic RGB estimated pupil radius vs known rendered radius in E002-240 (no human data).
Frontier: E002-240 synthetic falsification; E002-241 pooled within-condition exact binomial intervals did not condition on fixed four iris-radius strata.
Scalar: 16-cell maximum simultaneous 95% one-sided correct-and-admitted pair fraction upper bound; human primary remains participant-bootstrap Pearson lower bound with lag, amplitude and NRMSE gates.
Confound: iris texture/glints dominating pupil edge; human gaze, lighting, exposure clock remain unresolved.
Falsification: any cell upper >=0.75 prevents a resolution-uniform synthetic rejection. Publishable success requires >=8 untouched synchronized human participants, holdouts, independent checking, mechanism prediction and prior-art audit; not met.
Product threshold: >=75% correctly accepted human waveform windows; synthetic pair acceptance cannot certify humans.
Kill: retire these two heuristics; switch blocked data path after two attempts; reformulate after three nondiscriminating primary runs.
Method: 2 conditions x 2 gates x 4 fixed radii, n=15 each. One-sided Clopper-Pearson alpha=.05/16 per cell; union bound yields simultaneous >=95% under within-cell iid synthetic-generator assumption. Seeds are deterministic and results do not generalize to humans. Conservative Hoeffding bounds allowing independent nonidentical Bernoulli outcomes also support the conclusion (max 0.291094 across 4 condition/gate tests).
SCIENCE: maximum simultaneous upper 0.5805954507, below .75; fixes E002-241 inference specification, not a universal RGB impossibility theorem.
PRODUCT: even 28px iris radius/56px diameter fails the tested texture-confound screen. Pixel resolution alone does not certify measurement. Keep both gates retired, pursue human contour truth and synchronized waveform.
