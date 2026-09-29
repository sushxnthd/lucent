# Experiment Preregistration Template

Copy this file into `experiments/registrations/<experiment-id>.md` before running a confirmatory experiment.

## Identity

- Experiment ID:
- Date frozen:
- Commit SHA:
- Investigator:
- Exploratory or confirmatory:

## Question

**Primary question:**

**Primary hypothesis:**

**Null / failure interpretation:**

## Population

- Intended population:
- Inclusion criteria:
- Exclusion criteria:
- Minimum usable sessions per participant:
- Recruitment / sampling method:

## Collection protocol

- Video duration:
- Device constraints:
- Video-to-reference timing window:
- Reference measurement:
- Context variables recorded:

## Primary target

- Variable:
- Transformation:
- Person-centering / normalization:
- Missing-data handling:

## Split

- Unit held out:
- Split-generation rule:
- Random seed:
- Any stratification:

No participant or source recording may cross the final train/test boundary.

## Baselines

List all baselines that must be evaluated before the proposed model.

1.
2.
3.

## Model-selection rule

Specify what can be tuned and which data may be used for tuning.

## Primary metric

- Metric:
- Direction of improvement:
- Confidence interval method:

## Secondary metrics

-

## Planned ablations

-

## Success criterion

State the minimum result that would count as support **before** looking at the final holdout.

## Kill criterion

State the result that would cause the current hypothesis or model direction to be abandoned or narrowed.

## Deviations

Any deviation after this document is frozen must be appended here with a reason and treated as exploratory.
