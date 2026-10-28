#!/usr/bin/env python3
"""E002-512 synthetic rolling-shutter scanline gap falsifier. No physical certification."""
import json
from decimal import Decimal, InvalidOperation, localcontext

EPS = Decimal('1e-20')

def dec(value):
    if isinstance(value, bool) or value is None:
        raise ValueError('INVALID_NUMERIC_INPUT')
    try:
        v = Decimal(str(value))
    except (TypeError, ValueError, InvalidOperation):
        raise ValueError('INVALID_NUMERIC_INPUT') from None
    if not v.is_finite():
        raise ValueError('NONFINITE_NUMERIC_INPUT')
    return v

def scanline_bound(*, period, exposure, speed, mean, mean_error, threshold,
                   line_delay, row_1, row_2, sensor_height, row_uncertainty=0,
                   clock_gap_error='0', readout_direction='TOP_TO_BOTTOM',
                   observation_model='AFFINE_SINGLE_SCANLINE',
                   same_aperture_assumed=True):
    """Research-only bound for one tracked scanline and one common latent aperture."""
    with localcontext() as ctx:
        ctx.prec = 70
        p, w, v, b, r, th, ell, j = map(dec, (
            period, exposure, speed, mean, mean_error, threshold,
            line_delay, clock_gap_error))
        if not (p > 0 and 0 < w <= p and v > 0 and 0 <= b <= 1
                and 0 <= r <= 1 and 0 < th < 1 and ell >= 0 and j >= 0):
            raise ValueError('INVALID_INSTRUMENT_DOMAIN')
        if type(sensor_height) is not int or sensor_height < 2:
            raise ValueError('INVALID_SENSOR_HEIGHT')
        if any(type(x) is not int for x in (row_1, row_2, row_uncertainty)):
            raise ValueError('INVALID_ROW_INTEGER')
        u = row_uncertainty
        if u < 0 or min(row_1, row_2)-u < 0 or max(row_1, row_2)+u >= sensor_height:
            raise ValueError('ROW_INTERVAL_OUT_OF_SENSOR')
        if readout_direction not in ('TOP_TO_BOTTOM', 'BOTTOM_TO_TOP'):
            raise ValueError('UNKNOWN_READOUT_DIRECTION')
        if observation_model != 'AFFINE_SINGLE_SCANLINE' or same_aperture_assumed is not True:
            raise ValueError('UNSUPPORTED_MULTIROW_OR_GEOMETRY_MODEL')
        eta = Decimal(1) - b + r
        if eta > 1:
            raise ValueError('APERTURE_ERROR_EXCEEDS_RANGE')
        if eta <= v*w/2:
            d = min(Decimal(1), (2*v*w*eta).sqrt())
        else:
            d = min(Decimal(1), eta+v*w/2)
        sign = Decimal(1) if readout_direction == 'TOP_TO_BOTTOM' else Decimal(-1)
        signed_drift = sign * (row_2-row_1)
        h_base = p-w
        h_min = h_base + ell*(signed_drift-2*u)-j
        h_max = h_base + ell*(signed_drift+2*u)+j
        if h_min < 0:
            raise ValueError('POSSIBLY_OVERLAPPING_EXPOSURES')
        risk = d + v*h_max/2
        margin = Decimal(1)-th-risk
        critical_extra_gap = 2*(Decimal(1)-th-d)/v-h_base
        return {
            'experiment': 'E002-512',
            'evidence_tier': 'SYNTHETIC_AFFINE_SCANLINE_TIMING',
            'conditional_scalar_result': ('CONDITIONAL_EXCLUSION'
                if margin > EPS else 'NOT_EXCLUDED_OR_BOUNDARY'),
            'deficit_bound': str(+d),
            'blind_gap_min_seconds': str(+h_min),
            'blind_gap_max_seconds': str(+h_max),
            'risk_upper': str(+risk),
            'margin': str(+margin),
            'critical_extra_gap_seconds': str(+critical_extra_gap),
            'critical_rows_at_assumed_line_delay': (
                str(+(critical_extra_gap/ell)) if ell else None),
            'readout_direction': readout_direction,
            'sensor_row_displacement': row_2-row_1,
            'row_uncertainty_each': u,
            'product': 'ABSTAIN_UNCALIBRATED',
            'release': 'BLOCKED',
            'camera_line_timing_authenticated': False,
            'eyelid_velocity_certified': False,
            'anatomical_labels_obtained': False,
            'physical_hidden_closure_certified': False,
            'full_rgb_claim_supported': False,
        }

def fixture(row_2=100, **kw):
    args = dict(period=Decimal(1)/30, exposure='0.010', speed='60',
                mean='0.999', mean_error='0.001', threshold='0.20',
                line_delay='0.0001', row_1=100, row_2=row_2,
                sensor_height=288)
    args.update(kw)
    return scanline_bound(**args)

if __name__ == '__main__':
    print(json.dumps({
        'drift_0': fixture(),
        'drift_plus_10': fixture(110),
        'drift_plus_20': fixture(120),
        'drift_minus_20': fixture(80),
        'drift_plus_10_with_five_row_uncertainty': fixture(110, row_uncertainty=5),
    }, indent=2, sort_keys=True))
