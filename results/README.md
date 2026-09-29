# Results

Lucent does not currently publish a validated headline performance claim.

That is intentional.

Results belong here only when they can be tied to:

- a committed dataset version or collection ID;
- a frozen split definition;
- a committed experiment configuration;
- explicit baselines;
- participant-held-out evaluation where applicable;
- confidence intervals or uncertainty;
- known deviations from the preregistered plan.

## Result card template

Each result should report:

| Field | Value |
| --- | --- |
| Experiment ID | |
| Commit | |
| Dataset / cohort | |
| Participants | |
| Primary target | |
| Split | |
| Baselines | |
| Primary metric | |
| Confidence interval | |
| Distribution shifts tested | |
| Preregistered? | |
| Replicated? | |

## Negative results

Null and negative results should be kept.

A model that fails only after participant holdout may reveal identity leakage. A temporal model that fails to beat a static frame may falsify the temporal hypothesis. A model that fails under a new device may identify an operating-boundary problem.

Those are scientific outputs, not repository clutter.
