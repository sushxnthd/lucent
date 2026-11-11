# E002-419 — verified sharp bounds for unresolved high-speed reference truth

**Date:** 2026-10-24. **Frozen before implementation:** commit `5fed1ec1d23ab31cb900da1c4cba9df05647f71e` (`E002_419_FROZEN.md`). **Evidence tier:** synthetic finite-set identification and adversarial software verification, **not** physical human aperture or camera/shutter validation.

## Executed result

The independent checker enumerated **every binary assignment** of unresolved reference states in **1,000 seeded synthetic cases** (up to ten unresolved certified windows per case). All 1,000 exactly matched the primary implementation's sharp finite-set lower and upper bounds. Ten malformed/forged-input controls were rejected. The zero-certificate case correctly returned undefined selective error, not zero. The CI release check independently verified that a conditional zero-error result under operator-declared negative labels **cannot** authorize a product claim.

**Final GitHub Actions result:** [E002-419 independent verification run 40105936011](https://github.com/sushxnthd/lucent/actions/runs/40105936011), **SUCCESS**, at commit `908b944b0325eceb133998979bd09a2ac61e60ae`.

For N ordinary-camera **research** certificates, F high-speed reference intervals with witnessed closure and U intervals with unresolved physical reference, the fraction of false no-hidden-closure certificates on that finite set is partially identified by:

\[
\frac{F}{N} \leq \mathrm{false\ certificate\ fraction} \leq \frac{F+U}{N},\quad N>0.
\]

The bounds are sharp under arbitrary completion of the unresolved labels, assuming the resolved reference classifications are correct. This is elementary partial identification, **not a new theorem or a confidence bound**. Reference-negative classifications are operator-supplied research inputs and are **not authenticated by this program**.

### Frozen falsification examples

| Synthetic fixture | Certificates | Witnessed failures | Unresolved certified | Sharp finite-set error interval |
|---|---:|---:|---:|---|
| Naive zero-observed-failure case | 20 | 0 | 15 | **[0%, 75%]** |
| Fully resolved case | 20 | 5 | 0 | **[25%, 25%]** |
| All-abstain product | 0 | 0 | 0 | **Undefined** |

In the fully resolved case, ten additional product abstentions remain in the **30-window coverage denominator**, yielding coverage 20/30; they do not dilute the error denominator of 20 certificates. Reference-unresolved windows are counted even if the product abstains.

## Scientific consequence

E002-416 showed that high-speed reference video can itself have hidden closures between frames. E002-419 makes the evaluation consequence enforceable: **unresolved reference intervals cannot be silently removed to manufacture a zero-error result**. Even if every *resolved* reference interval agrees with a no-hidden-closure certificate, the upper error bound can remain large.

This does not measure the prevalence of unresolved human intervals or establish E002-371's physiological speed bound. It provides a conservative scoring contract for the prospective two-rater E002-407/408 human study. A population-risk claim additionally requires participant-level sampling, independent physical reference authentication, prospective unseen-condition validation and statistical uncertainty accounting (E002-410/414). The finite-set upper bound is not a population upper confidence limit.

## Product consequence and remaining blockers

The executable research evaluator always returns `product_claim_authorized=false` and `product=ABSTAIN_UNCALIBRATED`, including when the conditional upper error bound is zero. No operator-provided provenance string can turn its research arithmetic into a physical certificate. No human rater sheets, calibrated shutter/clock, independently justified hard eyelid-velocity bound, or prospective unseen-device outcomes were obtained in this run.

**Next decisive step remains physical human data collection:** two independent E002-418-qualified raters, completed blinded E002-407 sheets, E002-408 adjudication, independently measured camera response and timing, and E002-416-qualified reference intervals. Only then can E002-419 report empirical bounds rather than synthetic fixtures. Do not resume tuning rejected optical proxies. Hush was not modified.

**Artifacts:** `e002_419_reference_partial_id.py`, `test_e002_419_reference_partial_id.py`, `.github/workflows/e002_419_reference_partial_id.yml`; no raw eye data, linkage or human rater sheets uploaded.
