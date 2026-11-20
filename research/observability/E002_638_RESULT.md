# E002-638: Independent interval-reachability verification (synthetic)

Date: 2026-11-03 UTC. Kernel: E002-371 shutter-gap / bounded eyelid velocity.

An independently written exact-Fraction interval-feasibility oracle checks whether a threshold-crossing time can lie in both the forward reachable interval from the first open endpoint and the backward reachable interval from the second. This formulation is independent of E002-637's triangular-witness constructor.

Local execution of the new algorithm on the frozen 990 admissible parameter combinations returned **595 strict exclusions**, **395 reachable closures**, **44 exact equalities**, and **zero disagreements** with the analytical minimum-time criterion. All equalities remain reachable, not excluded. A threshold-monotonicity adversarial check passed for each case. The script is `e002_638_independent_boundary.py`; run it with Python 3. No hosted CI result is claimed.

**Evidence tier:** synthetic arithmetic cross-check only. No physical instrument, eyelid dataset, independently certified velocity ceiling, shutter timing, or held-out human labels. This does not increase the evidentiary tier of Lucent's product. Continue `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Next scientific experiment must use independently calibrated physical recordings or blinded human annotations; avoid more theorem-only iterations.
