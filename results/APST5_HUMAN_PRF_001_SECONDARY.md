# APST5-HUMAN-PRF-001 Secondary: Directional Human Response Kernels

**Status:** completed post-primary secondary/exploratory analysis.

**This result does not replace the failed preregistered primary H1/H2.**

## Directional held-out response adequacy

| subject | bright fit/val | dark fit/val | held-out RMSE | held-out R2 | sigma | split |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | 9/9 | 8/8 | 1.0248 | 0.0749 | 0.8860 | design |
| 02 | 12/12 | 12/12 | 0.9734 | 0.0557 | 0.6179 | held-out |
| 03 | 8/9 | 3/5 | 1.0714 | 0.0917 | 0.7564 | held-out |
| 04 | 12/12 | 12/11 | 1.1435 | 0.1353 | 0.8467 | held-out |
| 05 | 12/12 | 12/12 | 1.2317 | 0.1464 | 1.0234 | held-out |
| 07 | 12/12 | 12/12 | 0.7854 | 0.2008 | 0.7041 | held-out |
| 08 | 12/11 | 12/12 | 1.3433 | -0.1036 | 0.8486 | design |
| 09 | 12/12 | 12/9 | 0.8106 | -0.1852 | 0.6925 | design |
| 10 | 12/12 | 12/12 | 1.0002 | 0.1594 | 0.8673 | held-out |
| 11 | 11/8 | 8/12 | 1.0545 | -0.0351 | 0.6881 | design |
| 12 | 12/12 | 12/12 | 1.0787 | -0.0282 | 0.4106 | design |
| 13 | 12/12 | 12/12 | 1.0431 | 0.3653 | 0.9238 | held-out |
| 14 | 5/9 | 7/7 | 0.8071 | 0.2734 | 0.7026 | design |
| 15 | 12/12 | 12/12 | 1.0966 | 0.4713 | 0.8783 | held-out |
| 16 | 12/12 | 12/12 | 1.0939 | -0.0087 | 0.8356 | held-out |
| 17 | 12/12 | 12/11 | 1.0580 | 0.4712 | 0.9942 | held-out |
| 18 | 12/12 | 12/12 | 0.9270 | 0.3011 | 0.8003 | design |
| 19 | 12/12 | 12/12 | 0.9857 | 0.3276 | 0.8475 | design |
| 20 | 12/12 | 12/11 | 1.1278 | 0.2172 | 0.9179 | design |
| 21 | 8/11 | 10/8 | 0.8304 | 0.2254 | 0.8091 | held-out |
| 22 | 11/11 | 12/12 | 1.2322 | 0.0902 | 0.8493 | design |
| 23 | 12/10 | 10/11 | 0.9658 | -0.1093 | 0.8212 | design |

Non-positive directional held-out R2: **6/22** (08, 09, 11, 12, 16, 23).

## Equal-exposure secondary result

Directional design-set P10 search selected **(1, 2, 8)**.

| Probe | positions | design P10 S | held-out P10 S | held-out median S | held-out S>1.25 | design rank | required log-contrast | required luminance ratio |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| directional_selected | (1, 2, 8) | 1.310 | **1.264** | 1.836 | 90.9% | 1 | 0.989 | 2.69x |
| frozen_e002 | (1, 2, 8) | 1.310 | **1.264** | 1.836 | 90.9% | 1 | 0.989 | 2.69x |
| sim005 | (1, 2, 9) | 1.248 | **1.238** | 1.844 | 81.8% | 8 | 1.010 | 2.75x |
| evenly_spaced | (2, 5, 8) | 0.955 | **1.099** | 1.543 | 72.7% | 43 | 1.138 | 3.12x |

## Interpretation

Separating brightening and darkening response kernels tests whether the primary single-kernel model was too restrictive. Any improvement here is secondary evidence about response asymmetry, not a confirmatory rescue of the primary test.

The required-contrast columns use the LTI model's linear amplitude scaling to report the minimum high/low luminance ratio whose P10 separation would reach S=1.25. They are design requirements, not measurements of the current phone screen.

## Failures

- 06: missing luminance pupil file

## Claim boundary

This secondary analysis remains an EyeLink-based response-model bridge. It does not establish RGB-phone observability or state prediction.
