#!/usr/bin/env python3
"""E002-565: fail-closed, record-bound identity join for human reference evidence.

The public Zenodo record registry is source metadata, not a camera-time certificate.
This function does not verify downloaded bytes, signatures, participant identity,
independent ratings, exposure, or continuous-time physiological assumptions.
"""
import argparse
import json
import re
from pathlib import PurePosixPath, Path

REGISTRY = {
    '18970793': {'paradigm': 'motor_imagery', 'prefix': 'MI',
                 'archive_md5': 'fb56109542a13aa7879778833fe4cbaa'},
    '18971758': {'paradigm': 'motor_execution', 'prefix': 'ME',
                 'archive_md5': 'bce89dd9fbb67e27a656623aa27927e0'},
}
FIELDS = ('zenodo_record', 'paradigm', 'archive_md5', 'video_member',
          'session', 'participant_id', 'video_sha256', 'frame_namespace')


def valid_identity(obj):
    if not isinstance(obj, dict) or any(not isinstance(obj.get(k), str) for k in FIELDS):
        return False
    record = obj['zenodo_record']
    spec = REGISTRY.get(record)
    if spec is None or obj['paradigm'] != spec['paradigm'] or obj['archive_md5'] != spec['archive_md5']:
        return False
    if not re.fullmatch(r'[0-9a-f]{64}', obj['video_sha256']):
        return False
    if not re.fullmatch(r'S[0-9]{2}', obj['participant_id']):
        return False
    if not re.fullmatch(r'Sess[0-9]{2}', obj['session']):
        return False
    member = obj['video_member']
    # No absolute paths, traversals, backslashes or unknown hierarchy.
    if '\\' in member or not re.fullmatch(
        rf'{obj["session"]}/{spec["prefix"]}[0-9]{{3}}_phantom\.avi', member
    ):
        return False
    if obj['frame_namespace'] != 'native-index:' + PurePosixPath(member).name:
        return False
    return True


def adjudicate_source(prediction, witness):
    """Return only a necessary identity match, never an anatomical verdict."""
    a = prediction.get('source') if isinstance(prediction, dict) else None
    b = witness.get('source') if isinstance(witness, dict) else None
    if not valid_identity(a) or not valid_identity(b):
        status = 'REJECT_INCOMPLETE_OR_CONTRADICTORY_SOURCE'
    elif a['paradigm'] != b['paradigm'] or a['zenodo_record'] != b['zenodo_record']:
        status = 'REJECT_CROSS_PARADIGM'
    elif a['video_sha256'] != b['video_sha256']:
        status = 'REJECT_VIDEO_IDENTITY'
    elif any(a[k] != b[k] for k in ('video_member', 'session', 'participant_id', 'frame_namespace')):
        status = 'REJECT_SAMPLE_NAMESPACE'
    else:
        status = 'SOURCE_MATCH_ONLY_UNCALIBRATED'
    return {
        'experiment': 'E002-565',
        'status': status,
        'source_match_only': status == 'SOURCE_MATCH_ONLY_UNCALIBRATED',
        'physical_validation': False,
        'reference_negative_evidence': 'CENSORED',
        'product': 'ABSTAIN_UNCALIBRATED',
        'release': 'BLOCKED',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prediction', required=True)
    parser.add_argument('--witness', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    a = json.loads(Path(args.prediction).read_text())
    b = json.loads(Path(args.witness).read_text())
    result = adjudicate_source(a, b)
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
