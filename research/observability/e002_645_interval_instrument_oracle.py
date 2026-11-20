#!/usr/bin/env python3
"""E002-645: interval-certified LED visibility oracle (instrument surrogate only).

All times are integer microseconds on ONE authenticated clock. Intervals are
closed uncertainty sets, not measured probability distributions. Exposure
windows must include all relevant rows, subexposures and rolling-shutter offsets.
No physiology is inferred.
"""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Exposure:
    start_lo: int
    start_hi: int
    end_lo: int
    end_hi: int

@dataclass(frozen=True)
class Pulse:
    start_lo: int
    start_hi: int
    end_lo: int
    end_hi: int

def valid(lo, hi):
    return isinstance(lo, int) and isinstance(hi, int) and lo <= hi

def classify(p: Pulse, exposures: Sequence[Exposure], *, certified_clock: bool,
             certified_exposures: bool, certified_snr: bool) -> str:
    """Return GUARANTEED_MISS, GUARANTEED_INTERSECTION or ABSTAIN.

    INTERSECTION is geometric only: no guarantee of photometric detectability.
    Actual measured visibility is never an input to the prediction.
    """
    if not (certified_clock and certified_exposures) or not exposures:
        return "ABSTAIN"
    if not (valid(p.start_lo,p.start_hi) and valid(p.end_lo,p.end_hi)
            and p.start_hi < p.end_lo):
        return "ABSTAIN"
    for e in exposures:
        if not (valid(e.start_lo,e.start_hi) and valid(e.end_lo,e.end_hi)
                and e.start_hi < e.end_lo):
            return "ABSTAIN"
    # If the pulse can overlap any exposure under uncertainty, cannot certify a miss.
    if all(p.end_hi <= e.start_lo or p.start_lo >= e.end_hi for e in exposures):
        return "GUARANTEED_MISS"
    # A guaranteed strictly positive overlap with at least one exposure.
    # This does NOT guarantee detector visibility, even if SNR is certified:
    # threshold depends on integrated photons and image processing.
    if certified_snr and any(p.start_hi < e.end_lo and p.end_lo > e.start_hi
                             for e in exposures):
        return "GUARANTEED_INTERSECTION"
    return "ABSTAIN"

def test():
    e=[Exposure(100,102,110,112)]
    assert classify(Pulse(80,81,90,91),e,certified_clock=True,
                    certified_exposures=True,certified_snr=True)=="GUARANTEED_MISS"
    assert classify(Pulse(120,121,130,131),e,certified_clock=True,
                    certified_exposures=True,certified_snr=True)=="GUARANTEED_MISS"
    assert classify(Pulse(103,104,108,109),e,certified_clock=True,
                    certified_exposures=True,certified_snr=True)=="GUARANTEED_INTERSECTION"
    assert classify(Pulse(109,111,120,121),e,certified_clock=True,
                    certified_exposures=True,certified_snr=True)=="ABSTAIN"
    assert classify(Pulse(103,104,108,109),e,certified_clock=False,
                    certified_exposures=True,certified_snr=True)=="ABSTAIN"
    assert classify(Pulse(103,104,108,109),e,certified_clock=True,
                    certified_exposures=True,certified_snr=False)=="ABSTAIN"
    assert classify(Pulse(103,104,108,109),e+[Exposure(200,202,210,212)],
                    certified_clock=True,certified_exposures=True,
                    certified_snr=True)=="GUARANTEED_INTERSECTION"
    # A second exposure can invalidate a purported guaranteed miss.
    assert classify(Pulse(80,81,90,91),e+[Exposure(85,86,95,96)],
                    certified_clock=True,certified_exposures=True,
                    certified_snr=True)=="GUARANTEED_INTERSECTION"
    assert classify(Pulse(80,81,90,91),[Exposure(100,99,110,112)],
                    certified_clock=True,certified_exposures=True,
                    certified_snr=True)=="ABSTAIN"
    print("9 deterministic synthetic assertions passed; no physical evidence")

if __name__ == "__main__":
    test()
