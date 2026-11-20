#!/usr/bin/env python3
"""E002-707 strict prediction-side manifest preflight. Structural only, not blindness proof."""
import hashlib
import json
import math
import sys
from pathlib import Path

REQUIRED = {
 "participant_pseudonym","session_id","device_model","camera_firmware",
 "acquisition_clock_id","high_rate_file_sha256","low_rate_file_sha256",
 "exposure_start_interval","exposure_end_interval","roi_row","frame_drop_count",
 "aperture_scale_interval","aperture_error_interval","speed_ceiling_source",
 "clock_error_interval","shutter_gap_upper","closure_threshold","nuisance_tags"}
RECORD_KEYS = REQUIRED
ROOT_KEYS = {"schema","records"}
STRING_KEYS = {"participant_pseudonym","session_id","device_model","camera_firmware",
               "acquisition_clock_id","speed_ceiling_source"}
INTERVAL_KEYS = {"exposure_start_interval","exposure_end_interval",
                 "aperture_scale_interval","aperture_error_interval","clock_error_interval"}
SHA_KEYS = {"high_rate_file_sha256","low_rate_file_sha256"}
HEX = set("0123456789abcdef")

class Invalid(Exception):
    pass

def unique_pairs(pairs):
    result = {}
    for k,v in pairs:
        if k in result:
            raise Invalid("duplicate_json_key")
        result[k] = v
    return result

def finite(v):
    return type(v) in (int,float) and math.isfinite(v)

def validate(raw):
    try:
        obj = json.loads(raw, object_pairs_hook=unique_pairs,
                         parse_constant=lambda _: (_ for _ in ()).throw(Invalid("nonfinite_json_constant")))
        if type(obj) is not dict or set(obj) != ROOT_KEYS or obj["schema"] != "E002-707-v1":
            raise Invalid("invalid_root_schema")
        records = obj["records"]
        if type(records) is not list or not records or len(records) > 100000:
            raise Invalid("invalid_record_count")
        seen = set()
        for i,r in enumerate(records):
            if type(r) is not dict or set(r) != RECORD_KEYS:
                raise Invalid("record_%d_invalid_keys" % i)
            for k in STRING_KEYS:
                if type(r[k]) is not str or not r[k].strip() or len(r[k]) > 256:
                    raise Invalid("record_%d_bad_string_%s" % (i,k))
            ident = (r["participant_pseudonym"],r["session_id"])
            if ident in seen:
                raise Invalid("duplicate_participant_session")
            seen.add(ident)
            for k in SHA_KEYS:
                v = r[k]
                if type(v) is not str or len(v) != 64 or not set(v) <= HEX:
                    raise Invalid("record_%d_bad_digest_%s" % (i,k))
            for k in INTERVAL_KEYS:
                v = r[k]
                if type(v) is not list or len(v) != 2 or not all(finite(x) for x in v) or v[0] > v[1]:
                    raise Invalid("record_%d_bad_interval_%s" % (i,k))
            if r["aperture_scale_interval"][0] <= 0:
                raise Invalid("nonpositive_aperture_scale")
            if r["aperture_error_interval"][0] < 0:
                raise Invalid("negative_aperture_error")
            if r["exposure_start_interval"][1] > r["exposure_end_interval"][0]:
                raise Invalid("ambiguous_exposure_order")
            if type(r["frame_drop_count"]) is not int or r["frame_drop_count"] < 0:
                raise Invalid("invalid_frame_drop_count")
            if type(r["roi_row"]) is not int or r["roi_row"] < 0:
                raise Invalid("invalid_roi_row")
            for k in ("shutter_gap_upper","closure_threshold"):
                if not finite(r[k]) or r[k] < 0:
                    raise Invalid("bad_numeric_%s" % k)
            if type(r["nuisance_tags"]) is not list or not all(type(t) is str and 0 < len(t) <= 128 for t in r["nuisance_tags"]):
                raise Invalid("invalid_nuisance_tags")
        return []
    except (Invalid,ValueError,TypeError,OverflowError,RecursionError) as e:
        return [str(e)[:160]]

def main():
    if len(sys.argv) != 2:
        print(json.dumps({"verdict":"ABSTAIN_INVALID_MANIFEST","error":"expected_one_path"}))
        return 1
    try:
        raw = Path(sys.argv[1]).read_bytes()
        if len(raw) > 32_000_000:
            raise Invalid("manifest_too_large")
        errors = validate(raw)
        digest = hashlib.sha256(raw).hexdigest()
    except (OSError,Invalid) as e:
        errors = [str(e)[:160]]
        digest = None
    print(json.dumps({"schema":"E002-707-v1","manifest_sha256":digest,
      "verdict":"ABSTAIN_INVALID_MANIFEST" if errors else "STRUCTURE_ONLY_PASS",
      "errors":errors,"provenance_authenticated":False,"blindness_proven":False,
      "human_validation":False,"production_release":"BLOCKED"},sort_keys=True))
    return int(bool(errors))

if __name__ == "__main__":
    sys.exit(main())
