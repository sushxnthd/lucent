# Research Roadmap

Lucent is staged so that each phase can kill or narrow the hypothesis before more complexity is added.

## Phase 0: validation architecture

**Status: active / foundation complete**

- [x] define falsifiable thesis;
- [x] define participant-held-out evaluation as primary;
- [x] define baseline ladder;
- [x] define leakage / shortcut threat model;
- [x] add reproducible split utilities;
- [x] add synthetic leakage demonstration;
- [x] add preregistration template;
- [ ] lock first paired-data protocol.

**Exit criterion:** a study can be run without making analysis decisions after seeing the final holdout.

## Phase 1: paired pilot

Collect repeated short video + reference measurements from a small cohort.

Primary questions:

- Are labels and capture timings reliable?
- Is there measurable within-person variation?
- Do simple features move with the targets at all?
- Which confounds dominate?

**Exit criterion:** pipeline integrity and at least one target worth carrying forward.

## Phase 2: unseen-person test

Scale collection enough to make participant-held-out evaluation meaningful.

Primary questions:

- Does video add signal beyond time and sleep history?
- How large is the random-split inflation?
- Does temporal information beat a matched static frame?

**Kill condition:** no useful signal after participant holdout and baseline control.

## Phase 3: robustness

Stress the surviving signal across:

- sessions;
- devices;
- lighting;
- viewing distance;
- glasses / occlusion;
- compression.

**Exit criterion:** identify a clearly bounded operating regime where the signal remains useful.

## Phase 4: fresh-cohort replication

Freeze:

- preprocessing;
- model-selection rule;
- primary target;
- primary metric;
- exclusion rules.

Then collect a new cohort and evaluate once.

**Exit criterion:** independent replication of the central effect.

## Phase 5: productization

Only after replication:

- choose the narrowest reliable state variable;
- design the minimum-friction interaction around it;
- determine whether personalization materially improves value;
- validate real-world usefulness separately from model accuracy.

Lucent does not need to predict "everything." A narrow, robust signal is more valuable than a broad, fragile one.
