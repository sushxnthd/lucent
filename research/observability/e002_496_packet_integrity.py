#!/usr/bin/env python3
"""E002-496: independent technical integrity check of private S01 review packet.

Only aggregate protocol checks are emitted. No image content, native frame index,
individual annotation, image hash or private path is ever emitted.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import stat

EXPECTED_MANIFEST_SHA256 = '1ad969e986c8d5f32235ba519e55889237e0cb6571edf7b321f8b0103845cdeb'
EXPECTED_CLIPS = {f'clip_{i:02d}' for i in range(20)}
EXPECTED_FIELDS = {'frame', 'upper_y', 'lower_y', 'iris_diameter', 'uncertainty_px', 'flags'}
PNG_SIG = b'\x89PNG\r\n\x1a\n'


def _json(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError('INVALID_PRIVATE_FILE')
    return json.loads(path.read_text())


def _validate_template(t, rater):
    if t.get('experiment') != 'E002-492' or t.get('rater') != rater:
        raise ValueError('WRONG_RATER_TEMPLATE')
    if set(t) != {'experiment', 'rater', 'clips'}:
        raise ValueError('RATER_METADATA_LEAK')
    clips = t.get('clips')
    if not isinstance(clips, dict) or set(clips) != EXPECTED_CLIPS:
        raise ValueError('RATER_CLIP_SET')
    for rows in clips.values():
        if not isinstance(rows, list) or len(rows) != 13:
            raise ValueError('RATER_FRAME_SET')
        for i, frame in enumerate(rows):
            if not isinstance(frame, dict) or set(frame) != EXPECTED_FIELDS:
                raise ValueError('RATER_FIELD_LEAK')
            if frame['frame'] != i or type(frame['frame']) is not int:
                raise ValueError('RATER_FRAME_ORDER')
            if frame['flags'] != ['UNREVIEWED']:
                raise ValueError('RATER_UNBLINDED_STATUS')
            if any(frame[k] is not None for k in
                   ('upper_y','lower_y','iris_diameter','uncertainty_px')):
                raise ValueError('RATER_PREPOPULATED_LABEL')


def validate(packet):
    root = Path(packet)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('INVALID_PRIVATE_ROOT')
    if os.name != 'nt' and (stat.S_IMODE(root.stat().st_mode) & 0o077):
        raise ValueError('PRIVATE_ROOT_PERMISSIONS')
    manifest = _json(root/'OWNER_ONLY_MAPPING.json')
    canonical = json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()
    if hashlib.sha256(canonical).hexdigest() != EXPECTED_MANIFEST_SHA256:
        raise ValueError('FROZEN_MAPPING_MISMATCH')
    for rater in ('A','B'):
        _validate_template(_json(root/f'RATER_{rater}_TEMPLATE.json'), rater)
    image_dir = root/'PRIVATE_FRAMES_DO_NOT_UPLOAD'
    if image_dir.is_symlink() or not image_dir.is_dir():
        raise ValueError('MISSING_PRIVATE_IMAGE_DIR')
    if os.name != 'nt' and (stat.S_IMODE(image_dir.stat().st_mode) & 0o077):
        raise ValueError('PRIVATE_IMAGE_DIR_PERMISSIONS')
    files = list(image_dir.iterdir())
    if len(files) != 260:
        raise ValueError('WRONG_IMAGE_COUNT')
    counts = Counter()
    for path in files:
        if path.is_symlink() or not path.is_file() or path.stat().st_size < 100:
            raise ValueError('INVALID_IMAGE_FILE')
        m = re.fullmatch(r'(clip_\d\d)_frame_(\d\d)\.png', path.name)
        if not m or m.group(1) not in EXPECTED_CLIPS or not (0 <= int(m.group(2)) < 13):
            raise ValueError('UNBLINDED_IMAGE_FILENAME')
        counts[(m.group(1), int(m.group(2)))] += 1
        with path.open('rb') as f:
            header = f.read(24)
        if (header[:8] != PNG_SIG or header[12:16] != b'IHDR' or
            int.from_bytes(header[16:20], 'big') != 320 or
            int.from_bytes(header[20:24], 'big') != 288):
            raise ValueError('IMAGE_GEOMETRY_MISMATCH')
    if len(counts) != 260 or any(v != 1 for v in counts.values()):
        raise ValueError('DUPLICATE_OR_MISSING_FRAME')
    return {
        'experiment': 'E002-496',
        'source': 'S01_CALIBRATION_ONLY',
        'status': 'TECHNICAL_PACKET_INTEGRITY_PASS',
        'private_native_png_frames': 260,
        'blinded_clip_count': 20,
        'frames_per_clip': 13,
        'native_width': 320,
        'native_height': 288,
        'rater_templates': 2,
        'frozen_mapping_sha256': EXPECTED_MANIFEST_SHA256,
        'human_anatomical_labels': 0,
        'camera_clock_authenticated': False,
        'physical_shutter_calibrated': False,
        'human_reference_validated': False,
        'evidence_tier': 'AUTHENTIC_HUMAN_PACKET_TECHNICAL_INTEGRITY_ONLY',
        'product': 'ABSTAIN_UNCALIBRATED',
        'release': 'BLOCKED',
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--packet', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    try:
        report = validate(args.packet)
        rc = 0
    except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError):
        # Never print private file names, source frame indices or image hashes.
        report = {'experiment':'E002-496','status':'FAILED_OR_ABSTAINED',
                  'human_anatomical_labels':0,'human_reference_validated':False,
                  'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}
        rc = 2
    Path(args.output).write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
