# E002-210 — EVE pupil-label and timebase source audit (2026-10-15)

## Active question
Ordinary RGB pupil-to-anatomical-iris temporal waveform vs independently synchronized same-eye tracker pupil diameter (mm). Frontier: EyeDentify processed labels have temporal limitations; MCFW-Gaze has no verified paired RGB in inspected archive; EVE documents paired webcam videos and pupil-mm labels, but only Basler is stated reliably synchronized. Scalar: held-out participant-bootstrap lower Pearson bound, frozen r>0.30 and >0.10 above nuisance, lag<=100ms, amplitude 0.5–1.5, NRMSE<=0.75. Strongest confounds: brightness boundary drift, gaze projection, blur, clock offset. Falsification: prospective participant/device/lighting/glasses holdouts fail frozen waveform and nuisance gates. Publishable: >=8 untouched paired participants, independent checker, prior-art audit and unseen mechanism prediction. Product: >=75% prospective coverage with calibrated rejection. Kill/reformulate: prospective waveform failure or 3 nondiscriminating primary runs.

## SCIENCE ledger
Primary source: https://github.com/swook/EVE/blob/master/DATASET.md (Git blob 9b04b892e248c2030168c627357e4cb66c87104a). EVE documents 54 participants (39/5/10), four camera streams basler/webcam_l/webcam_c/webcam_r, per-camera MP4 and timestamps and HDF left_p/right_p pupil diameters in mm with validity. Crucially: only basler-to-tracker synchronization is stated reliable; webcam timestamps from Video4Linux may be imprecise. Public documentation provides no numeric webcam clock error bound. HDF field description does not establish native tracker timebase preservation. Dataset access is by request; none obtained this run.

Elementary exact clock-gauge result, NOT a novel physiological theorem: if observed waveform y(s)=p(s-tau+delta), shifting tau and delta together leaves the data unchanged. Physiological lag and clock offset are not separately identifiable from the waveform alone. With apparent lag ell=tau+delta and independent bound |delta|<=e, the sharp true-lag interval is [ell-e,ell+e]. A frozen lag threshold T can be certified for all admissible offsets iff |ell|+e<=T. Unbounded e means no lag certificate, regardless of observed waveform correlation. For a unit-amplitude sinusoid f Hz, sharp worst-case pointwise error from |delta|<=e seconds is 2 sin(min(pi*f*e,pi/2)); at 2 Hz and 100 ms this is 1.17557 amplitudes. This is worst-case synthetic mathematics, NOT measured human error.

Executable tests enumerate integer-ms offsets and independently verify the sinusoid chord geometry; corrupted-result control must fail. No human waveform was evaluated. Prior-art positioning: clock-gauge symmetry is elementary measurement science; no novelty or RGB impossibility claim.

## PRODUCT ledger
EVE is a conditional better source for paired RGB and pupil-mm than MCFW-Gaze. Basler may serve as a timing-anchored control, but is NOT proof of ordinary webcam performance. EVE webcams require an independently justified clock-error envelope before lag certification. Never infer offset by maximizing correlation with the pupil reference being evaluated: that leaks target lag. If e unknown, fail closed. Do not change frozen waveform gates.

Prospective sequence: (1) obtain access legally; hash subset and inspect native tracker timing/label generation; (2) freeze participants/devices/lighting/glasses; (3) use Basler for timing control only; (4) estimate webcam clock offset via independent shared motion or hardware event; (5) apply exact lag certificate and untouched waveform/nuisance gates; (6) report all failures and >=75% coverage honestly.

Wildcard (unexecuted): compare clock drift among webcam_l/c/r using shared motion, without pupil outcomes.

## Failed gates and CI
EVE human waveform: NOT RUN (access not obtained). Webcam clock lag certificate: FAIL-CLOSED (no numeric offset bound in public docs). Native tracker label timebase: UNVERIFIED. Independent local checker: PASS. Actions: NOT VERIFIED at publication. Smallest supported claim: EVE documents webcam+pupil-mm pairs but cannot certify <=100ms webcam physiological lag from public timing provenance alone.
