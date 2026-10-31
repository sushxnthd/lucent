#!/usr/bin/env python3
"""E002-500: private source-bound S01 replay, NOT human anatomical validation."""
import argparse
import hashlib
import hmac
import json
from pathlib import Path
import tempfile

from e002_492_anatomical_review import build_manifest, extract_frames_local_only
from e002_496_packet_integrity import validate as legacy_packet_validate

NAMES = tuple(f'clip_{i:02d}_frame_{j:02d}.png' for i in range(20) for j in range(13))

def digest_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.digest()

def compare_private_frames(packet_images, independently_extracted_images):
    """Compare all private PNG bytes without revealing names, indices or hashes."""
    a, b = Path(packet_images), Path(independently_extracted_images)
    if not a.is_dir() or not b.is_dir():
        raise ValueError('PRIVATE_IMAGE_DIRECTORY_MISSING')
    if ({p.name for p in a.iterdir()} != set(NAMES) or
            {p.name for p in b.iterdir()} != set(NAMES)):
        raise ValueError('SOURCE_FRAME_SET_MISMATCH')
    for name in NAMES:
        x, y = a / name, b / name
        if (x.is_symlink() or y.is_symlink() or not x.is_file() or not y.is_file()
                or x.stat().st_size != y.stat().st_size
                or not hmac.compare_digest(digest_file(x), digest_file(y))):
            raise ValueError('SOURCE_FRAME_CONTENT_MISMATCH')
    return True

def verify_against_source(packet, archive):
    """Re-extract independently from the pinned source; not an independent decoder."""
    packet = Path(packet)
    legacy_packet_validate(packet)
    with tempfile.TemporaryDirectory(prefix='lucent500_private_') as td:
        extract_frames_local_only(archive, td, build_manifest())
        compare_private_frames(packet / 'PRIVATE_FRAMES_DO_NOT_UPLOAD',
                               Path(td) / 'PRIVATE_FRAMES_DO_NOT_UPLOAD')
    return {'experiment': 'E002-500', 'status': 'SOURCE_REPLAY_MATCH',
            'evidence_tier': 'SOURCE_BOUND_PACKET_ONLY',
            'source_archive_checksum_pinned': True,
            'private_source_frame_matches': 260,
            'human_anatomical_labels': 0, 'acquisition_fps_authenticated': False,
            'physical_shutter_calibrated': False,
            'human_reference_validated': False,
            'physical_hidden_closure_certified': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', required=True)
    p.add_argument('--archive', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    try:
        report = verify_against_source(args.packet, args.archive)
        rc = 0
    except Exception:
        report = {'experiment': 'E002-500', 'status': 'FAILED_OR_ABSTAINED',
                  'human_anatomical_labels': 0, 'source_replay_verified': False,
                  'human_reference_validated': False,
                  'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}
        rc = 2
    Path(args.output).write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))
    return rc

if __name__ == '__main__':
    raise SystemExit(main())
