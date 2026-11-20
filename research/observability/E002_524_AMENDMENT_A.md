# E002-524 Amendment A | Full-closure exposure is sufficient, not necessary, for a reference witness

Date: 2026-10-29. Scientific interpretation correction after implementation; the original [frozen protocol](E002_524_FROZEN.md) is preserved as preregistered history.

The original E002-524 framing could be read as asserting that E002-519/520 **require** an entire reference exposure to fit inside a continuously closed eyelid interval. That assertion is **incorrect**.

- **E002-519:** the reference exposure must be contained within the ordinary camera's guaranteed **blind gap**, with calibrated timing and valid anatomy. This is a cross-camera temporal-containment condition, not a requirement that eyelids stay closed for the entire exposure.
- **E002-520:** a calibrated transported reference **exposure mean** below the ordinary closure threshold can establish at least one threshold crossing *during that exposure*. The actual closure may occupy only part of the exposure.
- **E002-521/522:** under calibrated shutter weighting and response-concentration bounds, a reference exposure mean can establish a positive **total closure duration** even without a wholly closed exposure.

Accordingly, E002-524's exact `d>P+e` law is only a **strong sufficient phase-independent opportunity** to capture one exposure entirely within a *continuous* closure. It is **not necessary** for a valid partial-exposure quantitative witness and must never be used to reject one. The `d>P-e` overlap boundary likewise guarantees only geometric overlap, not an interpretable image or anatomical threshold crossing.

The numeric 240-Hz/1-ms result is therefore an **instrument-design bound for full-closure exposures**, not a minimum measurable blink duration, minimum physiological blink duration, or limit on E002-520/522 quantitative reference evidence. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. No human or physical measurements were added.

This amendment does not alter the exact periodic lattice mathematics or the frozen numeric examples; it corrects the scientific interpretation and acceptance language. Future human studies must accept calibrated partial-exposure quantitative witnesses when E002-520/522 conditions hold, rather than imposing the stronger E002-524 full-exposure criterion as mandatory.
