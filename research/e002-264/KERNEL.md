# E002-264: single-chord projective ambiguity

Frozen question: can four RGB iris/pupil boundary crossings certify normalized pupil radius against synchronized same-eye Tobii diameter when pupil-center decentration is unknown?

SCIENCE: For iris crossings (-1,1), pupil crossings (d-r,d+r), q=((1-r)^2-d^2)/((1+r)^2-d^2). Centered inversion r_hat=(1-sqrt(q))/(1+sqrt(q)) is an upper bound on r. With independently established |d|<=D, the sharp lower bound is (1-D^2)/(A+sqrt(A^2-1+D^2)), where A=(1+q)/(1-q). Without D, compatible radii fill (0,r_hat].

Exact witness: projectivity h(x)=(x+1/4)/(1+x/4) sends centered r=7/20 to image quadruple (-1,-8/73,16/29,1), also explained by identity projection with r=700/2117, d=468/2117. Both q=169/729. Independent exact arithmetic checker passes.

PRODUCT: retire uncalibrated single-chord radius regression; keep conditional interval estimation only. Abstain if center displacement, boundary correspondence or optical assumptions are uncertified. Human waveform gates and five-second fatigue remain untested.

Prior art: Wang/Chern/Alexa 2019 arxiv:1902.04541 already recover projective radius for concentric circles. Pupil center displacement is documented in PMID 12091457 and PMC8516786. This is not claimed as novel projective geometry.

Active kernel: RGB cross-ratio waveform vs synchronized same-eye Tobii diameter; scalar geometric observability = interval width / upper bound; eventual held-out waveform Pearson lower bound. Strongest confounds: decentration, refraction, illumination, gaze. Falsification: identical images with different radii (achieved for one chord). Publishable physiological threshold: untouched human holdouts, nuisance controls, independent checker, mechanism prediction. Product threshold: certified interval tolerance and >=75% accurate admitted human windows. Kill: no independent decentration bound or repeated human failure.

Run: python research/e002-264/decentration_bound.py && python research/e002-264/independent_check.py
