#!/usr/bin/env python3
"""Pre-reference, fail-closed E002-690 prediction freeze. Standard library only."""
import argparse,csv,hashlib,json,pathlib,sys
from decimal import Decimal,InvalidOperation
FIELDS=('trial_id','aperture_left_low_mm','aperture_left_high_mm','aperture_right_low_mm','aperture_right_high_mm','closure_threshold_mm','velocity_ceiling_mm_per_s','blind_gap_upper_s','velocity_evidence_id','calibration_id','provenance_verified')

def number(row,key):
    try:
        x=Decimal(row[key]); assert x.is_finite() and x>=0
        return x
    except (KeyError,InvalidOperation,AssertionError): raise ValueError('invalid '+key)

def decide(row):
    for k in FIELDS:
        if not row.get(k): return 'ABSTAIN_MISSING_'+k.upper(),None
    if row['provenance_verified'].strip().lower()!='true': return 'ABSTAIN_UNVERIFIED',None
    a,A,b,B,c,V,h=[number(row,k) for k in FIELDS[1:8]]
    if a>A or b>B: return 'ABSTAIN_BAD_INTERVAL',None
    if not row['velocity_evidence_id'].strip() or not row['calibration_id'].strip():return 'ABSTAIN_UNCALIBRATED',None
    left=max(a,b-V*h);right=max(b,a-V*h)
    if left>A or right>B:return 'ABSTAIN_INCONSISTENT',None
    lower=max(Decimal(0),(left+right-V*h)/2)
    return ('CERTIFY_EXCLUSION' if lower>c else 'ABSTAIN_POSSIBLE_CLOSURE'),str(lower)

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');a=p.parse_args()
    src=pathlib.Path(a.input);dst=pathlib.Path(a.output)
    if dst.exists():sys.exit('Refusing overwrite of frozen predictions')
    if src.resolve()==dst.resolve():sys.exit('Input/output collision')
    with src.open(newline='') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or any(k not in reader.fieldnames for k in FIELDS):sys.exit('Missing mandatory columns')
        if any(k.startswith('reference_min') or k in ('reference_label','phone_decision') for k in reader.fieldnames):sys.exit('Reference labels or prior decisions in pre-freeze input')
        rows=list(reader)
    if not rows:sys.exit('No rows')
    if len({r['trial_id'] for r in rows})!=len(rows):sys.exit('Duplicate trial_id')
    out=[]
    for row in rows:
        try:decision,lower=decide(row)
        except ValueError as e:decision,lower='ABSTAIN_INVALID_'+str(e).replace(' ','_').upper(),None
        out.append({'trial_id':row['trial_id'],'decision':decision,'lower_bound_mm':lower})
    payload={'schema':'E002-695-v1','input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'predictions':out}
    encoded=(json.dumps(payload,sort_keys=True,indent=2)+'\n').encode()
    dst.open('xb').write(encoded)
    print(json.dumps({'output_sha256':hashlib.sha256(encoded).hexdigest(),'trials':len(out),'certificates':sum(x['decision']=='CERTIFY_EXCLUSION' for x in out)}))
if __name__=='__main__':main()
