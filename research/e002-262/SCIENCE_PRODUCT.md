# SCIENCE ledger
Verified original human P_33/P_54 native Tobii reference bytes via SHA-256. Each five-second window contains 600 tracker rows, but only 200 unique timestamps with at least one valid eye. P_33 maximum gap between valid timestamps 30.119ms, P_54 26.705ms. Both have zero bilateral valid-free gaps >=100ms (also zero >=150ms). Consecutive invalid tracker rows are NOT blink events; original flawed proxy failed and was preserved.

# PRODUCT ledger
These two windows cannot supply reference-validity blink anchors to certify RGB/Tobii clock offset. Do not claim that no physical blinks occurred, that pupil dynamics are unobservable, or that fatigue can be inferred. Retire blink-clock synchronization for these windows; prioritize EVE Basler synchronized positive control or an equivalent accessible dataset. No app work. Product gate >=75% prospectively accurate accepted windows.
