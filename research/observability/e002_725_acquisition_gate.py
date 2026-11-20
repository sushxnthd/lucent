"""E002-725: fail-closed acquisition record schema; NOT a calibration certificate."""
import csv,json,sys
from decimal import Decimal,InvalidOperation
REQUIRED=('trial_id','reference_kind','reference_calibration_id','camera_exposure_start_s','camera_exposure_end_s','reference_clock_uncertainty_s','camera_clock_uncertainty_s','aperture_lower','aperture_upper','velocity_upper','reference_closure','reference_label_valid','nuisance','target_fps','participant_id')
NUMERIC=('camera_exposure_start_s','camera_exposure_end_s','reference_clock_uncertainty_s','camera_clock_uncertainty_s','aperture_lower','aperture_upper','velocity_upper')
def inspect(row):
    missing=[k for k in REQUIRED if k not in row or row[k] is None or str(row[k]).strip()=='']
    if missing:return 'ABSTAIN_MISSING:'+','.join(missing)
    try:d={k:Decimal(str(row[k])) for k in NUMERIC}
    except (InvalidOperation,ValueError):return 'ABSTAIN_INVALID_NUMERIC'
    if not all(v.is_finite() for v in d.values()):return 'ABSTAIN_NONFINITE'
    if d['camera_exposure_end_s']<=d['camera_exposure_start_s']:return 'ABSTAIN_EXPOSURE_ORDER'
    if any(d[k]<0 for k in ('reference_clock_uncertainty_s','camera_clock_uncertainty_s','aperture_lower','aperture_upper','velocity_upper')):return 'ABSTAIN_NEGATIVE_BOUND'
    if d['aperture_lower']>d['aperture_upper']:return 'ABSTAIN_APERTURE_ORDER'
    if row['reference_kind'] not in ('photodiode','encoder','high_rate_independent_camera'):return 'ABSTAIN_REFERENCE_KIND'
    if row['reference_label_valid']!='true' or row['reference_closure'] not in ('true','false'):return 'ABSTAIN_REFERENCE_INVALID'
    if row['participant_id']!='INSTRUMENT_ONLY':return 'ABSTAIN_WRONG_POPULATION'
    return 'RECORD_COMPLETE_NOT_CALIBRATED'
def evaluate(rows):
    seen=set();out=[]
    for row in rows:
        tid=row.get('trial_id','')
        verdict='ABSTAIN_DUPLICATE_TRIAL' if tid in seen else inspect(row)
        seen.add(tid);out.append({'trial_id':tid,'record_status':verdict})
    return out
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python e002_725_acquisition_gate.py records.csv')
    with open(sys.argv[1],newline='',encoding='utf-8') as f:result=evaluate(csv.DictReader(f))
    print(json.dumps({'total':len(result),'records':result},indent=2))
