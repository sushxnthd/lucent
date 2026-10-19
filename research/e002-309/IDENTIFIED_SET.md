# Conditional exposure-weighting law

Define q as an ocular area fraction and v as visibility. Assume q in [0,1], v in [m,M] with m positive. The exposure observable is the ratio of the integral of v times q to the integral of v.

For observed value z, the exact feasible range of the unweighted mean q is:

lower = m*z / (M*(1-z)+m*z)
upper = M*z / (m*(1-z)+M*z)

For two exposures, a true mean increase is certain only if the second lower bound exceeds the first upper bound.

For m/M = 0.25, an observed z of 0.5 admits true means 0.2 and 0.8.

This is a mathematical oracle model, not validated human RGB measurement.