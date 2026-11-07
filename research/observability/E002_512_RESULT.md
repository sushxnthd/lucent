# E002-512 | Rolling-shutter scanline drift reverses a conditional exclusion

Date: 2026-10-29. Primary E002-371 workstream, existing branch and draft PR #26. [Frozen protocol](E002_512_FROZEN.md) committed as `23bb6d4` before executable implementation. Evidence tier: **synthetic affine single-scanline timing falsification**, not human anatomical data, physical shutter measurement, or a new theorem.

## Scientific finding

The existing E002-373 sharp scalar exposure theorem assumes that two exposure means refer to one common latent normalized aperture and that their actual blind gap is known. For an affine rolling shutter with line delay `ell`, a tracked single sensor row moving from `row_1` to `row_2` between frames changes that gap:

`H = P - w + ell*(row_2-row_1)` for top-to-bottom readout. With `u` independently bounded rows of localization error on **each** frame and independent relative clock-gap error `j`, use `H_max = P-w + ell*(row_2-row_1+2u)+j` and reject any case with `H_min < 0`. Reverse the signed drift for bottom-to-top readout. A multirow aggregate, unknown scan direction, nonlinear readout, or a changed anatomical scanline is **outside this model**, not evidence of exclusion.

For `P=1/30 s`, `w=10 ms`, `V=60/s`, `b=0.999 +/- 0.001`, `theta=0.2`, and **hypothetical** `ell=100 microseconds/row`:

| Second row relative to first | Conservative row error | Risk upper | Conditional scalar decision |
| --- | ---: | ---: | --- |
| 0 | 0 | 0.748989795 | Exclusion within stipulated model |
| +10 | 0 | 0.778989795 | Exclusion within stipulated model |
| +20 | 0 | 0.808989795 | Not excluded |
| +10 | +/-5 each | 0.808989795 | Not excluded |

The crossing occurs at ~17.0034 rows of positive displacement, equivalent to the previously established E002-505 critical **1.70034 ms** additional blind gap. The new information is the **rolling-shutter row-displacement mechanism**: correct nominal FPS and exposure length do not determine the exposure gap of a moving tracked scanline. This is a restricted nuisance-model consequence, not a new physiological law or a measured camera specification.

## Falsification and verification

- [Executable](e002_512_rolling_scanline.py), commit `ce54ebb`: high-precision decimal model, strict domain checks, both scan directions, row uncertainty, overlap refusal, explicit non-certification flags.
- [14 frozen adversarial tests](test_e002_512_rolling_scanline.py), commit `e741956`: reversal, sign, row uncertainty, monotonicity, boundary, unknown readout, multirow geometry, out-of-sensor coordinates, nonfinite parameters and product blocking. **All 14 passed locally**, Python 3.11.
- Independent Node.js calculation, not importing the Python model, reproduced 0/10/20-row risk values and ~17.0034-row crossing locally.
- [GitHub Actions workflow](../../.github/workflows/e002_512_rolling_scanline.yml), commit `46d8444`, [run 40756428360](https://github.com/sushxnthd/lucent/actions/runs/40756428360) **queued at report creation**. Hosted pass must be verified separately.
- E002-511 previous [prepatch](https://github.com/sushxnthd/lucent/actions/runs/40750100688) and [postpatch](https://github.com/sushxnthd/lucent/actions/runs/40750208798) runs both **completed successfully**. That closes the conditional denominator software falsification, not physiology.

## Product consequence and physical next test

A product cannot infer a shutter gap from frame rate and exposure duration alone on a rolling-shutter camera. A conditional single-scanline exclusion additionally requires independently measured line delay and direction, native sensor row mapping, conservative localization error, and proof that both exposure means observe the same normalized aperture trajectory. If the actual image pipeline uses a multirow landmark/RGB aggregate, **do not apply this single-scanline formula**; require a validated forward model or abstain. Even all those instrument calibrations cannot substitute for a certified continuous-time human eyelid-speed envelope.

Next decisive evidence remains (1) two real independent blinded S01 anatomical ratings using the already frozen local packet, and (2) a **physical** rolling-shutter/exposure calibration with independently timed optical pulses across known sensor rows, including clock uncertainty, followed by participant-disjoint high-rate human reference predictions. Do not infer physical readout timing from AVI nominal FPS, rehost claims, or image motion. The S01 metadata-only track is closed.

**Human anatomical ratings 0; authenticated physical shutter/line clock 0; certified continuous-time human speed envelope 0; held-out physical predictions 0.** Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. This synthetic nuisance result does not satisfy the world-class completion gate. Hush remains separate and untouched.

## Hosted verification resolution (2026-10-29)

The previously queued [E002-512 GitHub Actions run 40756495779](https://github.com/sushxnthd/lucent/actions/runs/40756495779) completed with GitHub conclusion `success` on branch head `9413dc71cb9ceb2e4f601e59572f8f5289746bf0`. This independently executes the committed Python regression workflow in GitHub Actions; it does **not** independently measure camera line timing, human anatomy, or eyelid velocity. The four hypothetical risk values and the 17.0034-row crossing remain conditional synthetic model calculations. No further E002-512 numerical tuning is warranted without externally authenticated optical acquisition. Continue the already frozen dual-rater S01 pilot and physical shutter/line-clock protocol. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
