"""E002-572: conservative optical-edge timing instrument, synthetic until physical input.

Only use independent photodiode edges and raw-linear sensor fractions. A fitted
camera timestamp is NOT an independently authenticated sensor exposure time.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


class CalibrationError(ValueError):
    pass


def _num(x, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise CalibrationError("INVALID_" + name.upper())
    return float(x)


@dataclass(frozen=True)
class Edge:
    camera_time_s: float
    reference_edge_s: float
    post_edge_fraction: float
    edge_uncertainty_s: float
    fraction_uncertainty: float
    row_skew_bound_s: float = 0.0


@dataclass(frozen=True)
class Instrument:
    shutter_min_s: float
    shutter_max_s: float
    offset_min_s: float
    offset_max_s: float
    rate_min: float
    rate_max: float


def _validate_instrument(inst):
    v = [_num(getattr(inst, field), field) for field in
         ("shutter_min_s", "shutter_max_s", "offset_min_s",
          "offset_max_s", "rate_min", "rate_max")]
    wlo, whi, alo, ahi, blo, bhi = v
    if not (0 < wlo <= whi and alo < ahi and 0 < blo < bhi):
        raise CalibrationError("INVALID_INSTRUMENT_PRIORS")
    return wlo, whi, alo, ahi, blo, bhi


def edge_start_interval(edge, inst):
    """Conservative exposure-start interval, including reference/row uncertainty."""
    wlo, whi, *_ = _validate_instrument(inst)
    c, t, f, dt, df, dr = [_num(getattr(edge, field), field) for field in
        ("camera_time_s", "reference_edge_s", "post_edge_fraction",
         "edge_uncertainty_s", "fraction_uncertainty", "row_skew_bound_s")]
    if not (0 < f < 1 and 0 < df < min(f, 1-f) and dt > 0 and dr >= 0):
        raise CalibrationError("INVALID_EDGE_OR_LINEAR_FRACTION")
    return (t-dt-whi*(1-f+df)-dr, t+dt-wlo*(1-f-df)+dr)


def _clip(poly, A, B, C):
    """Clip polygon by A*offset + B*rate <= C."""
    if not poly:
        return []
    out = []
    for j, q in enumerate(poly):
        p = poly[j-1]
        vp = A*p[0]+B*p[1]-C
        vq = A*q[0]+B*q[1]-C
        pin, qin = vp <= 1e-12, vq <= 1e-12
        if pin != qin:
            den = vp-vq
            if den:
                z = vp/den
                out.append((p[0]+z*(q[0]-p[0]), p[1]+z*(q[1]-p[1])))
        if qin:
            out.append(q)
    return out


def calibrate(edges, inst):
    """Return full feasible (offset, rate) polygon or reject all data."""
    _, _, alo, ahi, blo, bhi = _validate_instrument(inst)
    if not isinstance(edges, (tuple, list)) or len(edges) < 3:
        raise CalibrationError("INSUFFICIENT_INDEPENDENT_EDGES")
    cs = [_num(e.camera_time_s, "camera_time_s") for e in edges]
    if len(set(cs)) < 3:
        raise CalibrationError("INSUFFICIENT_DISTINCT_TIMESTAMPS")
    poly = [(alo,blo),(ahi,blo),(ahi,bhi),(alo,bhi)]
    for e in edges:
        lo, hi = edge_start_interval(e, inst)
        c = e.camera_time_s
        poly = _clip(poly, 1.0, c, hi)
        poly = _clip(poly, -1.0, -c, -lo)
        if not poly:
            raise CalibrationError("CALIBRATION_REJECTED")
    return tuple(poly)


def heldout_test(poly, edge, inst):
    """No refitting: compare independent held-out optical edge to feasible clock."""
    if not poly:
        raise CalibrationError("EMPTY_CALIBRATION")
    lo, hi = edge_start_interval(edge, inst)
    c = edge.camera_time_s
    pred_lo = min(a+b*c for a,b in poly)
    pred_hi = max(a+b*c for a,b in poly)
    decision = "CONTRADICTION" if pred_hi < lo-1e-12 or hi < pred_lo-1e-12 else "CONSISTENT"
    return {
        "decision": decision,
        "measured_start_interval_s": (lo,hi),
        "predicted_start_interval_s": (pred_lo,pred_hi),
        "physiological_claim": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
        "evidence_tier": "SYNTHETIC_OR_INSTRUMENT_ONLY",
    }


def synthetic_fixture():
    inst = Instrument(.00395,.00405,-.05,.05,.999,1.001)
    a, b, w = .012, 1.000020, .004
    def make(c, f, shift=0.0):
        t = a+b*c+w*(1-f)+shift
        return Edge(c,t,f,.00005,.01,.00003)
    return inst, [make(c,f) for c,f in zip((0,10,20,30),(.2,.4,.6,.8))], make(40,.5), make(40,.5,.010)


if __name__ == "__main__":
    inst, training, clean, delayed = synthetic_fixture()
    polygon = calibrate(training, inst)
    print("SYNTHETIC_CALIBRATION_FEASIBLE", len(polygon))
    print("HELDOUT_CLEAN", heldout_test(polygon,clean,inst))
    print("HELDOUT_DELAYED", heldout_test(polygon,delayed,inst))
