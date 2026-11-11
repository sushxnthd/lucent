#!/usr/bin/env python3
"""E002-566: independent post-handoff audit. Never emit private source content."""
import argparse
import hashlib
import hmac
import json
from pathlib import Path

FRAME_NAMES = {f'clip_{i:02d}_frame_{j:02d}.png' for i in range(20) for j in range(13)}
FIELDS = {'frame', 'upper_y', 'lower_y', 'iris_diameter', 'uncertainty_px', 'flags'}


def digest_file(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.digest()


def safe_file(path):
    return path.is_file() and not path.is_symlink() and path.stat().st_size > 0


def audit(root, viewer):
    root, viewer = Path(root), Path(viewer)
    if root.is_symlink() or not root.is_dir() or not safe_file(viewer):
        raise ValueError('INVALID_ROOT_OR_VIEWER')
    owner = root / 'OWNER_PRIVATE_DO_NOT_SHARE' / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
    if owner.is_symlink() or not owner.is_dir():
        raise ValueError('OWNER_IMAGES_MISSING')
    if {p.name for p in owner.iterdir()} != FRAME_NAMES:
        raise ValueError('OWNER_FRAME_SET_MISMATCH')
    if any(not safe_file(p) for p in owner.iterdir()):
        raise ValueError('OWNER_FRAME_INVALID')
    expected_html = digest_file(viewer)
    for r in ('A', 'B'):
        folder = root / 'REVIEWER_PACKETS' / f'RATER_{r}_PRIVATE'
        if folder.is_symlink() or not folder.is_dir():
            raise ValueError('RATER_BUNDLE_MISSING')
        expected = {'PRIVATE_FRAMES_DO_NOT_UPLOAD', f'RATER_{r}_TEMPLATE.json',
                    'e002_497_offline_rater.html', 'READ_ME_PRIVATE.txt'}
        if {p.name for p in folder.iterdir()} != expected:
            raise ValueError('RATER_EXTRA_OR_MISSING_FILE')
        images = folder / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
        if images.is_symlink() or not images.is_dir() or {p.name for p in images.iterdir()} != FRAME_NAMES:
            raise ValueError('RATER_FRAME_SET_MISMATCH')
        if not safe_file(folder / 'READ_ME_PRIVATE.txt'):
            raise ValueError('INSTRUCTIONS_MISSING')
        if not safe_file(folder / 'e002_497_offline_rater.html') or not hmac.compare_digest(
                digest_file(folder / 'e002_497_offline_rater.html'), expected_html):
            raise ValueError('RATER_VIEWER_MISMATCH')
        template = folder / f'RATER_{r}_TEMPLATE.json'
        if not safe_file(template):
            raise ValueError('RATER_TEMPLATE_MISSING')
        obj = json.loads(template.read_text())
        if set(obj) != {'experiment', 'rater', 'clips'} or obj['experiment'] != 'E002-492' or obj['rater'] != r:
            raise ValueError('RATER_TEMPLATE_WRONG_IDENTITY')
        if not isinstance(obj['clips'], dict) or set(obj['clips']) != {f'clip_{i:02d}' for i in range(20)}:
            raise ValueError('RATER_TEMPLATE_WRONG_CLIPS')
        for clip in obj['clips'].values():
            if not isinstance(clip, list) or len(clip) != 13:
                raise ValueError('RATER_TEMPLATE_WRONG_LENGTH')
            for j, frame in enumerate(clip):
                if (not isinstance(frame, dict) or set(frame) != FIELDS or
                        type(frame['frame']) is not int or frame['frame'] != j or
                        frame['flags'] != ['UNREVIEWED'] or
                        any(frame[k] is not None for k in FIELDS - {'frame', 'flags'})):
                    raise ValueError('RATER_TEMPLATE_PREPOPULATED')
        for name in FRAME_NAMES:
            a, b = owner / name, images / name
            if not safe_file(b) or not hmac.compare_digest(digest_file(a), digest_file(b)):
                raise ValueError('RATER_FRAME_NOT_SOURCE_BOUND')
    return {'experiment': 'E002-566', 'status': 'AUTHENTIC_RATER_BUNDLES_VERIFIED',
            'source_bound_native_frames': 260, 'private_rater_bundles': 2,
            'frames_per_rater': 260, 'independent_human_raters': 0,
            'physical_clock_authenticated': False, 'shutter_calibrated': False,
            'continuous_time_speed_certified': False,
            'heldout_physical_predictions': 0,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True)
    p.add_argument('--viewer', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    try:
        result = audit(args.root, args.viewer)
        rc = 0
    except Exception:
        result = {'experiment': 'E002-566', 'status': 'FAILED_OR_ABSTAINED',
                  'independent_human_raters': 0, 'physical_clock_authenticated': False,
                  'shutter_calibrated': False, 'continuous_time_speed_certified': False,
                  'heldout_physical_predictions': 0,
                  'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}
        rc = 2
    Path(args.output).write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
