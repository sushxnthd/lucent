# E002-484 amendment A: general threshold correction (before implementation)

The frozen protocol's general iff formula omitted the first-gate overlap condition. It is correct for the frozen numerical regime (delta=0.10, q=0.03) but **not for all** delta<1.

For epsilon>0, gate 1 imposes epsilon <= (6 delta + 4q)/(1+delta); gate 2 imposes epsilon <= (2 delta + 4q)/(1-delta). The correct necessary and sufficient criterion for an identical raw two-gate observation vector is

epsilon <= min[(6 delta+4q)/(1+delta), (2 delta+4q)/(1-delta)]

with delta in [0,1), q>=0, and positive signal ranges. The second gate controls when delta=0 or 2 delta + 2q <=1; otherwise the first gate may control. The frozen positive and negative predictions at delta=.10,q=.03 and delta=0,q=.03 are unchanged. The original erroneous general claim remains visible in E002_484_FROZEN.md for auditability.

Independently derived before writing simulator/test implementation.
