"""E002-675: fail-closed numerical input screening; NOT physical calibration verification."""
import math
import json
import sys
from pathlib import Path

REQUIRED = ('velocity_bound', 'clock_error_seconds', 'shutter_exposure_seconds', 'measurement_error', 'calibration_artifact_sha256', 'capture_artifact_sha256')

def positive_number(x, allow_zero=False):
    return type(x) in (float, int) and math.isfinite(x) and (x >= 0 if allow_zero else x > 0)

def screen(row):
    if not all(k in row for k in REQUIRED):
        return False, 'missing_numerical_or_provenance_field'
    if row.get('velocity_units') != 'normalized_aperture_per_second':
        return False, 'velocity_units_unverified'
    if row.get('measurement_error_units') != 'normalized_aperture':
        return False, 'measurement_units_unverified'
    if not positive_number(row['velocity_bound']):
        return False, 'invalid_velocity_bound'
    if not positive_number(row['clock_error_seconds'], True):
        return False, 'invalid_clock_error'
    if not positive_number(row['shutter_exposure_seconds']):
        return False, 'invalid_exposure'
    if not positive_number(row['measurement_error'], True) or row['measurement_error'] > 1:
        return False, 'invalid_measurement_error'
    for key in ('calibration_artifact_sha256','capture_artifact_sha256'):
        value = row[key]
        if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
            return False, 'invalid_artifact_digest'
    if row.get('calibration_independently_verified') is not True:
        return False, 'external_calibration_not_verified'
    return False, 'external_verification_not_machine_authenticated'

def audit(data):
    if data.get('protocol') != 'E002-671':
        raise ValueError('wrong protocol')
    rows = data.get('records')
    if not isinstance(rows, list):
        raise ValueError('records must be a list')
    reasons = {}
    for row in rows:
        if row.get('certificate') is True:
            ok, reason = screen(row)
            if not ok:
                reasons[reason] = reasons.get(reason, 0) + 1
    return {'total_records':len(rows),'eligible_certificates':0,'rejected_certificate_reasons':reasons,'release_blocked':True,'decision':'ABSTAIN_UNCALIBRATED'}

def selftest():
    base = dict(certificate=True, velocity_bound=60, velocity_units='normalized_aperture_per_second', measurement_error_units='normalized_aperture',clock_error_seconds=0.0001,shutter_exposure_seconds=1/30,measurement_error=0.01,calibration_artifact_sha256='a'*64,capture_artifact_sha256='b'*64,calibration_independently_verified=True)
    for mutation in ({},{'velocity_bound':-1},{'velocity_bound':0,'velocity_units':'unknown'},{'clock_error_seconds':-999},{'shutter_exposure_seconds':-1},{'measurement_error':float('nan')}):
        x = dict(base,**mutation)
        if not mutation:
            x.pop('velocity_bound')
        ok, reason = screen(x)
        assert not ok and reason
    assert screen(base) == (False,'external_verification_not_machine_authenticated')
    assert audit({'protocol':'E002-671','records':[base]})['eligible_certificates']==0
    print('E002-675: 8 fail-closed assertions passed; no independent calibration established')

if __name__ == '__main__':
    if sys.argv[1:] == ['--self-test']:
        selftest()
    else:
        print(json.dumps(audit(json.loads(Path(sys.argv[1]).read_text())),indent=2))
