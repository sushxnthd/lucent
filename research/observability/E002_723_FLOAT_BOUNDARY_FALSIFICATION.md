# E002-723 — False exclusion from binary floating-point comparison

**Evidence tier:** source-level mathematical counterexample and fail-closed code correction; not physical or human validation.

## Falsifier

The earlier E002-716 replay parsed CSV decimal measurements into binary64 and evaluated `velocity_upper * delta_upper < aperture0_lower + aperture1_lower`. For the valid CSV strings `0.1, 0.2, 0.3, 1`, exact decimal arithmetic gives `0.3 < 0.3`, **false**. In Python binary64, however, `0.3 < 0.1 + 0.2` evaluates **true**, causing a spurious hidden-closure exclusion at the sharp equality boundary. The false exclusion is a direct software counterexample, independent of camera or physiological assumptions.

## Enforcement change

Parse finite, nonnegative decimal strings through `Decimal` into exact `Fraction` values before the strict certificate comparison. The evaluator now avoids binary64 conversion and finite decimal-context rounding, including products with extreme exponents. Invalid/nonfinite values remain rejected. Self-tests cover equality and a nearby valid strict exclusion; existing participant-disjoint and nuisance abstention checks remain.

## Limits and follow-up

This correction does not certify that input bounds are conservative, timestamps correspond to instantaneous aperture, or reference labels are correct. It does not create human evidence. Independently run the committed self-tests in hosted CI, audit untrusted-input resource exhaustion from extremely large decimal exponents, then perform the independently timed physical occluder acquisition under E002-714. Until then, `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
